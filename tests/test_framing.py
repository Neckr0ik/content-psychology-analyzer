from src.framing import compare, gain_loss_cues, gain_loss_orientation, CAVEAT
from src.samples import FRAMING_PAIRS


def test_identical_wordings_have_no_differences():
    text = "A new drama series premieres Friday."
    cmp = compare(text, text)
    assert cmp.differing == []
    assert all(d.delta == 0 for d in cmp.deltas.values())
    assert "similar mix" in cmp.findings[0]


def test_detects_added_emphasis_and_reports_cues():
    a, b = FRAMING_PAIRS["Streaming series launch"]
    cmp = compare(a, b)
    ids = [d.dimension_id for d in cmp.differing]
    assert ids[0] == "scarcity_exclusivity"
    assert {"social_proof", "curiosity_gap"} <= set(ids)
    scarcity = cmp.deltas["scarcity_exclusivity"]
    assert scarcity.delta > 0 and "premiere" in scarcity.only_in_b and scarcity.only_in_a == []


def test_delta_sign_convention():
    cmp = compare("Exclusive world premiere, limited series.", "A drama.")
    assert cmp.deltas["scarcity_exclusivity"].delta < 0  # B - A


def test_gain_vs_loss_frame():
    a, b = FRAMING_PAIRS["Vaccination reminder"]
    cmp = compare(a, b)
    assert (cmp.frame_a, cmp.frame_b) == ("gain", "loss")
    assert any("Tversky & Kahneman" in f for f in cmp.findings)
    assert cmp.valence_delta < 0


def test_gain_loss_orientation():
    assert gain_loss_orientation(gain_loss_cues("Nothing here.")) == "none"
    assert gain_loss_orientation(gain_loss_cues("Save money but risk delays")) == "mixed"
    assert gain_loss_orientation(gain_loss_cues("Don't miss out or you'll lose")) == "loss"


def test_threshold_controls_sensitivity():
    a, b = FRAMING_PAIRS["Vaccination reminder"]
    assert len(compare(a, b, threshold=100).differing) == 0
    assert len(compare(a, b, threshold=1).differing) >= len(compare(a, b).differing)


def test_caveat_is_honest():
    assert "does not measure or predict" in CAVEAT


def test_numeric_signals_are_not_reported_as_cues():
    # both versions trigger a VADER signal with different numbers; that is not a wording cue
    cmp = compare("An amazing, wonderful triumph!", "An amazing, wonderful, brilliant triumph!")
    arousal = cmp.deltas["emotional_arousal"]
    assert not any("VADER" in c for c in arousal.only_in_a + arousal.only_in_b)
    cmp = compare("She left.", "She said he and they knew his secret, but her plan failed.")
    narr = cmp.deltas["narrative_transport"]
    assert not any("marker" in c for c in narr.only_in_a + narr.only_in_b)
