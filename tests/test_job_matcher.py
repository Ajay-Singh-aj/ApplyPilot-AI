from applypilot.jobs.matcher import score_job, rank_jobs

PROFILE = {"skills": ["Python", "SQL", "LightGBM", "PyTorch"]}
PREFS = {"target_roles": ["Data Scientist", "AI Engineer"], "minimum_required_experience_years": 0,
         "maximum_required_experience_years": 2, "allow_remote": True, "allow_hybrid": True}

def test_relevant_india_job_scores_well():
    job = {"title":"Junior Data Scientist", "location":"Bengaluru, India", "description":"Python SQL LightGBM 0-2 years"}
    result = score_job(job, PROFILE, PREFS)
    assert result["eligible"] and result["match_score"] >= 60
    assert "Python" in result["matched_skills"]

def test_explicit_senior_experience_is_filtered():
    job = {"title":"Data Scientist", "location":"India", "description":"Requires 5+ years Python SQL"}
    assert not score_job(job, PROFILE, PREFS)["eligible"]

def test_unknown_experience_is_not_assumed():
    job = {"title":"AI Engineer", "location":"Remote", "description":"Build Python services"}
    result = score_job(job, PROFILE, PREFS)
    assert result["eligible"]
    assert "experience requirement not stated; verify manually" in result["match_reasons"]
