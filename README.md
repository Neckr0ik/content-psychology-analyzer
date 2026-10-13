# Content Psychology Analyzer

> **Resumen:** Califica textos de medios (sinopsis, titulares, posts) en siete dimensiones psicológicas de enganche, cada una ligada a una teoría publicada, y compara dos redacciones del mismo mensaje para mostrar qué consideraciones enfatiza cada una (teoría del encuadre de Chong y Druckman, 2007). Es una heurística transparente basada en palabras clave: describe el texto, no mide ni predice la respuesta del público.

*Part of Giovanni Oliveira's Hybrid Intelligence portfolio — see https://github.com/Neckr0ik*

**Core question:** which psychological mechanisms does a piece of media copy lean on, and how does a rewrite change that emphasis?

The tool scores text on seven engagement dimensions. Each one is grounded in a published theory and turned into explicit text cues (keywords, VADER tone, questions, audience numbers). From the scores it assigns a profile type and suggests edits. It can also **compare two wordings of the same message** and report which dimensions differ: a public, heuristic relative of message testing.

---

## Sample output

Real output of `python main.py --no-charts` (excerpt):

```
  Thriller Drama (OTT)  [Streaming Series]
  [########            ] 41/100  |  Prestige Signal
  Top dimensions: Social:65 | Arousal:30 | Narrative:28

  LinkedIn Resilience Post  [Social Media (Professional)]
  [##########          ] 55/100  |  Community Builder
  Top dimensions: Identity:74 | PERMA:54 | Arousal:35

  Late Night Talk Show  [Entertainment / Talk]
  [############        ] 63/100  |  Curiosity Engine
```

Framing comparison, `python main.py --framing-demo` (excerpt):

```
[Streaming series launch]
  Dimension                    A     B    B-A
  Scarcity / Exclusivity       0    75    +75  <- differs
  Social Proof                 0    52    +52  <- differs
  Curiosity Gap                0    49    +49  <- differs
  PERMA Wellbeing             16     0    -16  <- differs
  ...
  Findings:
    - Scarcity / Exclusivity: B emphasises this more than A by 75 pts (cues only in B: limited series, premiere, only, world premiere). [Prospect Theory — Kahneman & Tversky (1979)]
    - Social Proof: B emphasises this more than A by 52 pts (cues only in B: award, everyone is talking, series). ...
```

The scores show cue density on a 0–100 scale. They are not predicted engagement rates.

---

## The seven dimensions

| Dimension | Theoretical basis | Text cues used |
|:---|:---|:---|
| **Emotional Arousal** | Russell (1980) circumplex; arousal and sharing in Berger & Milkman (2012) | High-arousal words + VADER compound magnitude |
| **Curiosity Gap** | Loewenstein (1994) information-gap theory | Teaser phrases, questions |
| **Social Proof** | Cialdini (1984) | Awards, acclaim, audience numbers ("4 million viewers") |
| **Narrative Transport** | Green & Brock (2000) | Story markers, protagonists, conflict words |
| **Identity Resonance** | Markus & Wurf (1987) self-concept | Second person, aspirational and community language |
| **PERMA Wellbeing** | Seligman (2011) | Words for the five PERMA pillars, plus a bonus for covering several |
| **Scarcity / Exclusivity** | Kahneman & Tversky (1979) loss aversion | Premiere, exclusive, limited, first look |

Keywords match as **whole words or phrases**, so "us" does not match "because" and "hit" does not match "white".

## Profile types

| Profile | Rule (on the scores above) |
|:---|:---|
| Viral Emotion Driver | Arousal is the top dimension and > 55 |
| Curiosity Engine | Curiosity Gap is top and > 45 |
| Narrative Immersive | Narrative Transport is top and > 45 |
| Meaning-Led Content | PERMA top, Identity second |
| Community Builder | Identity top, PERMA second |
| Prestige Signal | Social Proof or Scarcity is top |
| Balanced Engagement | none of the above |

