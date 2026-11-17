"""ApplyPilot AI entry point."""
import argparse

from applypilot.cli import parse_resume, show_profile, validate_saved_profile


def main() -> None:
    parser = argparse.ArgumentParser(description="ApplyPilot AI — Phase 1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_cmd = subparsers.add_parser("parse-resume", help="Extract a local PDF/DOCX resume")
    parse_cmd.add_argument("file", help="Path to your resume")

    subparsers.add_parser("show-profile", help="Print the locally saved draft profile")
    subparsers.add_parser("validate-profile", help="Run basic checks on the saved profile")

    args = parser.parse_args()
    if args.command == "parse-resume":
        parse_resume(args.file)
    elif args.command == "show-profile":
        show_profile()
    elif args.command == "validate-profile":
        validate_saved_profile()


if __name__ == "__main__":
    main()
