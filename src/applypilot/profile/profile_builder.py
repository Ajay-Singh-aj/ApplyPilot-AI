"""Conservative, reviewable profile extraction from resume text.

This module avoids guessing dates, seniority, or missing facts.
The output is a draft profile and must be reviewed by the candidate.
"""
from __future__ import annotations

import re
from typing import Any


KNOWN_SKILLS = [
    "Python", "SQL", "C++", "C", "NumPy", "Pandas", "Matplotlib",
    "scikit-learn", "XGBoost", "LightGBM", "SHAP", "PyTorch", "MySQL",
    "Presto", "FAISS", "Git", "GitHub", "Gemini", "RAG", "Transformers",
    "LangGraph", "FastAPI", "Playwright",
]

SECTION_HEADERS = {
    "education": ("education", "academic qualifications"),
    "experience": ("experience", "work experience", "employment"),
    "projects": ("projects", "key projects"),
    "skills": ("skills", "technical skills", "technologies"),
}


def _find_email(text: str) -> str | None:
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    return match.group(0) if match else None


def _find_phone(text: str) -> str | None:
    match = re.search(r"(?<!\w)(?:\+?\d[\d\s().-]{8,}\d)(?!\w)", text)
    return re.sub(r"\s+", " ", match.group(0)).strip() if match else None


def _find_name(text: str) -> str | None:
    for line in text.splitlines()[:8]:
        candidate = line.strip()
        if (
            candidate
            and len(candidate.split()) <= 5
            and not re.search(r"@|https?://|\d{4}", candidate)
            and not any(word in candidate.lower() for word in ("resume", "curriculum", "phone"))
        ):
            return candidate
    return None


def extract_skills(text: str) -> list[str]:
    lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lower):
            found.append(skill)
    return found


def _section_lines(text: str, section: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    aliases = SECTION_HEADERS[section]
    start = None
    for idx, line in enumerate(lines):
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        if normalized in aliases:
            start = idx + 1
            break
    if start is None:
        return []
    all_headers = {h for values in SECTION_HEADERS.values() for h in values}
    output = []
    for line in lines[start:]:
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        if normalized in all_headers:
            break
        output.append(line)
    return output


def build_profile(text: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "review_required": True,
        "personal": {
            "name": _find_name(text),
            "email": _find_email(text),
            "phone": _find_phone(text),
        },
        "skills": extract_skills(text),
        "education_section": _section_lines(text, "education"),
        "experience_section": _section_lines(text, "experience"),
        "projects_section": _section_lines(text, "projects"),
        "skills_section": _section_lines(text, "skills"),
        "source": {
            "parser": "pypdf/python-docx",
            "extraction_note": (
                "Section text is preserved as extracted. Review dates, titles, "
                "skills and contact details before using this profile."
            ),
        },
    }
