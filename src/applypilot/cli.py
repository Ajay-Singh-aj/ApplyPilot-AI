"""Command-line interface for ApplyPilot Phase 1."""
from __future__ import annotations

import json
from pathlib import Path

from applypilot.profile.profile_builder import build_profile
from applypilot.profile.resume_parser import extract_resume_text
from applypilot.profile.validators import validate_profile


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROFILE_PATH = DATA_DIR / "profile.json"
RAW_TEXT_PATH = DATA_DIR / "resume_extracted.txt"


def parse_resume(file_path: str) -> None:
    text = extract_resume_text(file_path)
    profile = build_profile(text)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    RAW_TEXT_PATH.write_text(text, encoding="utf-8")
    print(f"Draft profile saved to: {PROFILE_PATH}")
    print("Review the generated profile before using it. Personal data stays local.")


def show_profile() -> None:
    if not PROFILE_PATH.exists():
        raise SystemExit("No profile found. Run: python main.py parse-resume <file>")
    print(PROFILE_PATH.read_text(encoding="utf-8"))


def validate_saved_profile() -> None:
    if not PROFILE_PATH.exists():
        raise SystemExit("No profile found. Run: python main.py parse-resume <file>")
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    errors = validate_profile(profile)
    if errors:
        print("Profile needs review:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Basic profile checks passed. Human review is still required.")
