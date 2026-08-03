from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


RELEVANCE_LABELS = [
    "water_treatment",
    "adjacent_matrix",
    "treatment_unspecified_matrix",
    "contextual",
    "likely_irrelevant",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read manually reviewed relevance-validation records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def validate_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Return completed rows and reject malformed validation data."""
    required_fields = {
        "sample_relevance_label",
        "manual_relevance_label",
        "manual_include",
    }

    if not rows:
        raise ValueError("The validation file contains no records")

    missing_fields = required_fields.difference(rows[0])

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(
            f"Validation file is missing fields: {missing}"
        )

    completed = []

    for row in rows:
        automatic = row["sample_relevance_label"].strip()
        manual = row["manual_relevance_label"].strip()
        include = row["manual_include"].strip().lower()

        if not automatic or not manual or not include:
            continue

        if automatic not in RELEVANCE_LABELS:
            raise ValueError(
                f"Unknown automatic label: {automatic}"
            )

        if manual not in RELEVANCE_LABELS:
            raise ValueError(
                f"Unknown manual label: {manual}"
            )

        if include not in {"yes", "no"}:
            raise ValueError(
                f"Invalid manual_include value: {include}"
            )

        completed.append(row)

    return completed


def calculate_metrics(
    rows: list[dict[str, str]],
) -> dict[str, Any]:
    """Calculate accuracy, precision and inclusion statistics."""
    automatic_counts = Counter(
        row["sample_relevance_label"].strip()
        for row in rows
    )
    manual_counts = Counter(
        row["manual_relevance_label"].strip()
        for row in rows
    )
    include_counts = Counter(
        row["manual_include"].strip().lower()
        for row in rows
    )

    correct_by_label: Counter[str] = Counter()
    confusion: dict[str, Counter[str]] = {
        label: Counter()
        for label in RELEVANCE_LABELS
    }

    exact_matches = 0

    for row in rows:
        automatic = row["sample_relevance_label"].strip()
        manual = row["manual_relevance_label"].strip()

        confusion[automatic][manual] += 1

        if automatic == manual:
            exact_matches += 1
            correct_by_label[automatic] += 1

    accuracy = exact_matches / len(rows) if rows else 0.0

    return {
        "automatic_counts": automatic_counts,
        "manual_counts": manual_counts,
        "include_counts": include_counts,
        "correct_by_label": correct_by_label,
        "confusion": confusion,
        "exact_matches": exact_matches,
        "accuracy": accuracy,
    }


def print_counts(
    heading: str,
    counts: Counter[str],
) -> None:
    """Print a labelled count section."""
    print(f"\n{heading}")
    print("-" * 40)

    for label, count in sorted(counts.items()):
        print(f"{label}: {count}")


def print_confusion_matrix(
    confusion: dict[str, Counter[str]],
) -> None:
    """Print automatic labels against manual labels."""
    print("\nConfusion matrix")
    print("Rows = automatic; columns = manual")
    print("-" * 120)

    row_width = 32
    column_width = 22

    print(
        "".ljust(row_width)
        + "".join(
            label[:20].rjust(column_width)
            for label in RELEVANCE_LABELS
        )
    )

    for automatic in RELEVANCE_LABELS:
        line = automatic.ljust(row_width)

        for manual in RELEVANCE_LABELS:
            line += str(
                confusion[automatic][manual]
            ).rjust(column_width)

        print(line)


def print_report(
    total_rows: int,
    completed_rows: list[dict[str, str]],
    metrics: dict[str, Any],
) -> None:
    """Print the complete validation report."""
    completed_count = len(completed_rows)
    exact_matches = metrics["exact_matches"]
    accuracy = metrics["accuracy"]

    print(f"Total records: {total_rows}")
    print(f"Completed records: {completed_count}")

    if completed_count != total_rows:
        missing = total_rows - completed_count
        print(f"Incomplete records: {missing}")

    print("\nOverall exact-label accuracy")
    print("-" * 40)
    print(
        f"{exact_matches}/{completed_count} "
        f"({accuracy:.1%})"
    )

    print_counts(
        "Automatic label counts",
        metrics["automatic_counts"],
    )
    print_counts(
        "Manual label counts",
        metrics["manual_counts"],
    )

    print("\nPrecision by automatic category")
    print("-" * 40)

    automatic_counts = metrics["automatic_counts"]
    correct_by_label = metrics["correct_by_label"]

    for label in RELEVANCE_LABELS:
        total = automatic_counts[label]
        correct = correct_by_label[label]

        if total:
            print(
                f"{label}: {correct}/{total} "
                f"({correct / total:.1%})"
            )
        else:
            print(f"{label}: no sampled records")

    print_confusion_matrix(metrics["confusion"])

    print_counts(
        "Manual inclusion decisions",
        metrics["include_counts"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate manually reviewed PFAS relevance labels."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "validation/relevance_validation_sample.csv"
        ),
        help="Path to the reviewed validation CSV",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    completed_rows = validate_rows(rows)

    if not completed_rows:
        raise ValueError(
            "No completed validation records were found"
        )

    metrics = calculate_metrics(completed_rows)
    print_report(
        total_rows=len(rows),
        completed_rows=completed_rows,
        metrics=metrics,
    )


if __name__ == "__main__":
    main()
