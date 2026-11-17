"""Himalayas public remote-jobs API adapter (no key or account required).

Attribution: keep the Himalayas source label and original listing link in the UI.
The provider asks clients not to republish its listings to other job aggregators.
"""
from __future__ import annotations
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json


def _plain_text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html or "")).strip()


def search_himalayas(query: str, country: str = "India", page: int = 1) -> list[dict]:
    params = {"q": query, "country": country, "sort": "recent", "page": max(1, page)}
    url = "https://himalayas.app/jobs/api/search?" + urlencode(params)
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "ApplyPilot-AI/0.2"})
    try:
        with urlopen(req, timeout=30) as response: payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Himalayas request failed: {exc}") from exc
    jobs=[]
    for item in payload.get("jobs", []):
        restrictions = item.get("locationRestrictions") or []
        worldwide = not restrictions
        loc = ", ".join(restrictions) if restrictions else "Worldwide remote"
        jobs.append({"source":"Himalayas", "source_id":str(item.get("guid", "")),
          "title":item.get("title", ""), "company":item.get("companyName", ""),
          "location":loc, "description":_plain_text(item.get("description") or item.get("excerpt", "")),
          "url":item.get("applicationLink") or item.get("guid", ""),
          "posted_at":item.get("pubDate", ""), "employment_type":item.get("employmentType", ""),
          "seniority":"; ".join(item.get("seniority") or []), "remote":True,
          "worldwide":worldwide, "attribution":"Himalayas"})
    return jobs
