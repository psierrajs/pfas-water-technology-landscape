from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_final.csv"
)

OUTPUT_PATH = Path(
    "figures/patent_adsorption_strategic_themes.png"
)

def read_rows() -> list[dict[str, str]]:
    """Read the final adsorption family intelligence dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def format_label(
    value: str,
) -> str:
    """Convert machine-readable labels into chart labels."""
    special_labels = {
        "capture_and_destroy": "Capture and destroy",
        "combined_treatment_train": "Combined treatment train",
        "enhanced_adsorption_material": "Enhanced adsorption material",
        "conventional_adsorption": "Conventional adsorption",
        "in_situ_remediation": "In-situ remediation",
        "industrial_point_source": "Industrial point source",
        "mobile_or_modular_treatment": "Mobile/modular treatment",
        "regenerable_carbon": "Regenerable carbon",
    }

    return special_labels.get(
        value,
        value.replace("_", " ").title(),
    )

def count_strategic_themes(
    rows: list[dict[str, str]],
) -> Counter[str]:
    """Count strategic-theme classifications."""
    return Counter(
        row.get(
            "strategic_theme",
            "",
        ).strip()
        for row in rows
        if row.get(
            "strategic_theme",
            "",
        ).strip()
    )


def prepare_chart_data(
    counts: Counter[str],
) -> tuple[list[str], list[int]]:
    """Prepare sorted labels and values for plotting."""
    items = sorted(
        counts.items(),
        key=lambda item: (
            item[1],
            item[0],
        ),
    )

    labels = [
        format_label(label)
        for label, _ in items
    ]

    values = [
        count
        for _, count in items
    ]

    return labels, values

def create_chart(
    labels: list[str],
    values: list[int],
) -> None:
    """Create and save the strategic-theme bar chart."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    bars = ax.barh(
        labels,
        values,
    )

    ax.set_title(
        "Strategic Themes in Activated-Carbon PFAS Patent Families"
    )

    ax.set_xlabel(
        "Number of patent families"
    )

    ax.set_ylabel(
        "Strategic theme"
    )

    for bar, value in zip(
        bars,
        values,
    ):
        ax.text(
            value + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center",
        )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)


def main() -> None:
    """Generate the adsorption strategic-theme figure."""
    rows = read_rows()

    counts = count_strategic_themes(
        rows
    )

    labels, values = prepare_chart_data(
        counts
    )

    create_chart(
        labels,
        values,
    )

    print(
        f"Patent families plotted: {len(rows)}"
    )
    print(
        f"Figure written to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
