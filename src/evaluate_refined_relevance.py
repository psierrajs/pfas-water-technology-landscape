from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from classify_openalex_relevance import classify_relevance


RELEVANCE_LABELS = [
    "water_treatment",
    "adjacent_matrix",
    "treatment_unspecified_matrix",
    "contextual",
    "likely_irrelevant",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read the manually reviewed validation records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def completed_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Return records containing completed manual labels."""
    completed = []

    for row in rows:
        manual_label = row.get(
            "manual_relevance_label",
            "",
        ).strip()

        if manual_label:
            completed.append(row)

    return completed


def evaluate(
    rows: list[dict[str, str]],
) -> None:
    """Compare original and refined predictions with manual labels."""
    original_correct = 0
    refined_correct = 0

    original_by_label: Counter[str] = Counter()
    refined_by_label: Counter[str] = Counter()
    refined_correct_by_label: Counter[str] = Counter()
    transitions: Counter[tuple[str, str]] = Counter()

    disagreements = []

    for row in rows:
        title = row.get("title", "")
        abstract = row.get("abstract", "")

        original = row["sample_relevance_label"].strip()
        manual = row["manual_relevance_label"].strip()

        refined, signals = classify_relevance(
            title,
            abstract,
        )

        original_by_label[original] += 1
        refined_by_label[refined] += 1

        if original == manual:
            original_correct += 1

        if refined == manual:
            refined_correct += 1
            refined_correct_by_label[refined] += 1

        if original != refined:
            transitions[(original, refined)] += 1

        if refined != manual:
            disagreements.append(
                {
                    "title": title,
                    "doi": row.get("doi", ""),
                    "original": original,
                    "refined": refined,
                    "manual": manual,
                    "signals": ";".join(signals),
                }
            )

    total = len(rows)

    print(f"Validation records: {total}")

    print("\nOriginal classifier")
    print("-" * 40)
    print(
        f"{original_correct}/{total} "
        f"({original_correct / total:.1%})"
    )

    print("\nRefined classifier")
    print("-" * 40)
    print(
        f"{refined_correct}/{total} "
        f"({refined_correct / total:.1%})"
    )

    difference = refined_correct - original_correct

    print("\nAccuracy change")
    print("-" * 40)
    print(
        f"{difference:+d} correct classifications"
    )

    print("\nRefined precision by predicted category")
    print("-" * 40)

    for label in RELEVANCE_LABELS:
        predicted = refined_by_label[label]
        correct = refined_correct_by_label[label]

        if predicted:
            print(
                f"{label}: {correct}/{predicted} "
                f"({correct / predicted:.1%})"
            )
        else:
            print(f"{label}: no predictions")

    print("\nChanged predictions")
    print("-" * 40)

    if transitions:
        for transition, count in sorted(
            transitions.items(),
            key=lambda item: (-item[1], item[0]),
        ):
            original, refined = transition
            print(
                f"{original} -> {refined}: {count}"
            )
    else:
        print("No predictions changed")

    print("\nRemaining disagreements")
    print("-" * 40)

    if not disagreements:
        print("None")
        return

    for index, row in enumerate(
        disagreements,
        start=1,
    ):
        print()
        print(f"{index}. {row['title']}")
        print(f"DOI: {row['doi']}")
        print(f"Original: {row['original']}")
        print(f"Refined: {row['refined']}")
        print(f"Manual: {row['manual']}")
        print(f"Signals: {row['signals']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the refined relevance classifier against "
            "the manually reviewed validation sample."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "validation/relevance_validation_sample.csv"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    reviewed = completed_rows(rows)

    if not reviewed:
        raise ValueError(
            "No manually reviewed records were found"
        )

    evaluate(reviewed)


if __name__ == "__main__":
    main()
