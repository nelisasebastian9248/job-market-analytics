"""Adzuna ingestion entry point."""

from __future__ import annotations

from typing import Any

import requests

from config.settings import load_settings


ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def fetch_adzuna_jobs(
    *,
    results_per_page: int = 25,
    page: int = 1,
    what: str = "data",
) -> dict[str, Any]:
    settings = load_settings()
    if not settings.adzuna_app_id or not settings.adzuna_api_key:
        raise ValueError("Missing Adzuna credentials in environment variables.")

    endpoint = (
        f"{ADZUNA_BASE_URL}/{settings.adzuna_country}/search/{page}"
        f"?app_id={settings.adzuna_app_id}"
        f"&app_key={settings.adzuna_api_key}"
        f"&results_per_page={results_per_page}"
        f"&what={what}"
        "&content-type=application/json"
    )
    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_adzuna_jobs_multi_page(
    *,
    results_per_page: int = 25,
    pages: int = 4,
    what: str = "data engineer",
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        payload = fetch_adzuna_jobs(
            results_per_page=results_per_page,
            page=page,
            what=what,
        )
        jobs.extend(payload.get("results", []))
    return jobs


def fetch_adzuna_jobs_for_roles(
    *,
    roles: tuple[str, ...] = ("data engineer", "analytics engineer"),
    results_per_page: int = 25,
    pages_per_role: int = 4,
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for role in roles:
        jobs.extend(
            fetch_adzuna_jobs_multi_page(
                results_per_page=results_per_page,
                pages=pages_per_role,
                what=role,
            )
        )
    return jobs


if __name__ == "__main__":
    jobs = fetch_adzuna_jobs_for_roles()
    print(f"Fetched {len(jobs)} Adzuna jobs.")
