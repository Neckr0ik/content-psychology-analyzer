"""
Visualization and report generation for content psychology analysis.
"""

from __future__ import annotations
import os
import re
from datetime import datetime
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .scorer import ContentScore
from .frameworks import ENGAGEMENT_DIMENSIONS, CONTENT_PROFILE_TYPES

OUTPUT_DIR = "output"


def _ensure_dir(filename: str) -> None:
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)


# ── Per-item radar chart ──────────────────────────────────────────────────────

def plot_radar(result: ContentScore, filename: str = None) -> str:
    dims = list(result.dimensions.values())
    labels = [d.short for d in dims]
    scores = [d.score for d in dims]
    n = len(labels)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    scores_plot = scores + [scores[0]]
    angles_plot = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")

    fill_color = "#3498DB"
    ax.plot(angles_plot, scores_plot, color=fill_color, linewidth=2)
    ax.fill(angles_plot, scores_plot, color=fill_color, alpha=0.25)

    # Benchmark ring at 50 (moderate engagement)
    benchmark = [50] * n + [50]
    ax.plot(angles_plot, benchmark, color="#8B949E", linewidth=0.8,
            linestyle="--", alpha=0.5, label="50pt benchmark")

    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], color="#8B949E", fontsize=7)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#C9D1D9", fontsize=9)
    ax.grid(color="#30363D", linewidth=0.8)
    ax.spines["polar"].set_color("#30363D")

    ax.set_title(
        f"{result.label}\n"
        f"{result.content_type}  |  Overall: {result.overall_score:.0f}/100  "
        f"|  {result.profile_type}",
        color="#E6EDF3", fontsize=9, fontweight="bold", pad=20,
    )

    if filename is None:
        safe = re.sub(r"[^a-z0-9]+", "_", result.label.lower()).strip("_")[:30]
        filename = os.path.join(OUTPUT_DIR, f"radar_{safe}.png")
    _ensure_dir(filename)
    plt.tight_layout()
    plt.savefig(filename, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    return filename


# ── Grouped bar: all dimensions across all samples ────────────────────────────

def plot_dimension_bars(results: List[ContentScore], filename: str = None) -> str:
    dim_ids   = list(ENGAGEMENT_DIMENSIONS.keys())
    dim_short = [ENGAGEMENT_DIMENSIONS[d]["short"] for d in dim_ids]
    colors    = [ENGAGEMENT_DIMENSIONS[d]["color"] for d in dim_ids]
    n_dims    = len(dim_ids)
    n_items   = len(results)

    x = np.arange(n_dims)
    width = 0.8 / max(n_items, 1)

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")

    for i, result in enumerate(results):
        scores = [result.dimensions[d].score for d in dim_ids]
        offset = (i - n_items / 2 + 0.5) * width
        bars = ax.bar(x + offset, scores, width * 0.9,
                      label=result.label[:25], alpha=0.85,
                      color=[c for c in colors], edgecolor="#30363D", linewidth=0.3)

    ax.set_xticks(x)
    ax.set_xticklabels(dim_short, color="#C9D1D9", fontsize=9)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Engagement Score (0-100)", color="#8B949E", fontsize=9)
    ax.set_title("Psychological Engagement Dimensions by Content Sample",
                 color="#E6EDF3", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#8B949E")
    ax.axhline(y=50, color="#8B949E", linestyle="--", linewidth=0.8, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color("#30363D")

    ax.legend(loc="upper right", fontsize=7.5, facecolor="#161B22",
              edgecolor="#30363D", labelcolor="#C9D1D9", ncol=2)

    if filename is None:
        filename = os.path.join(OUTPUT_DIR, "dimensions_comparison.png")
    _ensure_dir(filename)
    plt.tight_layout()
    plt.savefig(filename, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    return filename


# ── Overall score ranking ─────────────────────────────────────────────────────

def plot_ranking(results: List[ContentScore], filename: str = None) -> str:
    sorted_results = sorted(results, key=lambda r: r.overall_score, reverse=True)
    labels  = [f"{r.label[:28]}\n({r.profile_type})" for r in sorted_results]
    scores  = [r.overall_score for r in sorted_results]

    cmap = plt.cm.RdYlGn
    bar_colors = [cmap(s / 100) for s in scores]

    fig, ax = plt.subplots(figsize=(10, max(5, len(results) * 0.8 + 2)))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")

    bars = ax.barh(labels, scores, color=bar_colors, height=0.6, edgecolor="#30363D")
    for bar, score in zip(bars, scores):
        ax.text(min(score + 1, 97), bar.get_y() + bar.get_height() / 2,
                f"{score:.0f}", va="center", ha="left", color="#C9D1D9", fontsize=9)

    ax.set_xlim(0, 105)
    ax.set_xlabel("Psychological Engagement Score (0-100)", color="#8B949E", fontsize=9)
    ax.set_title("Content Engagement Ranking", color="#E6EDF3", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#8B949E")
    ax.axvline(x=50, color="#8B949E", linestyle="--", linewidth=0.8, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color("#30363D")

    if filename is None:
        filename = os.path.join(OUTPUT_DIR, "engagement_ranking.png")
    _ensure_dir(filename)
    plt.tight_layout()
    plt.savefig(filename, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    return filename


# ── Markdown report ───────────────────────────────────────────────────────────

def write_report(results: List[ContentScore], filename: str = None) -> str:
    if filename is None:
        filename = os.path.join(OUTPUT_DIR, "analysis_report.md")

    lines = [
        "# Content Psychology Analysis Report",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Content | Type | Score | Profile Type | Top Dimension |",
        "|:---|:---|:---:|:---|:---|",
    ]

    for r in results:
        top = max(r.dimensions.values(), key=lambda d: d.score)
        lines.append(
            f"| {r.label[:35]} | {r.content_type} | {r.overall_score:.0f}/100 "
            f"| {r.profile_type} | {top.label} ({top.score:.0f}) |"
        )

    lines += ["", "---", "", "## Theoretical Framework", ""]

    for dim_id, dim in ENGAGEMENT_DIMENSIONS.items():
        lines.append(f"**{dim['label']}** — *{dim['theory']}*")
        lines.append(f"> {dim['description']}")
        lines.append("")

    lines += ["---", ""]

    for r in results:
        lines += [
            f"## {r.label}",
            f"**Type:** {r.content_type}  |  **Score:** {r.overall_score:.0f}/100  "
            f"|  **Profile:** {r.profile_type}",
            f"> {CONTENT_PROFILE_TYPES.get(r.profile_type, '')}",
            "",
            "**Dimension Scores:**",
            "",
            "| Dimension | Score | Theory | Key Signals |",
            "|:---|:---:|:---|:---|",
        ]
        for d in sorted(r.dimensions.values(), key=lambda x: x.score, reverse=True):
            sigs = ", ".join(f"`{s}`" for s in d.signals[:4])
            lines.append(f"| {d.label} | {d.score:.0f} | {d.theory} | {sigs} |")

        lines += ["", "**Recommendations:**"]
        for rec in r.recommendations:
            lines.append(f"- {rec}")

        lines += ["", "---", ""]

    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename


# ── Framing comparison (two wordings of one message) ─────────────────────────

def plot_framing_radar(cmp, filename: str = None) -> str:
    dims = list(cmp.deltas.values())
    labels = [cmp.result_a.dimensions[d.dimension_id].short for d in dims]
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    closed = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")
    for scores, color, name in [([d.score_a for d in dims], "#3498DB", cmp.label_a),
                                ([d.score_b for d in dims], "#E67E22", cmp.label_b)]:
        ax.plot(closed, scores + scores[:1], color=color, linewidth=2, label=name)
        ax.fill(closed, scores + scores[:1], color=color, alpha=0.18)

    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], color="#8B949E", fontsize=7)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#C9D1D9", fontsize=9)
    ax.grid(color="#30363D", linewidth=0.8)
    ax.spines["polar"].set_color("#30363D")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=8,
              facecolor="#161B22", edgecolor="#30363D", labelcolor="#C9D1D9")
    ax.set_title("Framing comparison (heuristic emphasis scores)", color="#E6EDF3",
                 fontsize=10, fontweight="bold", pad=20)

    if filename is None:
        filename = os.path.join(OUTPUT_DIR, "framing_comparison.png")
    _ensure_dir(filename)
    plt.tight_layout()
    plt.savefig(filename, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    return filename


def write_framing_report(cmp, filename: str = None) -> str:
    from .framing import CAVEAT

    if filename is None:
        filename = os.path.join(OUTPUT_DIR, "framing_report.md")
    lines = [
        "# Message Framing Comparison",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        f"> {CAVEAT}",
        "",
        f"**{cmp.label_a}:** {cmp.result_a.text}",
        "",
        f"**{cmp.label_b}:** {cmp.result_b.text}",
        "",
        "## Findings",
        "",
    ]
    lines += [f"- {f}" for f in cmp.findings]
    lines += [
        "",
        f"## Dimension scores (difference threshold: {cmp.threshold:.0f} pts)",
        "",
        f"| Dimension | {cmp.label_a} | {cmp.label_b} | Δ (B−A) | Cues only in A | Cues only in B |",
        "|:---|:---:|:---:|:---:|:---|:---|",
    ]
    for d in sorted(cmp.deltas.values(), key=lambda x: abs(x.delta), reverse=True):
        flag = " (differs)" if abs(d.delta) >= cmp.threshold else ""
        lines.append(f"| {d.label}{flag} | {d.score_a:.0f} | {d.score_b:.0f} | {d.delta:+.0f} | "
                     f"{', '.join(d.only_in_a[:4])} | {', '.join(d.only_in_b[:4])} |")
    lines += [
        "",
        f"**Tone (VADER compound):** {cmp.result_a.vader_scores['compound']:+.2f} → "
        f"{cmp.result_b.vader_scores['compound']:+.2f}",
        "",
        f"**Gain/loss wording:** {cmp.label_a}: {cmp.frame_a} {cmp.gain_loss_a} · "
        f"{cmp.label_b}: {cmp.frame_b} {cmp.gain_loss_b}",
        "",
        "---",
        "Framing theory: Chong, D. & Druckman, J. N. (2007). Framing theory. "
        "*Annual Review of Political Science, 10*, 103–126.",
    ]
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename
