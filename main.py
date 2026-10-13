"""
Content Psychology Analyzer
Run:  python main.py
Run on custom text:  python main.py --text "Your content here" --type "OTT Series"
Compare two wordings: python main.py --compare "Wording A" "Wording B"
Framing demo:         python main.py --framing-demo

Scores media content across seven psychological engagement dimensions with
transparent keyword/lexicon heuristics, classifies an engagement profile, and
suggests edits. It describes the text; it does not measure audience response.
"""

import argparse
import sys
import textwrap

from src.samples import SAMPLES, FRAMING_PAIRS
from src.scorer import score, score_batch
from src.framing import compare, CAVEAT
from src.reporter import (plot_radar, plot_dimension_bars, plot_ranking, write_report,
                          plot_framing_radar, write_framing_report)
from src.frameworks import CONTENT_PROFILE_TYPES


def print_result(result):
    bar = "[" + "#" * int(result.overall_score / 5) + " " * (20 - int(result.overall_score / 5)) + "]"
    print(f"\n  {result.label}  [{result.content_type}]")
    print(f"  {bar} {result.overall_score:.0f}/100  |  {result.profile_type}")

    dims_sorted = sorted(result.dimensions.values(), key=lambda d: d.score, reverse=True)
    top3 = [f"{d.short}:{d.score:.0f}" for d in dims_sorted[:3]]
    print(f"  Top dimensions: {' | '.join(top3)}")

    if result.recommendations:
        print(f"  Tip: {textwrap.shorten(result.recommendations[0], 90, placeholder='...')}")


def print_comparison(cmp):
    print(f"\n  {cmp.label_a}: {cmp.result_a.text[:90]}")
    print(f"  {cmp.label_b}: {cmp.result_b.text[:90]}")
    print(f"\n  {'Dimension':<24}{'A':>6}{'B':>6}{'B-A':>7}")
    for d in sorted(cmp.deltas.values(), key=lambda x: abs(x.delta), reverse=True):
        flag = "  <- differs" if abs(d.delta) >= cmp.threshold else ""
        print(f"  {d.label:<24}{d.score_a:>6.0f}{d.score_b:>6.0f}{d.delta:>+7.0f}{flag}")
    print("\n  Findings:")
    for f in cmp.findings:
        print(f"    - {f}")


def run_comparisons(pairs, content_type, threshold, charts):
    for i, (name, (a, b)) in enumerate(pairs.items(), 1):
        print(f"\n[{name}]")
        cmp = compare(a, b, label_a="A", label_b="B", content_type=content_type, threshold=threshold)
        print_comparison(cmp)
        suffix = "" if len(pairs) == 1 else f"_{i}"
        if charts:
            print(f"\n  Chart  -> {plot_framing_radar(cmp, f'output/framing_comparison{suffix}.png')}")
        print(f"  Report -> {write_framing_report(cmp, f'output/framing_report{suffix}.md')}")
    print(f"\nNote: {CAVEAT}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Content Psychology Analyzer")
    parser.add_argument("--text", "-t", type=str, help="Analyze a custom text string")
    parser.add_argument("--type", type=str, default="General", help="Content type label")
    parser.add_argument("--compare", nargs=2, metavar=("TEXT_A", "TEXT_B"),
                        help="Compare two wordings of the same message (framing comparison)")
    parser.add_argument("--framing-demo", action="store_true", help="Run the bundled framing pairs")
    parser.add_argument("--threshold", type=float, default=10.0,
                        help="Points of difference for a dimension to count as different (default 10)")
    parser.add_argument("--no-charts", action="store_true", help="Skip chart generation")
    args = parser.parse_args(argv)

    print("Content Psychology Analyzer")
    print("=" * 65)
    print("Heuristic psychological-engagement scoring for media content")
    print("=" * 65)

    if args.compare or args.framing_demo:
        pairs = {"Custom comparison": tuple(args.compare)} if args.compare else FRAMING_PAIRS
        run_comparisons(pairs, args.type, args.threshold, charts=not args.no_charts)
        return 0

    if args.text:
        result = score(args.text, label="Custom Content", content_type=args.type)
        print_result(result)
        if not args.no_charts:
            f = plot_radar(result)
            print(f"\n  Chart saved -> {f}")
        print(f"\n  Recommendations:")
        for rec in result.recommendations:
            print(f"    - {rec}")
        return 0

    print("\n[1/3] Scoring content samples across 7 dimensions...")
    results = score_batch(SAMPLES)

    print()
    for result in results:
        print_result(result)

    if not args.no_charts:
        print("\n[2/3] Generating visualizations...")
        for result in results:
            plot_radar(result)
        dim_f  = plot_dimension_bars(results)
        rank_f = plot_ranking(results)
        print(f"  Dimension bars  -> {dim_f}")
        print(f"  Ranking chart   -> {rank_f}")

    print("\n[3/3] Writing report...")
    report_f = write_report(results)
    print(f"  Markdown report -> {report_f}")

    print()
    print("=" * 65)
    print("ENGAGEMENT PROFILE DISTRIBUTION")
    print("=" * 65)
    profiles = {}
    for r in results:
        profiles[r.profile_type] = profiles.get(r.profile_type, 0) + 1
    for profile, count in sorted(profiles.items(), key=lambda x: -x[1]):
        desc = CONTENT_PROFILE_TYPES.get(profile, "")
        print(f"  {profile}: {count}")
        if desc:
            print(f"    {desc}")

    print()
    print("HOW TO READ THIS")
    print("-" * 65)
    print("Scores count theory-linked cues in the wording (keywords, VADER tone,")
    print("questions, numbers). They show which mechanisms a text leans on, not")
    print("how an audience will respond. Validate with real audience data.")
    print()
    print("All charts and report saved to output/")
    print()
    print("TIP: python main.py --text 'your content' --type 'OTT'   score custom content")
    print("     python main.py --compare 'wording A' 'wording B'    compare two framings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
