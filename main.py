"""
Content Psychology Analyzer
Run:  python main.py
Run on custom text:  python main.py --text "Your content here" --type "OTT Series"

Scores media content across seven psychological engagement dimensions,
classifies engagement profile type, and generates actionable recommendations
for content strategists, OTT platforms, and media teams.
"""

import argparse
from src.samples import SAMPLES
from src.scorer import score, score_batch
from src.reporter import plot_radar, plot_dimension_bars, plot_ranking, write_report
from src.frameworks import ENGAGEMENT_DIMENSIONS, CONTENT_PROFILE_TYPES


def print_result(result):
    bar = "[" + "#" * int(result.overall_score / 5) + " " * (20 - int(result.overall_score / 5)) + "]"
    print(f"\n  {result.label}  [{result.content_type}]")
    print(f"  {bar} {result.overall_score:.0f}/100  |  {result.profile_type}")

    dims_sorted = sorted(result.dimensions.values(), key=lambda d: d.score, reverse=True)
    top3 = [f"{d.short}:{d.score:.0f}" for d in dims_sorted[:3]]
    print(f"  Top dimensions: {' | '.join(top3)}")

    if result.recommendations:
        print(f"  Tip: {result.recommendations[0][:90]}")


def main():
    parser = argparse.ArgumentParser(description="Content Psychology Analyzer")
    parser.add_argument("--text", "-t", type=str, help="Analyze a custom text string")
    parser.add_argument("--type", type=str, default="General", help="Content type label")
    parser.add_argument("--no-charts", action="store_true", help="Skip chart generation")
    args = parser.parse_args()

    print("Content Psychology Analyzer")
    print("=" * 65)
    print("Psychological engagement scoring for media and content strategy")
    print("=" * 65)

    if args.text:
        result = score(args.text, label="Custom Content", content_type=args.type)
        print_result(result)
        if not args.no_charts:
            f = plot_radar(result)
            print(f"\n  Chart saved -> {f}")
        print(f"\n  Recommendations:")
        for rec in result.recommendations:
            print(f"    - {rec}")
        return

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
    print("KEY INSIGHT")
    print("-" * 65)
    print("High-performing OTT content typically stacks 3+ dimensions above 40.")
    print("The most shareable content (news, social posts) relies on Emotional")
    print("Arousal + Curiosity Gap, while content that builds loyal audiences")
    print("(limited series, documentaries) prioritizes Narrative Transport and")
    print("PERMA Wellbeing — aligning with what viewers return for, not just click.")
    print()
    print("All charts and report saved to output/")
    print()
    print("TIP: Run  python main.py --text 'your content' --type 'OTT'  to score custom content.")


if __name__ == "__main__":
    main()
