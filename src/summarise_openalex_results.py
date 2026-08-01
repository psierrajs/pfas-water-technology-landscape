from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dictionaries."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def print_counter(
    title: str,
    counter: Counter[str],
    limit: int | None = None,
) -> None:
    """Print a labelled frequency table."""
    print()
    print(title)
    print("-" * len(title))

    items = counter.most_common(limit)

    for value, count in items:
        label = value or "Unknown"
        print(f"{label}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarise deduplicated OpenAlex PFAS results."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/openalex_deduplicated.csv"),
        help="Deduplicated OpenAlex CSV file.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top records or sources to display.",
    )
    args = parser.parse_args()

    rows = read_csv(args.input)

    print(f"Total unique records: {len(rows)}")

    years = Counter(
        row.get("publication_year", "")
        for row in rows
    )

    sources = Counter(
        row.get("source", "")
        for row in rows
    )

    publication_types = Counter(
        row.get("type", "")
        for row in rows
    )

    query_counts = Counter(
        row.get("query_count", "")
        for row in rows
    )

    category_counts: Counter[str] = Counter()

    for row in rows:
        categories = row.get("categories", "")

        for category in categories.split(";"):
            category = category.strip()

            if category:
                category_counts[category] += 1

    print_counter(
        "Publications by year",
        Counter(dict(sorted(years.items()))),
    )

    print_counter(
        "Publication types",
        publication_types,
    )

    print_counter(
        "Most frequent sources",
        sources,
        args.top,
    )

    print_counter(
        "Records retrieved by number of queries",
        query_counts,
    )

    print_counter(
        "Query-category coverage",
        category_counts,
    )

    ranked_rows = sorted(
        rows,
        key=lambda row: (
            -int(row.get("query_count", "0") or 0),
            -int(row.get("cited_by_count", "0") or 0),
        ),
    )

    print()
    print("Most widely retrieved records")
    print("-----------------------------")

    for row in ranked_rows[: args.top]:
        print()
        print(row.get("title", ""))
        print(f"Year: {row.get('publication_year', '')}")
        print(f"Queries: {row.get('query_count', '')}")
        print(f"Query IDs: {row.get('query_ids', '')}")
        print(f"Citations: {row.get('cited_by_count', '')}")


if __name__ == "__main__":
    main()
