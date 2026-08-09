from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/"
    "science_patent_technology_comparison.csv"
)

REPORT_PATH = Path(
    "reports/science-patent-technology-comparison.md"
)


def format_label(value: str) -> str:
    return value.replace("_", " ")


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Comparison file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    lines = [
        "# Science–Patent Technology Comparison",
        "",
        "## Scope",
        "",
        (
            "This comparison examines the relative scientific and patent "
            "activity observed for activated-carbon and ion-exchange "
            "PFAS water-treatment technologies."
        ),
        "",
        "## Evidence counts",
        "",
    ]

    for _, row in df.iterrows():
        lines.extend(
            [
                f"### {format_label(row['technology']).title()}",
                "",
                f"- Scientific publications: {row['science_publications']}",
                f"- Patent families: {row['patent_families']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Initial intelligence signals",
            "",
            (
                "- Activated carbon and ion exchange show similar scientific "
                "representation in the analysed publication corpus."
            ),
            (
                "- Activated carbon shows a larger number of included patent "
                "families in the current patent datasets."
            ),
            (
                "- This may indicate stronger translation from research into "
                "patented technology for activated-carbon approaches, although "
                "differences in search strategy and patent coverage mean that "
                "the comparison should be interpreted as directional rather "
                "than absolute."
            ),
            (
                "- Both technologies display substantial activity across "
                "scientific and patent evidence, supporting their importance "
                "within the PFAS water-treatment landscape."
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

    print(f"Technologies compared: {len(df)}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
    