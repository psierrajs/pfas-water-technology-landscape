from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_INPUT = Path(
    "data/processed/openalex_analysis_corpus.csv"
)

DEFAULT_OUTPUT = Path(
    "data/processed/openalex_authorships.csv"
)

DEFAULT_CACHE_DIR = Path(
    "data/raw/openalex_work_cache"
)

OPENALEX_API_URL = "https://api.openalex.org/works"

REQUEST_DELAY_SECONDS = 0.15
MAX_RETRIES = 4


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read the analysis corpus."""
    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalize_openalex_id(value: str) -> str:
    """Return the short OpenAlex identifier."""
    return (
        value.strip()
        .rstrip("/")
        .split("/")[-1]
    )


def build_request(
    openalex_id: str,
    email: str,
) -> Request:
    """Build an OpenAlex API request."""
    url = f"{OPENALEX_API_URL}/{openalex_id}"

    user_agent = (
        "PFAS-Water-Technology-Landscape"
    )

    if email:
        user_agent += f" (mailto:{email})"

    return Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/json",
        },
    )


def cache_path(
    cache_dir: Path,
    openalex_id: str,
) -> Path:
    """Return the cache file for an OpenAlex work."""
    return cache_dir / f"{openalex_id}.json"


def load_cached_work(
    path: Path,
) -> dict[str, Any] | None:
    """Load a cached OpenAlex work when available."""
    if not path.exists():
        return None

    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return None


def save_cached_work(
    work: dict[str, Any],
    path: Path,
) -> None:
    """Save an OpenAlex work response locally."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            work,
            file,
            ensure_ascii=False,
            indent=2,
        )

