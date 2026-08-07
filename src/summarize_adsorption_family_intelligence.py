from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_final.csv"
)

REPORT_PATH = Path(
    "reports/patent-adsorption-intelligence-summary.md"
)

def read_rows() -> list[dict[str, str]]:
    """Read the final adsorption family intelligence dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def count_field(
    rows: list[dict[str, str]],
    field: str,
) -> Counter[str]:
    """Count values for one intelligence field."""
    return Counter(
        row.get(
            field,
            "",
        ).strip() or "blank"
        for row in rows
    )
def format_label(
    label: str,
) -> str:
    """Convert machine-readable labels into report-friendly text."""
    special_labels = {
        "GAC": "GAC",
        "PAC": "PAC",
        "submicron_PAC": "sub-micron PAC",
    }

    if label in special_labels:
        return special_labels[label]

    return label.replace(
        "_",
        " ",
    )

def format_counter(
    counts: Counter[str],
) -> list[str]:
    """Format a counter as Markdown bullet lines."""
    return [
        f"- {format_label(label)}: {count}"
        for label, count in counts.most_common()
    ]
    
def build_core_counts(
    rows: list[dict[str, str]],
) -> dict[str, Counter[str]]:
    """Build counts for the main intelligence dimensions."""
    fields = (
        "treatment_mode",
        "carbon_type",
        "target_matrix",
        "pfas_handling",
        "system_configuration",
        "maturity_signal",
        "strategic_theme",
    )

    return {
        field: count_field(
            rows,
            field,
        )
        for field in fields
    }


def build_key_signals(
    rows: list[dict[str, str]],
) -> list[str]:
    """Build concise strategic signals from the classified families."""
    counts = build_core_counts(
        rows
    )

    total = len(rows)

    capture_only = counts[
        "pfas_handling"
    ].get(
        "capture_only",
        0,
    )

    destructive = sum(
        counts["pfas_handling"].get(
            label,
            0,
        )
        for label in (
            "capture_and_destroy",
            "destruction",
            "defluorination",
        )
    )

    field_deployable = counts[
        "maturity_signal"
    ].get(
        "field_deployable_system",
        0,
    )

    enhanced_materials = counts[
        "strategic_theme"
    ].get(
        "enhanced_adsorption_material",
        0,
    )

    combined_processes = counts[
        "treatment_mode"
    ].get(
        "combined_process",
        0,
    )

    return [
        (
            f"- Capture-only approaches remain dominant "
            f"({capture_only} of {total} families)."
        ),
        (
            f"- {destructive} families incorporate destruction, "
            "capture-and-destroy, or explicit defluorination."
        ),
        (
            f"- {combined_processes} families use combined-process "
            "architectures rather than adsorption alone."
        ),
        (
            f"- Enhanced adsorption materials account for "
            f"{enhanced_materials} families."
        ),
        (
            f"- {field_deployable} families show field-deployable "
            "system characteristics."
        ),
    ]

def build_report(
    rows: list[dict[str, str]],
) -> str:
    """Build the adsorption family intelligence Markdown report."""
    counts = build_core_counts(
        rows
    )

    lines = [
        "# Activated-Carbon PFAS Patent Intelligence Summary",
        "",
        "## Scope",
        "",
        (
            "This report summarizes the final family-level "
            "intelligence classification for the included "
            "activated-carbon PFAS patent families."
        ),
        "",
        "## Portfolio overview",
        "",
        f"- Included patent families: {len(rows)}",
        "",
        "## Treatment modes",
        "",
        *format_counter(
            counts["treatment_mode"]
        ),
        "",
        "## Carbon types",
        "",
        *format_counter(
            counts["carbon_type"]
        ),
        "",
        "## Target matrices",
        "",
        *format_counter(
            counts["target_matrix"]
        ),
        "",
        "## PFAS handling",
        "",
        *format_counter(
            counts["pfas_handling"]
        ),
        "",
        "## System configurations",
        "",
        *format_counter(
            counts["system_configuration"]
        ),
        "",
        "## Maturity signals",
        "",
        *format_counter(
            counts["maturity_signal"]
        ),
        "",
        "## Strategic themes",
        "",
        *format_counter(
            counts["strategic_theme"]
        ),
        "",
        "## Key intelligence signals",
        "",
        *build_key_signals(
            rows
        ),
        "",
    ]

    return "\n".join(lines)

def write_report(
    report_text: str,
) -> Path:
    """Write the family intelligence report."""
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        report_text,
        encoding="utf-8",
    )

    return REPORT_PATH


def main() -> None:
    """Generate the adsorption family intelligence summary."""
    rows = read_rows()

    report_text = build_report(
        rows
    )

    output_path = write_report(
        report_text
    )

    print(
        f"Patent families summarized: {len(rows)}"
    )
    print(
        f"Report written to: {output_path}"
    )


if __name__ == "__main__":
    main()

