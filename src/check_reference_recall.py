import argparse
import os
from pathlib import Path

import requests


OPENALEX_URL = "https://api.openalex.org/works"
DEFAULT_QUERY = "PFAS water treatment"
DEFAULT_MAX_RESULTS = 500
PAGE_SIZE = 100


def load_env_file(env_path: Path) -> None:
    """Load simple KEY=VALUE pairs from a local .env file."""
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def normalise_doi(doi: str) -> str:
    """Return a normalised DOI URL for case-insensitive comparison."""
    doi = doi.strip().lower()

    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "doi:",
    ):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
            break

    return f"https://doi.org/{doi.strip()}"

def confirm_indexed(api_key: str, target_doi: str) -> bool:
    """Check whether a DOI exists in OpenAlex."""
    params = {
        "filter": f"doi:{target_doi}",
        "select": "id",
        "api_key": api_key,
    }

    response = requests.get(
        OPENALEX_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    return bool(response.json().get("results", []))


def find_doi_rank(
    api_key: str,
    target_doi: str,
    query: str,
    max_results: int,
) -> tuple[int | None, str | None]:
    """Find the position of a DOI within paginated search results."""
    cursor = "*"
    inspected = 0

    while inspected < max_results:
        remaining = max_results - inspected
        per_page = min(PAGE_SIZE, remaining)

        params = {
            "search": query,
            "filter": (
                "from_publication_date:2018-01-01,"
                "to_publication_date:2026-12-31"
            ),
            "per-page": per_page,
            "cursor": cursor,
            "api_key": api_key,
        }

        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        for work in results:
            inspected += 1

            if work.get("doi") == target_doi:
                return inspected, work.get("display_name")

        cursor = data.get("meta", {}).get("next_cursor")

        if not cursor:
            break

    return None, None


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check whether a DOI is indexed in OpenAlex and determine "
            "its rank for a search query."
        )
    )

    parser.add_argument(
        "doi",
        help="DOI with or without the https://doi.org/ prefix.",
    )

    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help=f"OpenAlex search query. Default: {DEFAULT_QUERY!r}",
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=(
            "Maximum number of ranked results to inspect. "
            f"Default: {DEFAULT_MAX_RESULTS}"
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.max_results < 1:
        raise ValueError("--max-results must be at least 1.")

    project_root = Path(__file__).resolve().parent.parent
    load_env_file(project_root / ".env")

    api_key = os.getenv("OPENALEX_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENALEX_API_KEY is missing. Add it to the local .env file."
        )

    target_doi = normalise_doi(args.doi)

    if not confirm_indexed(api_key, target_doi):
        print("DOI not found in OpenAlex.")
        return

    print("DOI is indexed in OpenAlex.")

    position, title = find_doi_rank(
        api_key=api_key,
        target_doi=target_doi,
        query=args.query,
        max_results=args.max_results,
    )

    if position is None:
        print(
            f"Not found within the first {args.max_results} results "
            f"for query: {args.query}"
        )
        return

    print(f"Found at position {position}.")
    print(f"Title: {title}")


if __name__ == "__main__":
    main()
