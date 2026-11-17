"""Himalayas public remote-jobs API adapter (no key or account required).

Keep visible Himalayas attribution and use its applicationLink unchanged.
Do not redistribute these listings to other job boards or aggregators.
"""
from __future__ import annotations
import html
import re
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _plain_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\\s+", " ", html.unescape(value)).strip()


def search_himalayas(query: str, country: str = "India", page: int = 1) -> list[dict]:
    params = {"q": query, "country": country, "sort": "recent", "page": max(1, page)}
    url = "https://himalayas.app/jobs/api/search?" + urlencode(params)
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "ApplyPilot-AI/0.2"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Himalayas request failed: {exc}") from exc
    jobs = []
    for item in payload.get("jobs", []):
        restrictions = item.get("locationRestrictions") or []
        names = [entry.get("name", str(entry)) if isinstance(entry, dict) else str(entry) for entry in restrictions]
        worldwide = not restrictions
        location = ", ".join(names) if names else "Worldwide remote"
        jobs.append({
            "source": "Himalayas", "source_id": str(item.get("guid", "")),
            "title": item.get("title", ""), "company": item.get("companyName", ""),
            "location": location, "description": _plain_text(item.get("description") or item.get("excerpt", "")),
            "url": item.get("applicationLink", ""), "source_url": item.get("guid", ""),
            "posted_at": item.get("pubDate", ""), "employment_type": item.get("employmentType", ""),
            "seniority": "; ".join(item.get("seniority") or []), "remote": True,
            "worldwide": worldwide, "attribution": "Himalayas",
            "salary_min": item.get("minSalary"), "salary_max": item.get("maxSalary"),
            "salary_period": item.get("salaryPeriod"), "currency": item.get("currency"),
            "expiry_date": item.get("expiryDate"),
        })
    return jobs
