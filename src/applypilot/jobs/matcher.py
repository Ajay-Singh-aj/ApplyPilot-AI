"""Transparent, deterministic job filtering and scoring."""
from __future__ import annotations
import re

REMOTE_WORDS = ("remote", "work from home", "wfh")
HYBRID_WORDS = ("hybrid",)


def _text(job: dict) -> str:
    return " ".join(str(job.get(k, "") or "") for k in ("title", "description", "location", "employment_type")).lower()


def _experience_bounds(text: str):
    patterns = [r"(\\d+)\\s*[-–to]+\\s*(\\d+)\\s*(?:years?|yrs?)", r"(\\d+)\\+?\\s*(?:years?|yrs?)"]
    ranges = []
    for m in re.finditer(patterns[0], text): ranges.append((int(m.group(1)), int(m.group(2))))
    for m in re.finditer(patterns[1], text): ranges.append((int(m.group(1)), int(m.group(1))))
    return ranges


def score_job(job: dict, profile: dict, preferences: dict) -> dict:
    text = _text(job)
    skills = [s for s in profile.get("skills", []) if isinstance(s, str) and len(s) > 1]
    matched = sorted({s for s in skills if re.search(r"(?<![a-z0-9+#])" + re.escape(s.lower()) + r"(?![a-z0-9+#])", text)})
    roles = [r.lower() for r in preferences.get("target_roles", [])]
    title = str(job.get("title", "")).lower()
    role_match = any(r in title or title in r for r in roles)
    bounds = _experience_bounds(text)
    maximum = int(preferences.get("maximum_required_experience_years", 2))
    minimum = int(preferences.get("minimum_required_experience_years", 0))
    explicit_too_senior = any(lo > maximum or hi > maximum for lo, hi in bounds)
    explicit_too_experienced = any(hi < minimum for lo, hi in bounds)
    remote = any(w in text for w in REMOTE_WORDS)
    hybrid = any(w in text for w in HYBRID_WORDS)
    location = str(job.get("location", "")).lower()
    india = any(x in location for x in ("india", "bengaluru", "bangalore", "hyderabad", "mumbai", "pune", "delhi", "gurugram", "gurgaon", "noida", "chennai", "kolkata"))
    allowed_location = india or (remote and preferences.get("allow_remote", True))
    if remote and not preferences.get("allow_remote", True): allowed_location = False
    if hybrid and not preferences.get("allow_hybrid", True): allowed_location = False
    score = min(45, len(matched) * 7) + (30 if role_match else 0) + (15 if bounds and not explicit_too_senior else 7) + (10 if allowed_location else 0)
    reasons = []
    if role_match: reasons.append("target role match")
    if matched: reasons.append("skills: " + ", ".join(matched))
    if not bounds: reasons.append("experience requirement not stated; verify manually")
    if explicit_too_senior: reasons.append("likely exceeds configured experience limit")
    eligible = allowed_location and not explicit_too_senior and not explicit_too_experienced
    return {**job, "match_score": min(100, score), "matched_skills": matched,
            "experience_evidence": [f"{a}-{b} years" for a,b in bounds],
            "eligible": eligible, "match_reasons": reasons}


def rank_jobs(jobs: list[dict], profile: dict, preferences: dict) -> list[dict]:
    ranked = [score_job(j, profile, preferences) for j in jobs]
    return sorted(ranked, key=lambda x: (x["eligible"], x["match_score"]), reverse=True)