def fetch_work(
    openalex_id: str,
    email: str,
) -> dict[str, Any]:
    """Retrieve one work from OpenAlex with retries."""
    request = build_request(
        openalex_id,
        email,
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(
                request,
                timeout=30,
            ) as response:
                return json.load(response)

        except HTTPError as error:
            if (
                error.code == 429
                or 500 <= error.code < 600
            ):
                if attempt == MAX_RETRIES:
                    raise

                wait_seconds = attempt * 2
                print(
                    f"HTTP {error.code} for "
                    f"{openalex_id}; retrying in "
                    f"{wait_seconds}s"
                )
                time.sleep(wait_seconds)
                continue

            raise

        except URLError:
            if attempt == MAX_RETRIES:
                raise

            wait_seconds = attempt * 2
            print(
                f"Network error for {openalex_id}; "
                f"retrying in {wait_seconds}s"
            )
            time.sleep(wait_seconds)

    raise RuntimeError(
        f"Could not retrieve {openalex_id}"
    )


def get_work(
    openalex_id: str,
    email: str,
    cache_dir: Path,
) -> tuple[dict[str, Any], bool]:
    """Load a work from cache or retrieve it."""
    path = cache_path(
        cache_dir,
        openalex_id,
    )

    cached_work = load_cached_work(path)

    if cached_work is not None:
        return cached_work, True

    work = fetch_work(
        openalex_id,
        email,
    )
    save_cached_work(
        work,
        path,
    )

    time.sleep(REQUEST_DELAY_SECONDS)

    return work, False


def extract_authorship_rows(
    corpus_row: dict[str, str],
    work: dict[str, Any],
) -> list[dict[str, object]]:
    """Convert OpenAlex authorships into flat rows."""
    output_rows: list[dict[str, object]] = []

    authorships = work.get("authorships", [])

    for authorship_index, authorship in enumerate(
        authorships,
        start=1,
    ):
        author = authorship.get("author") or {}
        institutions = (
            authorship.get("institutions") or []
        )
        countries = authorship.get("countries") or []

        base_row: dict[str, object] = {
            "openalex_id": corpus_row.get(
                "openalex_id",
                "",
            ),
            "doi": corpus_row.get("doi", ""),
            "title": corpus_row.get("title", ""),
            "publication_year": corpus_row.get(
                "publication_year",
                "",
            ),
            "analysis_tier": corpus_row.get(
                "analysis_tier",
                "",
            ),
            "technology_labels": corpus_row.get(
                "technology_labels",
                "",
            ),
            "authorship_index": authorship_index,
            "author_position": authorship.get(
                "author_position",
                "",
            ),
            "is_corresponding": authorship.get(
                "is_corresponding",
                False,
            ),
            "author_id": author.get("id", ""),
            "author_name": author.get(
                "display_name",
                "",
            ),
            "author_orcid": author.get("orcid", ""),
            "raw_author_name": authorship.get(
                "raw_author_name",
                "",
            ),
            "authorship_countries": ";".join(
                sorted(set(countries))
            ),
        }

        if not institutions:
            row = dict(base_row)
            row.update(
                {
                    "institution_id": "",
                    "institution_name": "",
                    "institution_ror": "",
                    "institution_country_code": "",
                    "institution_type": "",
                    "raw_affiliations": "; ".join(
                        authorship.get(
                            "raw_affiliation_strings",
                            [],
                        )
                    ),
                }
            )
            output_rows.append(row)
            continue

        for institution in institutions:
            row = dict(base_row)
            row.update(
                {
                    "institution_id": institution.get(
                        "id",
                        "",
                    ),
                    "institution_name": institution.get(
                        "display_name",
                        "",
                    ),
                    "institution_ror": institution.get(
                        "ror",
                        "",
                    ),
                    "institution_country_code": (
                        institution.get(
                            "country_code",
                            "",
                        )
                    ),
                    "institution_type": institution.get(
                        "type",
                        "",
                    ),
                    "raw_affiliations": "; ".join(
                        authorship.get(
                            "raw_affiliation_strings",
                            [],
                        )
                    ),
                }
            )
            output_rows.append(row)

    return output_rows

def write_csv(
    rows: list[dict[str, object]],
    path: Path,
) -> None:
    """Write flattened authorship records."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "openalex_id",
        "doi",
        "title",
        "publication_year",
        "analysis_tier",
        "technology_labels",
        "authorship_index",
        "author_position",
        "is_corresponding",
        "author_id",
        "author_name",
        "author_orcid",
        "raw_author_name",
        "authorship_countries",
        "institution_id",
        "institution_name",
        "institution_ror",
        "institution_country_code",
        "institution_type",
        "raw_affiliations",
    ]

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Enrich the PFAS OpenAlex corpus with "
            "authorship, institution and country data."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_CACHE_DIR,
    )
    parser.add_argument(
        "--email",
        default="",
        help=(
            "Email address used in the OpenAlex "
            "User-Agent."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Optional number of corpus records to "
            "process for testing."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    corpus_rows = read_csv(args.input)

    if args.limit is not None:
        corpus_rows = corpus_rows[: args.limit]

    output_rows: list[dict[str, object]] = []

    cache_hits = 0
    fetched = 0
    failed = 0

    total = len(corpus_rows)

    for index, corpus_row in enumerate(
        corpus_rows,
        start=1,
    ):
        raw_id = corpus_row.get(
            "openalex_id",
            "",
        )
        openalex_id = normalize_openalex_id(raw_id)

        if not openalex_id:
            print(
                f"[{index}/{total}] Missing OpenAlex ID"
            )
            failed += 1
            continue

        try:
            work, from_cache = get_work(
                openalex_id,
                args.email,
                args.cache_dir,
            )

            if from_cache:
                cache_hits += 1
                source = "cache"
            else:
                fetched += 1
                source = "API"

            authorship_rows = extract_authorship_rows(
                corpus_row,
                work,
            )
            output_rows.extend(authorship_rows)

            print(
                f"[{index}/{total}] {openalex_id}: "
                f"{len(authorship_rows)} rows "
                f"from {source}"
            )

        except (
            HTTPError,
            URLError,
            OSError,
            json.JSONDecodeError,
        ) as error:
            failed += 1
            print(
                f"[{index}/{total}] Failed "
                f"{openalex_id}: {error}"
            )

    write_csv(
        output_rows,
        args.output,
    )

    print("\nEnrichment complete")
    print("-" * 40)
    print(f"Corpus records processed: {total}")
    print(f"Works fetched from API: {fetched}")
    print(f"Works loaded from cache: {cache_hits}")
    print(f"Failed works: {failed}")
    print(f"Authorship rows written: {len(output_rows)}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()  