from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path(
    "data/processed/"
    "science_patent_technology_comparison.csv"
)

FIGURE_PATH = Path(
    "figures/"
    "science_patent_technology_comparison.png"
)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Comparison file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    labels = (
        df["technology"]
        .str.replace("_", " ")
        .str.title()
    )

    x = range(len(df))
    width = 0.35

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    science_bars = ax.bar(
        [value - width / 2 for value in x],
        df["science_publications"],
        width=width,
        label="Scientific publications",
    )

    patent_bars = ax.bar(
        [value + width / 2 for value in x],
        df["patent_families"],
        width=width,
        label="Patent families",
    )

    ax.bar_label(
        science_bars,
        padding=3,
    )

    ax.bar_label(
        patent_bars,
        padding=3,
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)

    ax.set_ylabel("Evidence count")
    ax.set_title(
        "PFAS Water Treatment: Science vs Patent Activity"
    )

    ax.legend()

    fig.tight_layout()

    FIGURE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        FIGURE_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"Figure: {FIGURE_PATH}")


if __name__ == "__main__":
    main()