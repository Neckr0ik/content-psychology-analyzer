# Content Psychology Analyzer

**Core question:** Why does some content captivate audiences while identical content is ignored — and can we measure it before publishing?

This tool scores media content across seven psychological engagement dimensions grounded in peer-reviewed research. It classifies content into engagement profile types and generates strategic recommendations for OTT platforms, content teams, and media strategists.

---

## Sample output

```
Content Psychology Analyzer
=================================================================

  Thriller Drama (OTT)  [Streaming Series]
  [###############     ] 72/100  |  Viral Emotion Driver
  Top dimensions: Arousal:74 | Social:61 | Curiosity:48
  Tip: Add a protagonist journey or story arc to increase narrative transport.

  LinkedIn Resilience Post  [Social Media (Professional)]
  [#############       ] 66/100  |  Meaning-Led Content
  Top dimensions: PERMA:71 | Identity:68 | Narrative:55

  Late Night Talk Show  [Entertainment / Talk]
  [###########         ] 55/100  |  Curiosity Engine
  Top dimensions: Curiosity:65 | Social:42 | Arousal:38
```

---

## The seven dimensions of psychological engagement

Content does not succeed because it is "good." It succeeds because it activates specific psychological mechanisms that evolved to capture and hold human attention.

| Dimension | Theoretical Basis | What It Measures |
|:---|:---|:---|
| **Emotional Arousal** | Russell's Circumplex Model (1980) | High-activation emotion — the primary predictor of sharing behavior |
| **Curiosity Gap** | Loewenstein's Information Gap Theory (1994) | Partial information creating aversive uncertainty that compels engagement |
| **Social Proof** | Cialdini's Principles of Influence (1984) | Signals of others' engagement reducing the perceived risk of viewing |
| **Narrative Transport** | Green & Brock Transportation Model (2000) | Story structure activating multi-region brain engagement and recall |
| **Identity Resonance** | Self-Concept Theory (Markus & Wurf, 1987) | Content mirroring the audience's existing or aspirational self-concept |
| **PERMA Wellbeing** | Seligman's PERMA Model (2011) | Alignment with the five pillars of human flourishing |
| **Scarcity / Exclusivity** | Prospect Theory (Kahneman & Tversky, 1979) | Benign scarcity signals elevating perceived content value |

---

## Engagement profile types

The analyzer classifies each content piece into one of seven strategic profiles:

| Profile Type | Dominant Signal | Typical Context |
|:---|:---|:---|
| **Viral Emotion Driver** | Emotional Arousal > 55 | News, social clips, trailers |
| **Curiosity Engine** | Curiosity Gap > 45 | Headlines, teasers, episodic TV |
| **Narrative Immersive** | Narrative Transport > 45 | Prestige drama, documentary |
| **Community Builder** | Identity Resonance + PERMA | Reality TV, lifestyle brands |
| **Prestige Signal** | Social Proof + Scarcity | Awards content, limited series |
| **Meaning-Led Content** | PERMA Meaning + Identity | LinkedIn, purpose-driven brands |
| **Balanced Engagement** | No dominant dimension | Broad-appeal content |

*High-performing OTT content typically stacks 3+ dimensions above 40. The most shareable content relies on Arousal + Curiosity Gap, while content that builds loyal audiences prioritizes Narrative Transport and PERMA Wellbeing.*

---

## Quick start

```bash
git clone https://github.com/Neckr0ik/content-psychology-analyzer.git
cd content-psychology-analyzer
pip install -r requirements.txt
python main.py
```

Analyze your own content:

```bash
python main.py --text "Your series description or headline" --type "OTT Series"
```

Runtime: ~4 seconds for the full 8-sample batch.

---

## Architecture

```
content-psychology-analyzer/
├── main.py               # CLI entry point, batch runner
├── src/
│   ├── frameworks.py     # 7 psychological dimensions + theory citations + engagement profiles
│   ├── scorer.py         # Per-dimension scoring + profile classification + recommendations
│   ├── reporter.py       # Radar charts, dimension bars, ranking chart, markdown report
│   └── samples.py        # 8 content samples: OTT, news, LinkedIn, kids, sports, marketing
└── output/               # Generated charts and report (git-ignored)
```

---

## Scoring methodology

Each dimension has a custom scorer reflecting the specific mechanism it measures:

```python
# Emotional Arousal: VADER + keyword lexicon
arousal = keyword_score * 0.45 + abs(vader_compound) * 100 * 0.40 + blend * 0.15

# Social Proof: keywords + number detection (e.g., "4 million viewers")
social = keyword_score + min(numeric_signals * 15, 30)

# Narrative Transport: story markers + protagonist presence + conflict density
narrative = story_score * 0.50 + protagonist_count * 0.25 + conflict_score * 0.25

# PERMA: scores all 5 pillars independently + breadth bonus for multi-pillar content
perma = avg(P, E, R, M, A) + active_pillar_count * 8
```

---

## Output charts

| Chart | Description |
|---|---|
| `radar_*.png` | Per-content radar chart across all 7 dimensions |
| `dimensions_comparison.png` | Grouped bar chart: all samples × all dimensions |
| `engagement_ranking.png` | Horizontal bar chart ranking by overall engagement score |
| `analysis_report.md` | Full report with dimension scores, profile types, and recommendations |

---

## Industry context

This tool operationalizes the content strategy decisions that media executives make intuitively after years of experience. By formalizing the psychological mechanisms into measurable signals, it enables:

- **Pre-publish scoring** to forecast engagement before commissioning or releasing content
- **Competitive analysis** by scoring competitor content against the same dimensions
- **A/B testing guidance** by identifying which psychological dimensions a title or description is underserving
- **Genre benchmarking** to understand what psychological profile different content categories tend toward

---

## References

- Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology, 39*(6).
- Loewenstein, G. (1994). The psychology of curiosity. *Psychological Bulletin, 116*(1), 75–98.
- Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion.* Harper Business.
- Green, M. C. & Brock, T. C. (2000). The role of transportation. *Journal of Personality and Social Psychology, 79*(5).
- Markus, H. & Wurf, E. (1987). The dynamic self-concept. *Annual Review of Psychology, 38*.
- Seligman, M. E. P. (2011). *Flourish.* Free Press.
- Kahneman, D. & Tversky, A. (1979). Prospect Theory. *Econometrica, 47*(2), 263–291.

---

## Skills demonstrated

`Python` · `Applied Psychology` · `Content Strategy` · `OTT/Media Analytics` · `NLP (VADER)` · `Positive Psychology (PERMA)` · `Behavioral Science` · `Matplotlib` · `Data Visualization`

---

## License

MIT © 2026 Giovanni Oliveira
