from applypilot.profile.validators import validate_profile


def test_validator_requires_human_review():
    profile = {
        "personal": {"name": "Test User", "email": "test@example.com"},
        "skills": ["Python"],
        "experience_section": ["Analyst Intern"],
        "review_required": False,
    }
    assert any("candidate review" in error for error in validate_profile(profile))
