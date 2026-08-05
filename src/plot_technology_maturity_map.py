from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_PATH = Path(
    "data/processed/technology_maturity/"
    "technology_maturity_scores.csv"
)

OUTPUT_DIR = Path(
    "figures/technology_maturity"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "technology_maturity_map.png"
)

LABEL_OFFSETS = {
    "ion_exchange": (8, 4),
    "supercritical_water_oxidation": (8, 4),
    "electrochemical_oxidation": (8, 4),
    "adsorption": (8, 4),
    "plasma": (8, 4),
    "photocatalysis": (8, 4),
    "sonolysis": (8, 12),
    "thermal": (8, -18),
    "biological": (8, 22),
    "membranes": (8, 32),
    "hydrothermal": (8, -28),
    "capture_and_destroy": (8, -38),
}

def read_maturity_rows() -> list[dict[str, str]]:
    """Read technology maturity scores."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def to_float(
    row: dict[str, str],
    field: str,
) -> float:
    """Convert a CSV value to float."""
    value = row.get(field, "").strip()

    if not value:
        return 0.0

    return float(value)

def extract_plot_data(
    rows: list[dict[str, str]],
) -> tuple[
    list[str],
    list[float],
    list[float],
    list[float],
]:
    """Extract labels, coordinates and point sizes."""
    technologies: list[str] = []
    research_scores: list[float] = []
    deployment_scores: list[float] = []
    publication_counts: list[float] = []

    for row in rows:
        technologies.append(
            row["technology"]
        )

        research_scores.append(
            to_float(
                row,
                "normalized_research_score",
            )
        )

        deployment_scores.append(
            to_float(
                row,
                "normalized_deployment_score",
            )
        )

        publication_counts.append(
            to_float(
                row,
                "total_unique_publications",
            )
        )

    return (
        technologies,
        research_scores,
        deployment_scores,
        publication_counts,
    )

def format_technology_label(
    technology: str,
) -> str:
    """Create a readable technology label."""
    return technology.replace(
        "_",
        " ",
    ).title()


def calculate_point_sizes(
    publication_counts: list[float],
) -> list[float]:
    """Scale publication counts for scatter-plot marker sizes."""
    return [
        max(
            count * 8,
            80,
        )
        for count in publication_counts
    ]

def plot_maturity_map(
    technologies: list[str],
    research_scores: list[float],
    deployment_scores: list[float],
    publication_counts: list[float],

) -> None:
    """Create and save the technology maturity map."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    point_sizes = calculate_point_sizes(
        publication_counts
    )

    figure, axis = plt.subplots(
        figsize=(12, 8),
    )

    axis.scatter(
        research_scores,
        deployment_scores,
        s=point_sizes,
        alpha=0.7,
    )

    for (
        technology,
        research_score,
        deployment_score,
    ) in zip(
        technologies,
        research_scores,
        deployment_scores,
    ):
        axis.annotate(
            format_technology_label(
                technology
            ),
            (
                research_score,
                deployment_score,
            ),
            xytext=LABEL_OFFSETS.get(
                technology,
                (8, 4),
            ),
            textcoords="offset points",
            fontsize=9,
        )

    axis.set_title(
        "PFAS Water Treatment Technology Maturity Map"
    )
    axis.set_xlabel(
        "Normalized research maturity score"
    )
    axis.set_ylabel(
        "Normalized deployment maturity score"
    )
    axis.set_xlim(
        -2.5,
        56,
    )

    axis.set_ylim(
        -4,
        52,
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    figure.tight_layout()

    figure.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

def main() -> None:
    """Build the technology maturity map."""
    rows = read_maturity_rows()

    (
        technologies,
        research_scores,
        deployment_scores,
        publication_counts,
    ) = extract_plot_data(rows)

    plot_maturity_map(
        technologies,
        research_scores,
        deployment_scores,
        publication_counts,

    )

    print(
        f"Technologies plotted: {len(technologies)}"
    )
    print(
        f"Figure written to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
