from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/"
    "patent_technology_comparison.csv"
)

REPORT_PATH = Path(
    "reports/patent-technology-comparison.md"
)


def format_label(value: str) -> str:
    return value.replace("_", " ")


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Comparison file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    family_counts = (
        df["technology"]
        .value_counts()
    )

    treatment_table = pd.crosstab(
        df["technology"],
        df["treatment_mode"],
    )

    lines = [
        "# Patent Technology Comparison",
        "",
        "## Scope",
        "",
        (
            "This comparison integrates the included patent-family "
            "datasets for activated carbon and ion-exchange technologies."
        ),
        "",
        "## Family coverage",
        "",
    ]

    for technology, count in family_counts.items():
        lines.append(
            f"- {format_label(technology)}: {count} families"
        )

    lines.extend(
        [
            "",
            "## Treatment-mode comparison",
            "",
        ]
    )

    for technology in treatment_table.index:
        lines.append(
            f"### {format_label(technology).title()}"
        )
        lines.append("")

        for mode, count in treatment_table.loc[
            technology
        ].items():
            if count > 0:
                lines.append(
                    f"- {format_label(mode)}: {count}"
                )

        lines.append("")

    lines.extend(
        [
            "## Initial comparative signals",
            "",
            (
                "- Activated-carbon patents show a stronger presence "
                "of combined-process architectures."
            ),
            (
                "- Ion-exchange patents show a relatively stronger "
                "emphasis on regeneration and capture-and-destroy concepts."
            ),
            (
                "- Adsorption remains the dominant treatment mode "
                "for both technology groups."
            ),
            (
                "- The comparison suggests that innovation is moving "
                "beyond simple contaminant capture toward regeneration, "
                "integration and destruction."
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

    print(
        f"Patent families compared: {len(df)}"
    )
    print(
        f"Report: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()
    