The profile names are labels for score patterns. They are not validated audience segments.

---

## Message-framing comparison

Chong & Druckman (2007) define a frame by the **considerations a message emphasises**. Two wordings of the same facts can make different considerations salient and so change how people weigh an issue. `--compare` treats each dimension as one family of considerations and reports:

- **Dimensions that differ** by at least `--threshold` points (default 10), with the cues found only in A or only in B.
- **Tone difference** (VADER compound), when it is at least 0.25.
- **Gain vs. loss wording** (an *equivalency* frame): "protects you" vs. "you risk missing". Tversky & Kahneman (1981) showed that this kind of wording can shift choices.

```bash
python main.py --compare \
  "Getting your flu shot protects you and your family." \
  "If you skip your flu shot, you risk missing work. Don't wait until it's too late."
```

The command writes `output/framing_report.md` and an overlaid radar chart, `output/framing_comparison.png`. Use it as a structured checklist for editors or to form hypotheses. Whether a framing works better can only be learned by testing it with real audiences.

---

## Install, run, test

```bash
git clone https://github.com/Neckr0ik/content-psychology-analyzer.git
cd content-psychology-analyzer
pip install -r requirements.txt

python main.py                                   # 8 bundled samples -> charts + report in output/
python main.py --text "Your synopsis" --type "OTT Series"
python main.py --compare "Wording A" "Wording B" # framing comparison
python main.py --framing-demo                    # bundled framing pairs
python main.py --no-charts                       # skip PNGs

pytest -q                                        # offline test suite
```

Python 3.11+. CI runs the tests on Python 3.11 and 3.12 (`.github/workflows/tests.yml`).

## Architecture

```
content-psychology-analyzer/
├── main.py            # CLI: batch, single text, --compare, --framing-demo
├── src/
│   ├── frameworks.py  # dimensions, theory citations, keyword lists, profile types
│   ├── scorer.py      # whole-word matching, per-dimension scoring, profiles, recommendations
│   ├── framing.py     # two-wording comparison (emphasis + gain/loss frames)
│   ├── reporter.py    # radar/bar/ranking charts, markdown reports
│   └── samples.py     # illustrative sample texts and framing pairs (fictional)
└── tests/
```

## Limitations

- **A heuristic, not a measurement.** Scores count cues in the wording, using hand-picked keyword lists, fixed weights and VADER. They have not been calibrated against engagement data and do not predict views, clicks or sharing.
- **English only.** The keyword lists and VADER assume English text.
- **No context.** Sarcasm, negation ("not exclusive"), visuals, audio, brand and placement are all ignored.
- **The weights and thresholds are design choices.** These include the ×400 coverage scale, the dimension weights and the profile cut-offs. Change them in `src/frameworks.py` and `src/scorer.py` to fit your own data.
- **The sample texts are fictional.** Any figures inside them (for example "98% of families") are part of the made-up copy, not real statistics.

## References

- Berger, J. & Milkman, K. L. (2012). What makes online content viral? *Journal of Marketing Research, 49*(2), 192–205.
- Chong, D. & Druckman, J. N. (2007). Framing theory. *Annual Review of Political Science, 10*, 103–126.
- Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion.* William Morrow.
- Green, M. C. & Brock, T. C. (2000). The role of transportation in the persuasiveness of public narratives. *Journal of Personality and Social Psychology, 79*(5), 701–721.
- Kahneman, D. & Tversky, A. (1979). Prospect theory. *Econometrica, 47*(2), 263–291.
- Loewenstein, G. (1994). The psychology of curiosity. *Psychological Bulletin, 116*(1), 75–98.
- Markus, H. & Wurf, E. (1987). The dynamic self-concept. *Annual Review of Psychology, 38*, 299–337.
- Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology, 39*(6), 1161–1178.
- Seligman, M. E. P. (2011). *Flourish.* Free Press.
- Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science, 211*(4481), 453–458.

## License

MIT © 2026 Giovanni Oliveira
