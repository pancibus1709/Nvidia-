"""Prices for Nvidia's listed holdings, market value only (spec/11 U1, spec/04 market data class).

  python3 -m pipeline.watchers.market_values [--since YYYY-MM-DD]

Source: Yahoo Finance quote data (the chart endpoint on an allowlisted market data domain), fetched
through pipeline.cache. For each relationship whose holding has a ticker, a share count above zero and
a listed instrument, the hit proposes market_value = shares held times the last regular market price,
with the price timestamp and source name. Each quote is kept as its own file under
research/cache/market/, so a later fetch never changes the file an earlier figure was grounded in.

This class supports market_value and nothing else. Prices not quoted in US dollars are skipped with a
warning, because no exchange rate is sourced here. `--since` has no effect: a quote is always the latest.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone

from .. import cache
from ..common import doc_text, sha256_file
from . import base

NAME = "market_values"
LOOKBACK_DAYS = 1
DEFAULT_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
SOURCE = "Yahoo Finance"
_PRICE = re.compile(r'"regularMarketPrice"\s*:\s*[0-9.]+')


def fetch_quote(ctx, ticker: str, url: str) -> dict:
    """Fetch one quote and keep an unchanging copy. Returns price, currency, timestamp and the kept file."""
    path = cache.fetch(url, refresh=True, user_agent="Mozilla/5.0")
    raw = path.read_bytes()
    meta = json.loads(raw)["chart"]["result"][0]["meta"]
    ts = datetime.fromtimestamp(int(meta["regularMarketTime"]), timezone.utc)
    keep_dir = ctx.paths.root / "research" / "cache" / "market"
    keep_dir.mkdir(parents=True, exist_ok=True)
    kept = keep_dir / f"{re.sub(r'[^A-Za-z0-9.]+', '_', ticker)}_{ts.strftime('%Y%m%dT%H%M%SZ')}.json"
    if not kept.exists():
        kept.write_bytes(raw)
        (kept.parent / (kept.name + ".meta.json")).write_text(json.dumps({"url": url, "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                                           "status": 200, "content_hash": sha256_file(kept)}, indent=2))
    return {"price": float(meta["regularMarketPrice"]), "currency": meta.get("currency"), "timestamp": ts, "path": kept, "url": url,
            "name": meta.get("longName") or meta.get("shortName") or ticker}


def evidence_for(ctx, q: dict, ticker: str, rel_id: str) -> dict:
    """A market data evidence record with a placeholder id; apply_approved gives it a real one."""
    text = doc_text(q["path"])
    m = _PRICE.search(text)
    if not m:
        raise ValueError("quote file has no regularMarketPrice")
    return {"id": "new:1", "tier": "market", "kind": "market_data", "publisher": SOURCE, "title": f"{ticker} quote, {q['name']}",
            "url": q["url"], "source_link": f"https://finance.yahoo.com/quote/{ticker}", "accession": None, "section": "regularMarketPrice",
            "published": q["timestamp"].strftime("%Y-%m-%d"), "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "quote": m.group(0), "locator": str(m.start()), "unit_scale_locator": None, "parent_company": SOURCE, "cites_publisher": [],
            "cache_path": str(q["path"].resolve().relative_to(ctx.paths.root.resolve())), "content_hash": sha256_file(q["path"]),
            "sourcing": "named", "paywalled": False, "supports": [f"{rel_id}.amounts.market_value"], "grounded_value": q["price"]}


def proposal(rel: dict, q: dict, ev: dict) -> list[dict]:
    """The diff for one holding. The new evidence record travels beside the diff, in the hit's `evidence` list.
    last_verified is never touched: no person re-checked anything."""
    shares = float(rel["holding"]["shares"])
    value = round(shares * q["price"], 2)
    stamp = q["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
    base_path = f"relationships/{rel['id']}/amounts/market_value"
    old = (rel.get("amounts") or {}).get("market_value")
    new_fields = {"value": value, "as_of": q["timestamp"].strftime("%Y-%m-%d"), "price_source": SOURCE, "price_timestamp": stamp,
                  "price": q["price"], "shares": shares, "evidence": ["new:1"],
                  "note": f"{shares:,.0f} shares held as of {rel['holding'].get('as_of') or 'an undisclosed date'}, at the last regular market price of {q['price']:,.2f} per share."}
    diff = []
    if isinstance(old, dict):
        diff += [{"path": f"{base_path}/{k}", "old": old.get(k), "new": v} for k, v in new_fields.items() if old.get(k) != v]
        if old.get("components"):
            diff.append({"path": f"{base_path}/components", "old": old["components"], "new": None})
    else:
        diff.append({"path": base_path, "old": None, "new": {"fiscal_period": None, "original_currency": "USD", "original_value": None, "fx_rate": None,
                                                              "fx_date": None, "last_verified": None, "display_eligible": False, "lower_bound": False, **new_fields}})
    return diff


def run(ctx):
    cfg = ctx.paths.cfg("watch_sources.json", {})
    tmpl = cfg.get("yahoo_chart_url", DEFAULT_URL)
    instruments = set(cfg.get("market_value_instruments", ["common"]))
    held = [r for r in ctx.relationships()
            if (r.get("holding") or {}).get("ticker") and (r["holding"].get("shares") or 0) > 0
            and (r["holding"].get("instrument") or "common") in instruments and r.get("status") != "terminated"]
    hits, failed, quotes = [], 0, {}
    for r in held:
        t = r["holding"]["ticker"]
        try:
            if t not in quotes:
                quotes[t] = fetch_quote(ctx, t, tmpl.format(ticker=t))
            q = quotes[t]
            if q["currency"] != "USD":
                ctx.warn(f"{t}: quoted in {q['currency']}; skipped because no exchange rate is sourced")
                continue
            ev = evidence_for(ctx, q, t, r["id"])
            diff = proposal(r, q, ev)
        except cache.SourceNotAllowed:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            quotes.setdefault(t, None)
            ctx.warn(f"{t}: {str(err)[:120]}")
            continue
        stamp = q["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
        hits.append(ctx.hit("market_value", f"{r['id']}|{stamp}|{r['holding']['shares']}", entity=r["to"], relationship=r["id"], ticker=t,
                            date=stamp[:10], source_url=q["url"], price=q["price"], currency="USD", price_timestamp=stamp, price_source=SOURCE,
                            shares=r["holding"]["shares"], shares_as_of=r["holding"].get("as_of"), value=round(float(r["holding"]["shares"]) * q["price"], 2),
                            title=f"{t} at {q['price']:,.2f} on {stamp[:10]}", evidence=[ev], diff=diff))
    if held and failed == len(held):
        raise base.AllSourcesFailed("no quote could be fetched")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
