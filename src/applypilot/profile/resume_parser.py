"""Local PDF/DOCX resume text extraction."""
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SUPPORTED_SUFFIXES = {".pdf", ".docx"}


class ResumeParseError(ValueError):
    """Raised when a resume cannot be read or has no extractable text."""


def extract_resume_text(file_path: str | Path) -> str:
    path = Path(file_path).expanduser()
    if not path.exists() or not path.is_file():
        raise ResumeParseError(f"Resume file not found: {path}")
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ResumeParseError(
            f"Unsupported file type {suffix!r}. Please use PDF or DOCX."
        )

    try:
        if suffix == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            document = Document(str(path))
            paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
            table_text = [
                " | ".join(cell.text.strip() for cell in row.cells)
                for table in document.tables
                for row in table.rows
            ]
            text = "\n".join(paragraphs + table_text)
    except Exception as exc:
        raise ResumeParseError(f"Could not parse resume: {exc}") from exc

    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not cleaned:
        raise ResumeParseError(
            "No selectable text found. This may be a scanned PDF; OCR support can be added later."
        )
    return cleaned
