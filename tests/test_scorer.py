import pytest

from src.frameworks import ENGAGEMENT_DIMENSIONS, CONTENT_PROFILE_TYPES
from src.samples import SAMPLES
from src.scorer import find_keywords, score, score_batch


def test_whole_word_matching_avoids_substring_false_positives():
    # "white" contains "hit", "because"/"bus" contain "us", "the" contains "he"
    assert find_keywords("a white cat because the bus is late", ["hit", "us", "he"]) == []
    assert find_keywords("a hit show for us", ["hit", "us"]) == ["hit", "us"]


def test_phrases_and_special_tokens():
    assert find_keywords("the #1 show. you won't believe it", ["#1", "you won't believe"]) == ["#1", "you won't believe"]
    assert find_keywords("nominated for an emmy", ["Emmy"]) == ["emmy"]


def test_neutral_text_scores_low():
    r = score("This is a white cat because the bus is late.")
    assert all(d.score < 10 for d in r.dimensions.values())
    assert r.profile_type == "Balanced Engagement"


def test_scores_are_bounded_and_complete():
    for r in score_batch(SAMPLES):
        assert set(r.dimensions) == set(ENGAGEMENT_DIMENSIONS)
        assert 0 <= r.overall_score <= 100
        assert all(0 <= d.score <= 100 for d in r.dimensions.values())
        assert r.profile_type in CONTENT_PROFILE_TYPES
        assert r.recommendations


@pytest.mark.parametrize("dim,text", [
    ("curiosity_gap", "What really happened? The secret behind the untold mystery, revealed."),
    ("social_proof", "The award-winning, critically acclaimed hit loved by 4 million viewers."),
    ("scarcity_exclusivity", "World premiere: an exclusive first look, limited series, early access."),
])
def test_dimension_responds_to_its_cues(dim, text):
    r = score(text)
    assert r.dimensions[dim].score >= 40
    assert r.dimensions[dim].score == max(d.score for d in r.dimensions.values())


def test_deterministic():
    text = SAMPLES["News Headline"]["text"]
    assert score(text).overall_score == score(text).overall_score


def test_audience_number_signal_names_the_unit():
    r = score("Loved by 4 million viewers and 300 thousand fans.")
    sigs = r.dimensions["social_proof"].signals
    assert "million count" in sigs and "thousand count" in sigs
    assert "m count" not in sigs and "t count" not in sigs


def test_curly_quotes_and_nfkc_are_normalised():
    straight = score("You won't believe what happened.")
    curly = score("You won’t believe what happened.")
    assert "you won't believe" in curly.dimensions["curiosity_gap"].cues
    assert curly.dimensions["curiosity_gap"].score == straight.dimensions["curiosity_gap"].score
    fullwidth = score("Ｅｘｃｌｕｓｉｖｅ premiere")  # "Exclusive"
    assert "exclusive" in fullwidth.dimensions["scarcity_exclusivity"].cues


def test_cues_exclude_derived_signals():
    r = score("Loved by 4 million viewers. An amazing, thrilling hero's journey!")
    for d in r.dimensions.values():
        assert not any("VADER" in c or "count" in c or "marker" in c for c in d.cues)
