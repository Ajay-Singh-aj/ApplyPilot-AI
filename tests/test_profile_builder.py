from applypilot.profile.profile_builder import build_profile, extract_skills


def test_extract_skills_is_case_insensitive():
    assert extract_skills("Built models with PYTHON, pandas, and LightGBM.") == [
        "Python", "Pandas", "LightGBM"
    ]


def test_profile_keeps_experience_as_source_text():
    text = """Asha Kumar
asha@example.com

Technical Skills
Python, SQL, PyTorch

Work Experience
Data Analyst Intern | Example Corp
Worked with SQL and Python.
"""
    profile = build_profile(text)
    assert profile["personal"]["name"] == "Asha Kumar"
    assert profile["personal"]["email"] == "asha@example.com"
    assert profile["review_required"] is True
    assert any("Data Analyst Intern" in line for line in profile["experience_section"])
