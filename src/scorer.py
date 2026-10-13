"""
Content Psychology Scoring Engine
Scores media content across seven psychological engagement dimensions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List
import re
import unicodedata

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .frameworks import ENGAGEMENT_DIMENSIONS, CONTENT_PROFILE_TYPES

_vader = SentimentIntensityAnalyzer()


@dataclass
class DimensionScore:
    dimension_id: str
    label: str
    short: str
    score: float          # 0-100
    signals: List[str]    # matched keywords plus derived signals (VADER, counts) for display
    theory: str
    color: str
    cues: List[str] = field(default_factory=list)   # matched keywords/phrases only


@dataclass
class ContentScore:
    text: str
    label: str
    content_type: str
    dimensions: Dict[str, DimensionScore]
    overall_score: float          # 0-100
    profile_type: str
    dominant_dimensions: List[str]
    recommendations: List[str]
    vader_scores: dict
    word_count: int


_QUOTE_FOLD = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"'})


def _norm(text: str) -> str:
    """NFKC-normalise, fold curly quotes to ASCII, lowercase and collapse whitespace,
    so "won’t" matches the keyword "won't" and full-width letters match ASCII ones."""
    text = unicodedata.normalize("NFKC", text).translate(_QUOTE_FOLD)
    return re.sub(r"\s+", " ", text.lower().strip())


@lru_cache(maxsize=None)
def _pattern(keyword: str) -> "re.Pattern[str]":
    # Whole-word / whole-phrase match: "us" must not match "because", "hit" not "white".
    kw = re.escape(keyword.strip().lower())
    return re.compile(rf"(?<![\w#]){kw}(?!\w)")


def find_keywords(text: str, keywords: List[str]) -> List[str]:
    """Distinct keywords (in list order) that occur in `text` as whole words/phrases."""
    seen, matched = set(), []
    for kw in keywords:
        key = kw.strip().lower()
        if key not in seen and _pattern(key).search(text):
            seen.add(key)
            matched.append(key)
    return matched


def _kw_score(text: str, keywords: List[str], scale: float = 1.0) -> tuple:
    matched = find_keywords(text, keywords)
    ratio = len(matched) / max(len(keywords), 1)
    raw = min(ratio * 400 * scale, 100)
    return raw, matched


# ── Dimension-specific scorers ────────────────────────────────────────────────

def _score_emotional_arousal(text: str, vader: dict) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["emotional_arousal"]
    pos_score, pos_matched = _kw_score(text, dim["high_positive"])
    neg_score, neg_matched = _kw_score(text, dim["high_negative"])

    vader_arousal = abs(vader["compound"]) * 100

    combined = (
        max(pos_score, neg_score) * 0.45
        + vader_arousal * 0.40
        + min((pos_score + neg_score) * 0.5, 30) * 0.15
    )
    combined = min(combined * dim["weight"], 100)

    cues = pos_matched + neg_matched
    signals = list(cues)
    if vader["compound"] > 0.5:
        signals.append(f"VADER high-positive compound ({vader['compound']:.2f})")
    elif vader["compound"] < -0.3:
        signals.append(f"VADER negative compound ({vader['compound']:.2f})")

    return DimensionScore("emotional_arousal", dim["label"], dim["short"],
                          round(combined, 1), signals, dim["theory"], dim["color"], cues)


def _score_curiosity_gap(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["curiosity_gap"]
    score, matched = _kw_score(text, dim["keywords"])
    question_count = text.count("?")
    score += min(question_count * 8, 20)
    score = min(score * dim["weight"], 100)
    return DimensionScore("curiosity_gap", dim["label"], dim["short"],
                          round(score, 1), matched, dim["theory"], dim["color"], list(matched))


def _score_social_proof(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["social_proof"]
    score, matched = _kw_score(text, dim["keywords"], scale=1.2)
    # Number presence ("4 million viewers", "3 Emmy Awards") is implicit social proof
    number_signals = re.findall(r"\b\d[\d,]*\s*(million|thousand|hundred|viewers|users|fans)", text)
    score += min(len(number_signals) * 15, 30)
    # findall with one group returns the group strings ("million", "viewers"), not tuples
    signals = matched + [f"{n} count" for n in number_signals]
    score = min(score * dim["weight"], 100)
    return DimensionScore("social_proof", dim["label"], dim["short"],
                          round(score, 1), signals, dim["theory"], dim["color"], list(matched))


def _score_narrative(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["narrative_transport"]
    story_score, story_matched = _kw_score(text, dim["story_markers"])
    proto_count = len(find_keywords(text, dim["protagonist_markers"]))
    conflict_score, conflict_matched = _kw_score(text, dim["conflict_markers"])

    combined = (
        story_score * 0.50
        + min(proto_count * 15, 30) * 0.25
        + conflict_score * 0.25
    )
    combined = min(combined * dim["weight"], 100)
    cues = story_matched + conflict_matched
    signals = list(cues)
    if proto_count:
        signals.append(f"{proto_count} protagonist marker(s)")
    return DimensionScore("narrative_transport", dim["label"], dim["short"],
                          round(combined, 1), signals, dim["theory"], dim["color"], cues)


def _score_identity(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["identity_resonance"]
    sp_score, sp_matched = _kw_score(text, dim["second_person"], scale=1.5)
    asp_score, asp_matched = _kw_score(text, dim["aspirational"])
    com_score, com_matched = _kw_score(text, dim["community"])

    combined = min((sp_score * 0.5 + asp_score * 0.3 + com_score * 0.2) * dim["weight"], 100)
    signals = sp_matched + asp_matched + com_matched
    return DimensionScore("identity_resonance", dim["label"], dim["short"],
                          round(combined, 1), signals, dim["theory"], dim["color"], list(signals))


def _score_perma(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["perma_wellbeing"]
    subscores = {}
    all_signals = []
    for pillar in ["positive_emotion", "engagement_flow", "relationships", "meaning", "accomplishment"]:
        s, matched = _kw_score(text, dim[pillar])
        subscores[pillar] = s
        all_signals += matched

    breadth_bonus = sum(1 for s in subscores.values() if s > 5) * 8
    combined = min((sum(subscores.values()) / len(subscores) + breadth_bonus) * dim["weight"], 100)
    return DimensionScore("perma_wellbeing", dim["label"], dim["short"],
                          round(combined, 1), all_signals, dim["theory"], dim["color"], list(all_signals))


def _score_scarcity(text: str) -> DimensionScore:
    dim = ENGAGEMENT_DIMENSIONS["scarcity_exclusivity"]
    score, matched = _kw_score(text, dim["keywords"])
    score = min(score * dim["weight"], 100)
    return DimensionScore("scarcity_exclusivity", dim["label"], dim["short"],
                          round(score, 1), matched, dim["theory"], dim["color"], list(matched))


# ── Profile classification ────────────────────────────────────────────────────

def _classify_profile(dimensions: Dict[str, DimensionScore], dominant: List[str]) -> str:
    if not dominant:
        return "Balanced Engagement"
    top = dominant[0]
    second = dominant[1] if len(dominant) > 1 else None

    if top == "emotional_arousal" and dimensions[top].score > 55:
        return "Viral Emotion Driver"
    if top == "curiosity_gap" and dimensions[top].score > 45:
        return "Curiosity Engine"
    if top == "narrative_transport" and dimensions[top].score > 45:
        return "Narrative Immersive"
    if top == "perma_wellbeing" and second in ("identity_resonance", None):
        return "Meaning-Led Content"
    if top == "identity_resonance" and second in ("perma_wellbeing", None):
        return "Community Builder"
    if top == "social_proof" or top == "scarcity_exclusivity":
        return "Prestige Signal"
    return "Balanced Engagement"


# ── Recommendations ───────────────────────────────────────────────────────────

def _build_recommendations(dimensions: Dict[str, DimensionScore]) -> List[str]:
    recs = []
    scored = {k: v.score for k, v in dimensions.items()}

    if scored["emotional_arousal"] < 30:
        recs.append("Add high-arousal language (vivid adjectives, emotional stakes) "
                    "to increase sharing propensity.")
    if scored["curiosity_gap"] < 25:
        recs.append("Open with a provocative question or withhold key information to "
                    "create an information gap that compels engagement.")
    if scored["narrative_transport"] < 25:
        recs.append("Introduce a protagonist or story arc — even a single character's "
                    "journey gives the audience something to be transported into.")
    if scored["social_proof"] < 20:
        recs.append("Add validation signals: audience size, critical reception, or "
                    "award recognition to reduce perceived risk for new viewers.")
    if scored["perma_wellbeing"] < 20:
        recs.append("Connect content to a higher-order meaning or human outcome "
                    "(purpose, connection, growth) to increase lasting resonance.")

    if not recs:
        recs.append("Several dimensions are already active. Consider A/B testing emphasis on your "
                    "top two dimensions with a real audience.")
    return recs


# ── Main entry point ──────────────────────────────────────────────────────────

def score(text: str, label: str = "Content", content_type: str = "General") -> ContentScore:
    normalized = _norm(text)
    vader = _vader.polarity_scores(text)

    dimensions = {
        "emotional_arousal":   _score_emotional_arousal(normalized, vader),
        "curiosity_gap":       _score_curiosity_gap(normalized),
        "social_proof":        _score_social_proof(normalized),
        "narrative_transport": _score_narrative(normalized),
        "identity_resonance":  _score_identity(normalized),
        "perma_wellbeing":     _score_perma(normalized),
        "scarcity_exclusivity": _score_scarcity(normalized),
    }

    dominant = sorted(dimensions.values(), key=lambda d: d.score, reverse=True)
    dominant_ids = [d.dimension_id for d in dominant[:3] if d.score > 10]

    # Overall score: mean of the top-3 dimensions. This is a design choice, not an empirical
    # finding: most texts lean on two or three mechanisms and score 0 on the rest, so averaging
    # all seven would mostly measure how many dimensions a text ignores.
    top3_scores = sorted([d.score for d in dimensions.values()], reverse=True)[:3]
    overall = min(sum(top3_scores) / 3, 100)

    profile_type = _classify_profile(dimensions, dominant_ids)
    recs = _build_recommendations(dimensions)

    return ContentScore(
        text=text,
        label=label,
        content_type=content_type,
        dimensions=dimensions,
        overall_score=round(overall, 1),
        profile_type=profile_type,
        dominant_dimensions=dominant_ids,
        recommendations=recs,
        vader_scores=vader,
        word_count=len(normalized.split()),
    )


def score_batch(samples: dict) -> list:
    return [
        score(text, label=label, content_type=meta.get("content_type", "General"))
        for label, meta in samples.items()
        for text in [meta["text"]]
    ]
