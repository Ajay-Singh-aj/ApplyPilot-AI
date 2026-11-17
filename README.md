# ApplyPilot AI

An open-source, privacy-first job-search assistant. ApplyPilot helps a candidate structure their resume, define job preferences, and prepare for later job-discovery and application workflows.

> **Current milestone: Phase 2 — Job Discovery & Matching.** In addition to local resume parsing, ApplyPilot can query the Adzuna India API, score listings against the candidate profile, and store results locally. It does not submit applications.

## Candidate targeting preset

The example configuration is tuned for an India-wide search across:
- AI / ML Engineer, Data Scientist, Data Analyst, GenAI Engineer
- Python Developer, SDE-1, Applied Scientist, NLP / Research Engineer
- Entry-level to 2 years of required experience
- India, with remote and hybrid opportunities allowed

This is a search preference, not a claim about the candidate's employment duration. The system preserves the resume's actual dates and facts.

## Phase 1 and Phase 2 features

- Extract text from PDF and DOCX resumes.
- Build a structured, editable profile (skills, education, experience, projects, contact fields).
- Keep personal resume data local; no resume is sent to an LLM in Phase 1.
- Store role, experience, and location preferences in JSON.
- CLI commands to parse, inspect, and validate a profile.\n- Search India job listings through the Adzuna API adapter.\n- Explainable skills/role/experience/location scoring and local SQLite storage.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python main.py parse-resume "/path/to/your_resume.pdf"
python main.py show-profile
python main.py validate-profile
pytest -q
```

The first command writes `data/profile.json` and `data/resume_extracted.txt`. Review these local files before using them in later phases. Do not commit them.

## Project structure

```text
ApplyPilot-AI/
├── config/
│   ├── job_roles.py
│   ├── locations.py
│   └── preferences.json
├── data/
│   └── .gitkeep
├── src/applypilot/\n│   ├── jobs/\n│   │   ├── adzuna.py\n│   │   ├── matcher.py\n│   │   └── storage.py
│   ├── profile/
│   │   ├── resume_parser.py
│   │   ├── profile_builder.py
│   │   └── validators.py
│   └── cli.py
├── tests/
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Privacy and security

- Keep the original resume, `data/profile.json`, API keys, browser profiles, and session cookies out of Git.
- `.gitignore` excludes personal data by default.
- Never put API keys in source code.
- Phase 1 does not require an LLM or paid API.
- Later phases should use official APIs, permitted feeds, or site-approved workflows. Do not bypass CAPTCHAs or access controls. Require candidate review before application submission.

## Roadmap

1. **Phase 1:** Resume parsing and candidate profile.
2. Phase 2: Job discovery from permitted sources.
3. Phase 3: Explainable job matching and ranking.
4. Phase 4: Tailored resume and cover-letter drafts.
5. Phase 5: Assisted form filling with validation and user approval.
6. Phase 6: Application tracking dashboard and scheduled searches.

## License

MIT. See `LICENSE`.
