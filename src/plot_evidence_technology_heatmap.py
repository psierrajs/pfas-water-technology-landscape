from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_PATH = Path(
    "data/processed/evidence_technology_matrix/"
    "evidence_type_by_technology.csv"
)

OUTPUT_DIR = Path(
    "figures/evidence_technology"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "evidence_type_by_technology_heatmap.png"
)

EVIDENCE_COLUMNS = [
    "field_demonstration",
    "pilot",
    "life_cycle_assessment",
    "experimental",
    "computational",
    "mechanistic",
    "review",
]

def read_matrix() -> tuple[
    list[str],
    list[list[int]],
]:
    """Read technology labels and evidence counts."""
    technologies: list[str] = []
    matrix: list[list[int]] = []

    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            technologies.append(
                row["technology"]
            )

            matrix.append(
                [
                    int(row[column])
                    for column in EVIDENCE_COLUMNS
                ]
            )

    return technologies, matrix

def format_evidence_labels() -> list[str]:
    """Create readable labels for the heatmap columns."""
    return [
        column.replace("_", " ").title()
        for column in EVIDENCE_COLUMNS
    ]


def format_technology_labels(
    technologies: list[str],
) -> list[str]:
    """Create readable labels for the heatmap rows."""
    return [
        technology.replace("_", " ").title()
        for technology in technologies
    ]

def plot_heatmap(
    technologies: list[str],
    matrix: list[list[int]],
) -> None:
    """Create and save the evidence-technology heatmap."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(12, 8),
    )

    image = axis.imshow(
        matrix,
        aspect="auto",
    )

    axis.set_xticks(
        range(len(EVIDENCE_COLUMNS))
    )
    axis.set_xticklabels(
        format_evidence_labels(),
        rotation=35,
        ha="right",
    )

    axis.set_yticks(
        range(len(technologies))
    )
    axis.set_yticklabels(
        format_technology_labels(
            technologies
        )
    )

    axis.set_title(
        "PFAS Water Treatment Evidence by Technology"
    )
    axis.set_xlabel(
        "Evidence type"
    )
    axis.set_ylabel(
        "Technology"
    )

    figure.colorbar(
        image,
        ax=axis,
        label="Publication count",
    )

    figure.tight_layout()

    figure.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

def main() -> None:
    """Build the evidence-technology heatmap."""
    technologies, matrix = read_matrix()

    plot_heatmap(
        technologies,
        matrix,
    )

    print(
        f"Technologies plotted: {len(technologies)}"
    )
    print(
        f"Evidence categories: {len(EVIDENCE_COLUMNS)}"
    )
    print(
        f"Figure written to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
