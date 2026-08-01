from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Any

import requests


OPENALEX_WORKS_URL = "https://api.openalex.org/works"

QUERIES = {
    "B01": {
        "category": "Cross-technology",
        "query": "PFAS water treatment",
    },
    "T01": {
        "category": "Adsorption",
        "query": "PFAS adsorption water treatment",
    },
    "T02": {
        "category": "Ion exchange",
        "query": "PFAS ion exchange water treatment",
    },
    "T03": {
        "category": "Membranes",
        "query": "PFAS membrane filtration water",
    },
    "T04": {
        "category": "Electrochemical oxidation",
        "query": "PFAS electrochemical oxidation water",
    },
    "T05": {
        "category": "Plasma",
        "query": "PFAS plasma degradation water",
    },
    "T06": {
        "category": "Photocatalysis",
        "query": "PFAS photocatalytic degradation water",
    },
    "T07": {
        "category": "Sonolysis",
        "query": "PFAS sonolysis water degradation",
    },
    "T08": {
        "category": "Supercritical water oxidation",
        "query": "PFAS supercritical water oxidation",
    },
    "T09": {
        "category": "Hydrothermal liquefaction",
        "query": "PFAS hydrothermal liquefaction",
    },
    "T10": {
        "category": "Capture-and-destroy",
        "query": "PFAS combined adsorption electrochemical oxidation",
    },
}


def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs without overwriting existing variables."""
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def extract_authors(work: dict[str, Any]) -> str:
    """Return a semicolon-separated author list."""
    names = []

    for authorship in work.get("authorships", []):
        author = authorship.get("author") or {}
        name = author.get("display_name")

        if name:
            names.append(name)

    return "; ".join(names)


def extract_source(work: dict[str, Any]) -> str:
    """Return the primary source or journal name."""
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    return source.get("display_name") or ""

def reconstruct_abstract(
    inverted_index: dict[str, list[int]] | None,
) -> str:
    """Reconstruct an abstract from an OpenAlex inverted index."""
    if not inverted_index:
        return ""

    positioned_words = []

    for word, positions in inverted_index.items():
        for position in positions:
            positioned_words.append((position, word))

    positioned_words.sort(key=lambda item: item[0])

    return " ".join(
        word
        for _, word in positioned_words
    )


def fetch_query_results(
    query_id: str,
    category: str,
    query: str,
    per_page: int,
    api_key: str | None,
) -> list[dict[str, Any]]:
    """Fetch one page of OpenAlex results and add query provenance."""
    params = {
        "search": query,
        "filter": (
            "from_publication_date:2018-01-01,"
            "to_publication_date:2026-12-31"
        ),
        "per-page": per_page,
    }

    if api_key:
        params["api_key"] = api_key

    response = requests.get(
        OPENALEX_WORKS_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    rows = []

    for rank, work in enumerate(response.json().get("results", []), start=1):
        rows.append(
            {
                "query_id": query_id,
                "category": category,
                "query": query,
                "rank": rank,
                "openalex_id": work.get("id") or "",
                "doi": work.get("doi") or "",
                "title": work.get("title") or "",
                "abstract": reconstruct_abstract(
                    work.get("abstract_inverted_index")
                ),
                "publication_year": work.get("publication_year") or "",
                "type": work.get("type") or "",
                "source": extract_source(work),
                "authors": extract_authors(work),
                "cited_by_count": work.get("cited_by_count") or 0,
            }
        )

    return rows


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    """Write retrieved records to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "query_id",
        "category",
        "query",
        "rank",
        "openalex_id",
        "doi",
        "title",
        "abstract",
        "publication_year",
        "type",
        "source",
        "authors",
        "cited_by_count",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the initial OpenAlex PFAS query matrix."
    )
    parser.add_argument(
        "--per-query",
        type=int,
        default=25,
        help="Number of results retrieved per query.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/openalex_query_results.csv"),
        help="CSV output path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.per_query < 1 or args.per_query > 200:
        raise ValueError("--per-query must be between 1 and 200")

    load_env_file(Path(".env"))
    api_key = os.getenv("OPENALEX_API_KEY")

    all_rows = []

    for query_id, details in QUERIES.items():
        print(
            f"Running {query_id}: "
            f"{details['category']} — {details['query']}"
        )

        rows = fetch_query_results(
            query_id=query_id,
            category=details["category"],
            query=details["query"],
            per_page=args.per_query,
            api_key=api_key,
        )

        all_rows.extend(rows)
        print(f"Retrieved {len(rows)} records.")

    write_csv(all_rows, args.output)

    print()
    print(f"Saved {len(all_rows)} records to {args.output}")


if __name__ == "__main__":
    main()
