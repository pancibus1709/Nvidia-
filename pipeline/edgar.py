"""SEC EDGAR client.

- User-Agent comes from the environment variable SEC_USER_AGENT. It is never stored in the repository.
- Requests are throttled to at most 8 per second across every process on this machine (file lock).
- Every response is cached under research/cache/ with its retrieval timestamp, so nothing is fetched twice.

CLI:
  python3 -m pipeline.edgar filings --cik 1045810 --forms 10-K,10-Q --since 2023-01-01
  python3 -m pipeline.edgar index --cik 1045810 --accession 0001045810-25-000023
  python3 -m pipeline.edgar get <sec url>
  python3 -m pipeline.edgar search '"NVIDIA" "backstop"' --forms 8-K,10-Q --start 2023-01-01 --end 2026-11-23
  python3 -m pipeline.edgar cik "CoreWeave"
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse

import requests

from .common import CACHE, ROOT, sha256_file

MIN_INTERVAL = 1.0 / 8.0
API_DIR = CACHE / "_api"          # index and search responses: reproducible, not committed
SEC_DIR = CACHE / "sec"           # filings and XBRL facts: committed, used for grounding
NVIDIA_CIK = "0001045810"


class SecConfigError(RuntimeError):
    pass


def user_agent() -> str:
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if not ua:
        # fallback: a one-line file in the home directory, outside the repository
        f = Path.home() / ".config" / "sec_user_agent"
        if f.exists():
            ua = f.read_text().strip()
    if not ua:
        raise SecConfigError(
            "SEC_USER_AGENT is not set. SEC.gov requires a declared contact (name and email). "
            "Set it in the environment; it is never written to the repository.")
    return ua


def _throttle():
    API_DIR.mkdir(parents=True, exist_ok=True)
    lock = API_DIR / ".throttle"
    with open(lock, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        try:
            last = float(fh.read().strip() or 0)
        except ValueError:
            last = 0.0
        wait = MIN_INTERVAL - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
        fh.seek(0)
        fh.truncate()
        fh.write(repr(time.time()))
        fh.flush()
        fcntl.flock(fh, fcntl.LOCK_UN)


def cache_path_for(url: str) -> Path:
    u = urlparse(url)
    host = u.hostname or ""
    m = re.match(r"/Archives/edgar/data/(\d+)/(\d{18})/(.+)$", u.path)
    if host.endswith("sec.gov") and m and not m.group(3).endswith("index.json"):
        return SEC_DIR / m.group(1) / m.group(2) / m.group(3).replace("/", "_")
    m = re.match(r"/api/xbrl/companyfacts/(CIK\d+\.json)$", u.path)
    if m:
        return SEC_DIR / "xbrl" / m.group(1)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", (u.path + ("?" + u.query if u.query else "")).strip("/"))[:180]
    return API_DIR / host / (name or "index")


def get(url: str, max_age_hours: float | None = None, retries: int = 4) -> Path:
    """Fetch a SEC URL through the cache. Returns the cached file path."""
    path = cache_path_for(url)
    meta = Path(str(path) + ".meta.json")
    if path.exists() and meta.exists():
        if max_age_hours is None:
            return path
        age = time.time() - path.stat().st_mtime
        if age < max_age_hours * 3600:
            return path
    headers = {"User-Agent": user_agent(), "Accept-Encoding": "gzip, deflate"}
    last_err = None
    for attempt in range(retries):
        _throttle()
        try:
            r = requests.get(url, headers=headers, timeout=60)
        except requests.RequestException as e:
            last_err = e
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 200:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(r.content)
            meta.write_text(json.dumps({
                "url": url,
                "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": 200,
                "content_hash": sha256_file(path),
            }, indent=2))
            return path
        last_err = RuntimeError(f"HTTP {r.status_code} for {url}")
        if r.status_code in (403, 429, 500, 502, 503):
            time.sleep(2 ** attempt + 1)
            continue
        break
    raise last_err


def meta_for(path) -> dict:
    p = Path(str(path) + ".meta.json")
    return json.loads(p.read_text()) if p.exists() else {}


def get_json(url: str, max_age_hours: float | None = None):
    return json.loads(get(url, max_age_hours).read_text())


def pad(cik) -> str:
    return str(cik).lstrip("0").zfill(10)


def submissions(cik, max_age_hours: float | None = 12) -> dict:
    return get_json(f"https://data.sec.gov/submissions/CIK{pad(cik)}.json", max_age_hours)


def list_filings(cik, forms=None, since=None, until=None, max_age_hours: float | None = 12) -> list[dict]:
    """Every filing for a CIK (recent plus older pages), newest first."""
    sub = submissions(cik, max_age_hours)
    blocks = [sub["filings"]["recent"]]
    for f in sub["filings"].get("files", []):
        if since and f.get("filingTo", "9999") < since:
            continue
        blocks.append(get_json(f"https://data.sec.gov/submissions/{f['name']}", max_age_hours))
    out = []
    for b in blocks:
        for i, acc in enumerate(b["accessionNumber"]):
            row = {
                "cik": pad(cik), "accession": acc, "form": b["form"][i], "filed": b["filingDate"][i],
                "report_date": b["reportDate"][i], "primary_doc": b["primaryDocument"][i],
                "description": b.get("primaryDocDescription", [""] * (i + 1))[i],
                "items": b.get("items", [""] * (i + 1))[i],
            }
            if forms and row["form"] not in forms:
                continue
            if since and row["filed"] < since:
                continue
            if until and row["filed"] > until:
                continue
            row["url"] = doc_url(cik, acc, row["primary_doc"]) if row["primary_doc"] else None
            out.append(row)
    out.sort(key=lambda r: r["filed"], reverse=True)
    return out


def doc_url(cik, accession: str, filename: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{int(str(cik))}/{accession.replace('-', '')}/{filename}"


def filing_index(cik, accession: str) -> list[dict]:
    """Documents in a filing: name, type, size."""
    url = f"https://www.sec.gov/Archives/edgar/data/{int(str(cik))}/{accession.replace('-', '')}/index.json"
    items = get_json(url)["directory"]["item"]
    return [{"name": i["name"], "type": i.get("type", ""), "size": i.get("size", ""),
             "url": doc_url(cik, accession, i["name"])} for i in items]


def fulltext_search(query: str, forms=None, start=None, end=None, offset: int = 0, max_age_hours: float | None = 24) -> dict:
    """EDGAR full-text search (the API behind sec.gov/edgar/search). 100 hits per page."""
    params = {"q": query}
    if forms:
        params["forms"] = ",".join(forms)
    if start or end:
        params.update({"dateRange": "custom", "startdt": start or "2001-01-01", "enddt": end or datetime.now().strftime("%Y-%m-%d")})
    if offset:
        params["from"] = offset
    return get_json("https://efts.sec.gov/LATEST/search-index?" + urlencode(params), max_age_hours)


def hit_to_row(hit: dict) -> dict:
    src = hit["_source"]
    acc, _, fname = hit["_id"].partition(":")
    cik = (src.get("ciks") or [""])[0]
    return {"accession": acc, "file": fname, "cik": cik, "names": src.get("display_names", []),
            "form": src.get("form") or src.get("root_forms", [""])[0], "filed": src.get("file_date"),
            "file_type": src.get("file_type"), "url": doc_url(cik, acc, fname) if cik else None}


def find_cik(name: str) -> list[dict]:
    """Look up CIKs by company name using EDGAR's company tickers file plus full-text entity hints."""
    data = get_json("https://www.sec.gov/files/company_tickers.json", 24 * 7)
    q = name.lower()
    hits = [{"cik": pad(v["cik_str"]), "ticker": v["ticker"], "name": v["title"]} for v in data.values() if q in v["title"].lower() or q == v["ticker"].lower()]
    return hits


