from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/high_maturity_validation/"
    "high_maturity_validation_sample.csv"
)

OUTPUT_DIR = Path(
    "reports"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "high-maturity-validation-summary.md"
)

def read_validation_rows() -> list[dict[str, str]]:
    """Read the manually reviewed high-maturity records."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def count_values(
    rows: list[dict[str, str]],
    field: str,
) -> Counter[str]:
    """Count normalized non-empty values from one field."""
    return Counter(
        row.get(
            field,
            "",
        ).strip()
        or "blank"
        for row in rows
    )

def validate_review_completion(
    rows: list[dict[str, str]],
) -> None:
    """Ensure every record has a manual decision and scale."""
    incomplete_rows = [
        row
        for row in rows
        if not row.get(
            "manual_evidence_decision",
            "",
        ).strip()
        or not row.get(
            "manual_scale",
            "",
        ).strip()
    ]

    if incomplete_rows:
        raise ValueError(
            "Validation file contains "
            f"{len(incomplete_rows)} incomplete records."
        )
def format_counts(
    counts: Counter[str],
) -> list[str]:
    """Convert counts into Markdown bullet points."""
    return [
        f"- `{label}`: {count}"
        for label, count in counts.most_common()
    ]


def format_record_table(
    rows: list[dict[str, str]],
) -> list[str]:
    """Create a Markdown table for reviewed records."""
    lines = [
        (
            "| Year | Technology | Automatic label | "
            "Manual decision | Manual scale | Title |"
        ),
        (
            "|---:|---|---|---|---|---|"
        ),
    ]

    for row in rows:
        title = row.get(
            "title",
            "",
        ).replace(
            "|",
            "\\|",
        )

        technologies = row.get(
            "technology_labels",
            "",
        ).replace(
            "|",
            ", ",
        )

        lines.append(
            "| "
            f"{row.get('publication_year', '')} | "
            f"{technologies} | "
            f"{row.get('primary_evidence_type', '')} | "
            f"{row.get('manual_evidence_decision', '')} | "
            f"{row.get('manual_scale', '')} | "
            f"{title} |"
        )

    return lines

def build_report(
    rows: list[dict[str, str]],
) -> str:
    """Build the Markdown validation summary."""
    decision_counts = count_values(
        rows,
        "manual_evidence_decision",
    )

    scale_counts = count_values(
        rows,
        "manual_scale",
    )

    lines = [
        "# High-Maturity Evidence Validation Summary",
        "",
        "## Purpose",
        "",
        (
            "This report documents the manual validation of "
            "publications automatically classified as pilot or "
            "field-demonstration evidence."
        ),
        "",
        "## Validation set",
        "",
        f"- Records reviewed: {len(rows)}",
        "",
        "## Manual evidence decisions",
        "",
        *format_counts(decision_counts),
        "",
        "## Manual scales",
        "",
        *format_counts(scale_counts),
        "",
        "## Reviewed records",
        "",
        *format_record_table(rows),
        "",
    ]

    return "\n".join(lines)

def write_report(
    report: str,
) -> Path:
    """Write the Markdown validation report."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    return OUTPUT_PATH


def main() -> None:
    """Summarize the completed high-maturity validation."""
    rows = read_validation_rows()

    validate_review_completion(
        rows
    )

    report = build_report(
        rows
    )

    output_path = write_report(
        report
    )

    print(
        f"Validated records summarized: {len(rows)}"
    )
    print(
        f"Report written to: {output_path}"
    )


if __name__ == "__main__":
    main()

