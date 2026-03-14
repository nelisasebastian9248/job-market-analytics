"""GitHub ingestion entry point."""

from __future__ import annotations

from typing import Any

import requests

from config.settings import load_settings


GITHUB_API_BASE_URL = "https://api.github.com/repos"


def fetch_github_repo_stats() -> list[dict[str, Any]]:
    settings = load_settings()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"

    repos: list[dict[str, Any]] = []
    for repository in settings.github_repositories:
        response = requests.get(
            f"{GITHUB_API_BASE_URL}/{repository}",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        repos.append(
            {
                "full_name": payload["full_name"],
                "stargazers_count": payload["stargazers_count"],
                "forks_count": payload["forks_count"],
                "open_issues_count": payload["open_issues_count"],
                "subscribers_count": payload["subscribers_count"],
                "default_branch": payload["default_branch"],
                "updated_at": payload["updated_at"],
            }
        )
    return repos


if __name__ == "__main__":
    repo_stats = fetch_github_repo_stats()
    print(f"Fetched stats for {len(repo_stats)} GitHub repositories.")
