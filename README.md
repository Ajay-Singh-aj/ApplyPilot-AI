# ApplyPilot AI

An open-source, privacy-first job-search assistant. It parses a local resume, discovers listings from permitted sources, ranks them transparently, and stores results locally.

> **Current milestone: Phase 2 — Job Discovery & Matching.** The default discovery source is the public Himalayas remote-jobs API and requires no API key or credit card. Adzuna remains an optional adapter if you already have credentials.

## Candidate targeting preset

India-wide search for AI/ML Engineer, Data Scientist, Data Analyst, GenAI Engineer, Python Developer and SDE-1 roles; 0–2 years required experience; remote and hybrid preferences. This is a job-search filter, not a claim about the candidate's employment duration.

## Features

- Extract PDF/DOCX resume text and build a reviewable local profile.
- Search public remote listings via Himalayas without API keys.
- Optional Adzuna adapter for users who already have API credentials.
- Explainable role, skill, experience and location matching.
- Save discovered jobs in local SQLite; no auto-application.

## Quick start (Windows PowerShell)

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python main.py parse-resume "C:\\path\\to\\resume.pdf"
python main.py show-profile
python main.py find-jobs
python main.py show-jobs
pytest -q
```

The default `find-jobs` uses the Himalayas public remote-jobs API and requires no signup, API key, or card. It is remote-focused, so it does not cover every onsite or hybrid India vacancy. Keep the source attribution and original listing URL visible, and follow the provider's current API terms: [Himalayas remote jobs API](https://github.com/Himalayas-App/remote-jobs-api).

Optional Adzuna: set `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` in your shell and run `python main.py find-jobs --source adzuna`.

## Privacy and safety

Keep `data/profile.json`, `data/resume_extracted.txt`, API keys, browser profiles and cookies out of Git. Review each job and its experience requirements on the employer's site. Use only permitted sources; do not bypass CAPTCHAs or access controls. Require human approval before any application submission.

## License

MIT. See [LICENSE](LICENSE).
