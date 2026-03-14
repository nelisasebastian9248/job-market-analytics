"""Helpers for extracting skill mentions from job descriptions."""

from __future__ import annotations

import re


SKILL_PATTERNS = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b",
    "dbt": r"\bdbt\b",
    "spark": r"\bspark\b",
    "snowflake": r"\bsnowflake\b",
    "airflow": r"\bairflow\b",
    "tableau": r"\btableau\b",
    "power bi": r"\bpower\s?bi\b",
    "aws": r"\baws\b",
}


def extract_skills(description: str) -> list[str]:
    description_lower = description.lower()
    matches = [
        skill
        for skill, pattern in SKILL_PATTERNS.items()
        if re.search(pattern, description_lower)
    ]
    return sorted(matches)
