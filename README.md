# ApplyPilot AI

An open-source, privacy-first job-search assistant. ApplyPilot helps a candidate structure their resume, define job preferences, and prepare for later job-discovery and application workflows.

> **Current milestone: Phase 1 — Resume & Profile Intelligence.** This release parses a local PDF/DOCX resume, extracts text, builds a reviewable candidate profile, and stores preferences. It does not scrape job boards or submit applications.

## Candidate targeting preset

The example configuration is tuned for an India-wide search across:
- AI / ML Engineer, Data Scientist, Data Analyst, GenAI Engineer
- Python Developer, SDE-1, Applied Scientist, NLP / Research Engineer
- Entry-level to 2 years of required experience
- India, with remote and hybrid opportunities allowed

This is a search preference, not a claim about the candidate's employment duration. The system preserves the resume's actual dates and facts.

## Phase 1 features

- Extract text from PDF and DOCX resumes.
- Build a structured, editable profile (skills, education, experience, projects, contact fields).
- Keep personal resume data local; no resume is sent to an LLM in Phase 1.
- Store role, experience, and location preferences in JSON.
- CLI commands to parse, inspect, and validate a profile.

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
├── src/applypilot/
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
