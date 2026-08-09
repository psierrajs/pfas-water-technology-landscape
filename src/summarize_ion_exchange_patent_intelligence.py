from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_family_intelligence.csv"
)

REPORT_PATH = Path(
    "reports/patent-ion-exchange-intelligence-summary.md"
)


def format_label(value: str) -> str:
    return value.replace("_", " ")


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Family intelligence file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    treatment_counts = (
        df["treatment_mode"]
        .value_counts()
    )

    resin_counts = (
        df["resin_strategy"]
        .value_counts()
    )

    lines = [
        "# Ion-Exchange Patent Intelligence Summary",
        "",
        "## Dataset",
        "",
        f"- Included patent families: {len(df)}",
        "",
        "## Treatment mode",
        "",
    ]

    for label, count in treatment_counts.items():
        lines.append(
            f"- {format_label(label)}: {count}"
        )

    lines.extend(
        [
            "",
            "## Resin strategy",
            "",
        ]
    )

    for label, count in resin_counts.items():
        lines.append(
            f"- {format_label(label)}: {count}"
        )

    lines.extend(
        [
            "",
            "## Initial intelligence signals",
            "",
            (
                "- Conventional ion-exchange adsorption remains "
                "the dominant pattern in the included families."
            ),
            (
                "- Regeneration is a visible innovation theme, "
                "indicating interest in reducing resin replacement "
                "and secondary waste."
            ),
            (
                "- Several families move beyond simple capture toward "
                "combined treatment or capture-and-destroy approaches."
            ),
            (
                "- Selective and chemically modified resins represent "
                "an important material-development direction."
            ),
            "",
        ]
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Families summarized: {len(df)}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()

    