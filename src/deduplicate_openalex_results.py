from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


PREPRINT_DOI_MARKERS = (
    "10.20944/preprints",
    "10.2139/ssrn",
    "10.26434/chemrxiv",
    "10.31223/",
    "10.1101/",
    "scimeetings",
)


def normalise_identifier(value: str) -> str:
    """Return a lowercase identifier suitable for comparison."""
    return value.strip().lower()


def normalise_title(value: str) -> str:
    """Normalize title punctuation, spacing, case, and dash variants."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def record_key(row: dict[str, str]) -> str:
    """Prefer DOI, then OpenAlex ID, then normalized title."""
    doi = normalise_identifier(row.get("doi", ""))

    if doi:
        return f"doi:{doi}"

    openalex_id = normalise_identifier(row.get("openalex_id", ""))

    if openalex_id:
        return f"openalex:{openalex_id}"

    title = normalise_title(row.get("title", ""))

    if title:
        return f"title:{title}"

    raise ValueError("Record has no DOI, OpenAlex ID, or title")


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read OpenAlex query results from CSV."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> set[str]:
    """Split semicolon-delimited provenance values."""
    return {
        item.strip()
        for item in value.split(";")
        if item.strip()
    }


def integer_value(value: str, default: int = 0) -> int:
    """Safely convert a string to an integer."""
    try:
        return int(value or default)
    except ValueError:
        return default


def is_preprint_like(row: dict[str, Any]) -> bool:
    """Return True for common preprint and meeting-record identifiers."""
    doi = normalise_identifier(str(row.get("doi", "")))
    source = normalise_identifier(str(row.get("source", "")))
    work_type = normalise_identifier(str(row.get("type", "")))

    if any(marker in doi for marker in PREPRINT_DOI_MARKERS):
        return True

    return (
        "preprint" in source
        or "preprint" in work_type
        or "posted-content" in work_type
    )


def preferred_record_key(row: dict[str, Any]) -> tuple[int, int, int, int]:
    """
    Rank records so final publications are preferred over preprints.

    Preference order:
    1. Non-preprint records
    2. Records with an abstract
    3. Records with more citations
    4. Records with a DOI
    """
    return (
        0 if is_preprint_like(row) else 1,
        1 if str(row.get("abstract", "")).strip() else 0,
        integer_value(str(row.get("cited_by_count", "0"))),
        1 if str(row.get("doi", "")).strip() else 0,
    )


def merge_raw_query_hits(
    matching_rows: list[dict[str, str]],
) -> dict[str, Any]:
    """Merge duplicate query hits for a single bibliographic record."""
    matching_rows.sort(
        key=lambda row: (
            row.get("query_id", ""),
            integer_value(row.get("rank", "0")),
        )
    )

    first = matching_rows[0]

    query_ids = sorted(
        {
            row.get("query_id", "")
            for row in matching_rows
            if row.get("query_id")
        }
    )

    categories = sorted(
        {
            row.get("category", "")
            for row in matching_rows
            if row.get("category")
        }
    )

    best_rank = min(
        integer_value(row.get("rank", "0"))
        for row in matching_rows
    )

    return {
        "openalex_id": first.get("openalex_id", ""),
        "doi": first.get("doi", ""),
        "title": first.get("title", ""),
        "abstract": first.get("abstract", ""),
        "publication_year": first.get("publication_year", ""),
        "type": first.get("type", ""),
        "source": first.get("source", ""),
        "authors": first.get("authors", ""),
        "cited_by_count": first.get("cited_by_count", ""),
        "query_count": len(query_ids),
        "query_ids": ";".join(query_ids),
        "categories": ";".join(categories),
        "best_rank": best_rank,
    }


def merge_title_versions(
    matching_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Merge preprint, conference, and journal versions sharing a title.

    Bibliographic fields come from the preferred version, while search
    provenance is combined across every version.
    """
    preferred = max(matching_rows, key=preferred_record_key)

    query_ids: set[str] = set()
    categories: set[str] = set()

    for row in matching_rows:
        query_ids.update(split_values(str(row.get("query_ids", ""))))
        categories.update(split_values(str(row.get("categories", ""))))

    best_rank = min(
        integer_value(str(row.get("best_rank", "0")))
        for row in matching_rows
    )

    merged = dict(preferred)
    merged["query_ids"] = ";".join(sorted(query_ids))
    merged["query_count"] = len(query_ids)
    merged["categories"] = ";".join(sorted(categories))
    merged["best_rank"] = best_rank

    return merged


def deduplicate_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    """
    Deduplicate query hits and bibliographic versions.

    Pass 1 merges repeated search hits using DOI, OpenAlex ID, or title.
    Pass 2 merges preprint and published versions with normalized titles.
    """
    identifier_groups: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        identifier_groups[record_key(row)].append(row)

    identifier_deduplicated = [
        merge_raw_query_hits(matching_rows)
        for matching_rows in identifier_groups.values()
    ]

    title_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in identifier_deduplicated:
        normalized_title = normalise_title(str(row.get("title", "")))

        if normalized_title:
            title_groups[normalized_title].append(row)
        else:
            title_groups[f"openalex:{row.get('openalex_id', '')}"].append(row)

    deduplicated = [
        merge_title_versions(matching_rows)
        for matching_rows in title_groups.values()
    ]

    deduplicated.sort(
        key=lambda row: (
            -integer_value(str(row["query_count"])),
            integer_value(str(row["best_rank"])),
            str(row["title"]).lower(),
        )
    )

    return deduplicated


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    """Write deduplicated results to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "openalex_id",
        "doi",
        "title",
        "abstract",
        "publication_year",
        "type",
        "source",
        "authors",
        "cited_by_count",
        "query_count",
        "query_ids",
        "categories",
        "best_rank",
    ]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deduplicate OpenAlex query hits and publication versions."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/openalex_query_results.csv"),
        help="Input CSV generated by run_openalex_queries.py.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/openalex_deduplicated.csv"),
        help="Output CSV for deduplicated records.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    deduplicated = deduplicate_rows(rows)
    write_csv(deduplicated, args.output)

    duplicate_count = len(rows) - len(deduplicated)

    print(f"Input records: {len(rows)}")
    print(f"Unique records: {len(deduplicated)}")
    print(f"Duplicate records merged: {duplicate_count}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
