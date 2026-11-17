"""Official Adzuna job search API adapter (requires free developer credentials)."""
from __future__ import annotations
import json, os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def search_adzuna(query: str, location: str = "India", page: int = 1, results_per_page: int = 20) -> list[dict]:
    app_id, app_key = os.getenv("ADZUNA_APP_ID"), os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        raise RuntimeError("Set ADZUNA_APP_ID and ADZUNA_APP_KEY in your environment. Get free API credentials at https://developer.adzuna.com/")
    params = {"app_id": app_id, "app_key": app_key, "what": query, "where": location,
              "results_per_page": min(max(results_per_page, 1), 50), "content-type": "application/json"}
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/{max(1,page)}?{urlencode(params)}"
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "ApplyPilot-AI/0.2"})
    try:
        with urlopen(req, timeout=25) as response: payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Adzuna request failed: {exc}") from exc
    jobs = []
    for item in payload.get("results", []):
        company = item.get("company") or {}
        loc = item.get("location") or {}
        jobs.append({"source":"Adzuna", "source_id":str(item.get("id", "")), "title":item.get("title", ""),
          "company":company.get("display_name", ""), "location":loc.get("display_name", ""),
          "description":item.get("description", ""), "url":item.get("redirect_url", ""),
          "posted_at":item.get("created", ""), "salary_min":item.get("salary_min"),
          "salary_max":item.get("salary_max"), "currency":item.get("salary_currency", "INR")})
    return jobs
