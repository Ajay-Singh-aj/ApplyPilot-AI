"""Command-line interface for ApplyPilot AI."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from applypilot.profile.profile_builder import build_profile
from applypilot.profile.resume_parser import extract_resume_text
from applypilot.profile.validators import validate_profile
from applypilot.jobs.adzuna import search_adzuna
from applypilot.jobs.matcher import rank_jobs
from applypilot.jobs.storage import save_jobs, load_jobs

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROFILE_PATH = DATA_DIR / "profile.json"
RAW_TEXT_PATH = DATA_DIR / "resume_extracted.txt"
PREFERENCES_PATH = PROJECT_ROOT / "config" / "preferences.json"
DB_PATH = DATA_DIR / "applypilot.db"

def parse_resume(file_path: str) -> None:
    text = extract_resume_text(file_path); profile = build_profile(text)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    RAW_TEXT_PATH.write_text(text, encoding="utf-8")
    print(f"Draft profile saved to: {PROFILE_PATH}")
    print("Review the generated profile before using it. Personal data stays local.")

def show_profile() -> None:
    if not PROFILE_PATH.exists(): raise SystemExit("No profile found. Run: python main.py parse-resume <file>")
    print(PROFILE_PATH.read_text(encoding="utf-8"))

def validate_saved_profile() -> None:
    if not PROFILE_PATH.exists(): raise SystemExit("No profile found. Run: python main.py parse-resume <file>")
    errors = validate_profile(json.loads(PROFILE_PATH.read_text(encoding="utf-8")))
    if errors:
        print("Profile needs review:"); [print(f"- {e}") for e in errors]; raise SystemExit(1)
    print("Basic profile checks passed. Human review is still required.")

def find_jobs(query: str, location: str, page: int, limit: int) -> None:
    if not PROFILE_PATH.exists(): raise SystemExit("Parse your resume first: python main.py parse-resume <file>")
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    preferences = json.loads(PREFERENCES_PATH.read_text(encoding="utf-8"))
    print(f"Searching Adzuna India for: {query} | location: {location}")
    jobs = search_adzuna(query=query, location=location, page=page, results_per_page=limit)
    ranked = rank_jobs(jobs, profile, preferences)
    inserted = save_jobs(ranked, DB_PATH)
    print(f"Retrieved {len(jobs)} jobs; saved {inserted} new listings to {DB_PATH}")
    for i, job in enumerate(ranked[:15], 1):
        status = "MATCH" if job["eligible"] else "REVIEW/FILTERED"
        print(f"\\n{i}. [{status}] {job['match_score']}/100 — {job.get('title')} | {job.get('company')}")
        print(f"   {job.get('location')} | {job.get('url')}")
        print(f"   Skills: {', '.join(job.get('matched_skills', [])) or 'none detected'}")
        print(f"   Notes: {'; '.join(job.get('match_reasons', []))}")
    print("\\nVerify each listing and its experience requirement on the employer's site before applying.")

def show_jobs() -> None:
    jobs = load_jobs(DB_PATH)
    if not jobs: print("No saved jobs yet. Run: python main.py find-jobs"); return
    for i, job in enumerate(jobs, 1):
        print(f"{i}. [{ 'MATCH' if job.get('eligible') else 'REVIEW' }] {job.get('match_score',0)}/100 — {job.get('title')} | {job.get('company')} | {job.get('location')}")
        print(f"   {job.get('url')}")

def main() -> None:
    parser = argparse.ArgumentParser(description="ApplyPilot AI — resume and job matching")
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("parse-resume"); p.add_argument("file")
    subs.add_parser("show-profile"); subs.add_parser("validate-profile")
    j = subs.add_parser("find-jobs"); j.add_argument("--query", default="AI Engineer OR Machine Learning Engineer OR Data Scientist OR Data Analyst OR SDE 1"); j.add_argument("--location", default="India"); j.add_argument("--page", type=int, default=1); j.add_argument("--limit", type=int, default=20)
    subs.add_parser("show-jobs")
    args = parser.parse_args()
    if args.command == "parse-resume": parse_resume(args.file)
    elif args.command == "show-profile": show_profile()
    elif args.command == "validate-profile": validate_saved_profile()
    elif args.command == "find-jobs": find_jobs(args.query, args.location, args.page, args.limit)
    elif args.command == "show-jobs": show_jobs()

if __name__ == "__main__": main()
