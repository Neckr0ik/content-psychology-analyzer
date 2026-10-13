"""
Message-framing comparison: score two wordings of the same message and report
which engagement dimensions differ between them.

Theory
------
Chong & Druckman (2007) define a frame as the set of considerations a message
emphasises. "Emphasis frames" change which considerations are salient, and so can
change how an audience weighs an issue, even when the underlying facts are the same.
This module treats each engagement dimension as one family of considerations and
asks: does wording B emphasise a different mix than wording A?

It also flags *equivalency* (gain vs. loss) framing. Tversky & Kahneman (1981)
showed that describing the same outcome as a gain or as a loss can reverse choices.

What this is NOT
----------------
A heuristic, keyword-based description of the text. It does not predict or measure
how any audience will respond. Treat the output as a checklist for human review or
as hypotheses to test with real audiences.

References
- Chong, D. & Druckman, J. N. (2007). Framing theory. Annual Review of Political Science, 10, 103-126.
- Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. Science, 211(4481), 453-458.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .scorer import ContentScore, find_keywords, score, _norm

DEFAULT_THRESHOLD = 10.0   # points (0-100 scale) before a dimension counts as "different"
VALENCE_THRESHOLD = 0.25   # VADER compound difference before tone counts as "different"

GAIN_CUES = ["gain", "gains", "save", "saves", "saving", "protect", "protects", "benefit",
             "benefits", "win", "wins", "keep", "earn", "improve", "improves", "healthier",
             "safer", "grow", "more time", "peace of mind"]
LOSS_CUES = ["lose", "loses", "losing", "loss", "losses", "risk", "risks", "miss", "miss out",
             "cost", "costs", "fail", "fails", "danger", "penalty", "waste", "wasting", "fall behind",
             "too late", "regret"]

CAVEAT = ("Heuristic comparison of wording (keyword and lexicon signals). It describes which "
          "considerations each version emphasises; it does not measure or predict audience response.")


@dataclass
class DimensionDelta:
    dimension_id: str
    label: str
    theory: str
    score_a: float
    score_b: float
    only_in_a: List[str]
    only_in_b: List[str]

    @property
    def delta(self) -> float:
        """Positive = version B emphasises this dimension more."""
        return round(self.score_b - self.score_a, 1)


@dataclass
class FramingComparison:
    label_a: str
    label_b: str
    result_a: ContentScore
    result_b: ContentScore
    deltas: Dict[str, DimensionDelta]
    threshold: float
    gain_loss_a: Dict[str, List[str]]
    gain_loss_b: Dict[str, List[str]]
    findings: List[str] = field(default_factory=list)

    @property
    def differing(self) -> List[DimensionDelta]:
        """Dimensions whose scores differ by at least `threshold`, largest gap first."""
        diffs = [d for d in self.deltas.values() if abs(d.delta) >= self.threshold]
        return sorted(diffs, key=lambda d: abs(d.delta), reverse=True)

    @property
    def valence_delta(self) -> float:
        return round(self.result_b.vader_scores["compound"] - self.result_a.vader_scores["compound"], 3)

    @property
    def frame_a(self) -> str:
        return gain_loss_orientation(self.gain_loss_a)

    @property
    def frame_b(self) -> str:
        return gain_loss_orientation(self.gain_loss_b)


def gain_loss_cues(text: str) -> Dict[str, List[str]]:
    norm = _norm(text)
    return {"gain": find_keywords(norm, GAIN_CUES), "loss": find_keywords(norm, LOSS_CUES)}


def gain_loss_orientation(cues: Dict[str, List[str]]) -> str:
    g, l = len(cues["gain"]), len(cues["loss"])
    if g == l == 0:
        return "none"
    if g > l:
        return "gain"
    if l > g:
        return "loss"
    return "mixed"


def _findings(cmp: FramingComparison) -> List[str]:
    out: List[str] = []
    for d in cmp.differing:
        stronger, weaker = (cmp.label_b, cmp.label_a) if d.delta > 0 else (cmp.label_a, cmp.label_b)
        cues = d.only_in_b if d.delta > 0 else d.only_in_a
        cue_txt = (f" (cues only in {stronger}: {', '.join(cues[:5])})" if cues
                   else " (no keyword cue differs; the gap comes from tone, question or count signals)")
        out.append(f"{d.label}: {stronger} emphasises this more than {weaker} "
                   f"by {abs(d.delta):.0f} pts{cue_txt}. [{d.theory}]")
    if abs(cmp.valence_delta) >= VALENCE_THRESHOLD:
        more = cmp.label_b if cmp.valence_delta > 0 else cmp.label_a
        out.append(f"Tone: {more} reads as more positive (VADER compound difference "
                   f"{abs(cmp.valence_delta):.2f}).")
    if cmp.frame_a != cmp.frame_b and "none" not in (cmp.frame_a, cmp.frame_b):
        out.append(f"Equivalency frame: {cmp.label_a} leans {cmp.frame_a}, {cmp.label_b} leans "
                   f"{cmp.frame_b}. Gain vs. loss wording of the same outcome can shift choices "
                   "(Tversky & Kahneman, 1981).")
    elif cmp.frame_a != cmp.frame_b:
        framed = cmp.label_a if cmp.frame_a != "none" else cmp.label_b
        frame = cmp.frame_a if cmp.frame_a != "none" else cmp.frame_b
        out.append(f"Equivalency frame: only {framed} uses explicit {frame} wording.")
    if not out:
        out.append(f"No dimension differs by {cmp.threshold:.0f}+ pts: the two wordings emphasise "
                   "a similar mix of considerations.")
    return out


def compare(text_a: str, text_b: str, label_a: str = "Version A", label_b: str = "Version B",
            content_type: str = "General", threshold: float = DEFAULT_THRESHOLD) -> FramingComparison:
    """Score both wordings and describe how their emphasis differs."""
    a = score(text_a, label=label_a, content_type=content_type)
    b = score(text_b, label=label_b, content_type=content_type)

    deltas: Dict[str, DimensionDelta] = {}
    for dim_id, da in a.dimensions.items():
        db = b.dimensions[dim_id]
        # compare matched keyword cues only; derived signals such as "VADER ... (0.62)" or
        # "2 protagonist marker(s)" differ in their numbers and would show up as false "cues"
        sig_a, sig_b = da.cues, db.cues
        deltas[dim_id] = DimensionDelta(
            dimension_id=dim_id, label=da.label, theory=da.theory,
            score_a=da.score, score_b=db.score,
            only_in_a=[s for s in sig_a if s not in sig_b],
            only_in_b=[s for s in sig_b if s not in sig_a],
        )

    cmp = FramingComparison(label_a=label_a, label_b=label_b, result_a=a, result_b=b,
                            deltas=deltas, threshold=threshold,
                            gain_loss_a=gain_loss_cues(text_a), gain_loss_b=gain_loss_cues(text_b))
    cmp.findings = _findings(cmp)
    return cmp
