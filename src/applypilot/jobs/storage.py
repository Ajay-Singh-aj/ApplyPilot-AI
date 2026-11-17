"""Local SQLite storage for discovered job listings."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path


def save_jobs(jobs: list[dict], db_path: Path) -> int:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS jobs (source TEXT NOT NULL, source_id TEXT NOT NULL, url TEXT, title TEXT, company TEXT, location TEXT, score INTEGER, eligible INTEGER, payload TEXT NOT NULL, first_seen TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(source, source_id))""")
        count = 0
        for job in jobs:
            sid = job.get("source_id") or job.get("url") or (job.get("title", "") + job.get("company", ""))
            cur = db.execute("INSERT OR IGNORE INTO jobs(source,source_id,url,title,company,location,score,eligible,payload) VALUES(?,?,?,?,?,?,?,?,?)",
              (job.get("source", "manual"), str(sid), job.get("url"), job.get("title"), job.get("company"), job.get("location"), job.get("match_score", 0), int(bool(job.get("eligible"))), json.dumps(job, ensure_ascii=False)))
            count += cur.rowcount
    return count


def load_jobs(db_path: Path) -> list[dict]:
    if not db_path.exists(): return []
    with sqlite3.connect(db_path) as db:
        rows = db.execute("SELECT payload FROM jobs ORDER BY score DESC, first_seen DESC").fetchall()
    return [json.loads(row[0]) for row in rows]
