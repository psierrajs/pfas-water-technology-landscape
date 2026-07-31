import os
from pathlib import Path

import requests


OPENALEX_URL = "https://api.openalex.org/works"


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


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    load_env_file(project_root / ".env")

    api_key = os.getenv("OPENALEX_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENALEX_API_KEY is missing. Add it to the local .env file."
        )

    params = {
        "search": "PFAS water treatment",
        "filter": "from_publication_date:2018-01-01,to_publication_date:2026-12-31",
        "per-page": 10,
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

    print(f"Retrieved {len(results)} records:\n")

    for index, work in enumerate(results, start=1):
        title = work.get("display_name", "Untitled")
        year = work.get("publication_year", "Unknown year")
        doi = work.get("doi") or "No DOI"

        print(f"{index}. {title}")
        print(f"   Year: {year}")
        print(f"   DOI: {doi}")
        print()


if __name__ == "__main__":
    main()
