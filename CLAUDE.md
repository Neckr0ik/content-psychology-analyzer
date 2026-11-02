# CLAUDE.md — content-psychology-analyzer

Portfolio project (Neckr0ik / Giovanni Oliveira, "Hybrid Intelligence" portfolio). Scores media copy (synopses, headlines, posts) on 7 engagement dimensions, each tied to a published theory (arousal, curiosity gap, social proof, narrative transport, identity, PERMA, scarcity), assigns a profile type, suggests edits, and **compares two wordings** of the same message (Chong & Druckman framing, gain vs. loss wording). Transparent keyword heuristic: describes the text, does not predict engagement.

## Stack

Python 3.11+, vaderSentiment, matplotlib, numpy, pytest (`requirements.txt`). English only. No API keys, no network.

## Structure

```
main.py             # CLI: batch, --text/--type, --compare A B, --framing-demo, --threshold, --no-charts
src/frameworks.py   # dimensions, theory citations, keyword lists, profile types
src/scorer.py       # whole-word matching, per-dimension scores, profiles, recommendations
src/framing.py      # two-wording comparison (emphasis differences, tone, gain/loss frame)
src/reporter.py     # radar/bar/ranking charts, markdown reports
src/samples.py      # fictional sample texts and framing pairs
tests/              # test_scorer.py, test_framing.py, test_cli.py
```

## Commands

```bash
pip install -r requirements.txt
python main.py                                   # 8 samples -> charts + report in output/
python main.py --text "Your synopsis" --type "OTT Series"
python main.py --compare "Wording A" "Wording B" # writes output/framing_report.md + framing_comparison.png
python main.py --framing-demo                    # bundled framing pairs
python main.py --compare "A" "B" --threshold 15  # min point difference to report (default 10)
python main.py --no-charts
pytest -q                                        # 22 tests, offline
```

## Gotchas

- Overall score = mean of the 3 highest dimensions (design choice). Profile rules are evaluated in README order, first match wins; only dimensions > 10 count as "top"/"second".
- Keywords match as whole words/phrases after NFKC normalisation and curly-quote folding ("us" ≠ "because").
- `--compare` lists only **keyword** cues found in A or B; derived signals (VADER tone, audience-number counts) affect scores but are not listed as cues.
- No negation/sarcasm handling ("not exclusive" still counts as scarcity) — documented limitation.
- Weights, the ×400 coverage scale and profile cut-offs live in `src/frameworks.py` / `src/scorer.py`; keep README tables in sync.

## Conventions (shared across the owner's portfolio repos)

- Plain Python 3.11+ CLI: `main.py` (argparse) at the root, logic in `src/`, tests in `tests/`. No package build, no lint/format config.
- `pytest.ini` sets `testpaths = tests` and `pythonpath = .`, so run `pytest` from the repo root.
- CI (`.github/workflows/tests.yml`): `pip install -r requirements.txt` + `pytest -q` on Python 3.11 and 3.12, on every push and PR. Tests must stay offline (no network, no API keys).
- Generated files go to `output/` (gitignored). Never commit them.
- README is English with a Spanish `> **Resumen:**` blurb at the top; it documents formulas and limitations precisely. When you change behaviour, update the README in the same change (tests often pin the documented formulas).
- Be honest about scope: the README's "Limitations" section is part of the product. Don't add claims the code doesn't support.

## Memoria persistente (Graphiti MCP)
Este proyecto usa el connector **Graphiti** (memoria en grafo compartida entre sesiones).
- `group_id` de este repo: `content-psychology-analyzer`. Datos del usuario y transversales: `neckr0ik-global`.
- Al empezar una tarea: busca contexto con `search_memory_facts` y `search_nodes` usando `group_ids: ["content-psychology-analyzer", "neckr0ik-global"]`.
- Al terminar algo relevante (decisión de arquitectura, convención nueva, bug resuelto y su causa, preferencia del usuario, estado de un despliegue): guárdalo con `add_memory` (`group_id: "content-psychology-analyzer"`, `source: "text"`) con un nombre descriptivo.
- Nunca guardes secretos, API keys, tokens, contraseñas ni datos personales sensibles.
- Si Graphiti no está disponible en la sesión, continúa normalmente.
