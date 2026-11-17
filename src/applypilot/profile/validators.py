"""Basic checks for a candidate profile draft."""
from typing import Any


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    personal = profile.get("personal", {})
    if not personal.get("name"):
        errors.append("Candidate name was not detected; add it manually.")
    if not personal.get("email"):
        errors.append("Email was not detected; add it manually.")
    if not profile.get("skills") and not profile.get("skills_section"):
        errors.append("No skills were detected; review the resume text.")
    if not profile.get("experience_section"):
        errors.append("Experience section was not detected; verify section headings.")
    if profile.get("review_required") is not True:
        errors.append("Profile must remain marked for candidate review.")
    return errors