def rel(path) -> str:
    return str(Path(path).resolve().relative_to(ROOT))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("filings"); a.add_argument("--cik", required=True); a.add_argument("--forms"); a.add_argument("--since"); a.add_argument("--until")
    a = sp.add_parser("index"); a.add_argument("--cik", required=True); a.add_argument("--accession", required=True)
    a = sp.add_parser("get"); a.add_argument("url")
    a = sp.add_parser("search"); a.add_argument("query"); a.add_argument("--forms"); a.add_argument("--start"); a.add_argument("--end"); a.add_argument("--offset", type=int, default=0)
    a = sp.add_parser("cik"); a.add_argument("name")
    args = ap.parse_args(argv)
    if args.cmd == "filings":
        forms = set(args.forms.split(",")) if args.forms else None
        for r in list_filings(args.cik, forms, args.since, args.until):
            print(f"{r['filed']}  {r['form']:<10} {r['accession']}  {r['report_date'] or '-':<10}  {r['items'] or '':<18} {r['url']}")
    elif args.cmd == "index":
        for d in filing_index(args.cik, args.accession):
            print(f"{d['size']:>10}  {d['name']:<50} {d['url']}")
    elif args.cmd == "get":
        p = get(args.url)
        print(rel(p))
    elif args.cmd == "search":
        res = fulltext_search(args.query, args.forms.split(",") if args.forms else None, args.start, args.end, args.offset)
        total = res["hits"]["total"]["value"]
        print(f"# total hits: {total}")
        for h in res["hits"]["hits"]:
            r = hit_to_row(h)
            print(f"{r['filed']}  {r['form']:<8} {r['accession']}  {(r['names'] or ['?'])[0][:45]:<45} {r['url']}")
    elif args.cmd == "cik":
        for h in find_cik(args.name):
            print(h)


if __name__ == "__main__":
    try:
        main()
    except SecConfigError as e:
        sys.exit(str(e))
