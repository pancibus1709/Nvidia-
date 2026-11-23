"""Shared helpers: paths, JSON IO, text rendering of cached sources, number parsing.

Text rendering rule (used by grounding): a cached source is stored raw. Its "text" is a
deterministic rendering (tags stripped, entities decoded, all whitespace collapsed to one
space). Quotes and locators always refer to that rendering, so the grounding check can
re-derive it from the raw cached bytes and re-find the quote.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "research" / "cache"
REGISTER = ROOT / "data" / "register"
PUBLISHED = ROOT / "data" / "published"
CONFIG = ROOT / "config"
SCHEMA = ROOT / "schema"


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    tmp.replace(path)


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@lru_cache(maxsize=1)
def enums() -> dict:
    return load_json(SCHEMA / "enums.json")


def allowlist() -> dict:
    return load_json(CONFIG / "sources_allowlist.json")


# ---------------------------------------------------------------- text rendering

_WS = re.compile(r"[\s  -​  　]+")
_DROP = re.compile(r"(?is)<(script|style|ix:header|head)\b.*?</\1\s*>")
_BLOCK = re.compile(r"(?i)</?(p|div|br|tr|li|h[1-6]|table|ul|ol|section|article|title|hr)\b[^>]*>")
_CELL = re.compile(r"(?i)</(td|th)\s*>")
_TAG = re.compile(r"(?s)<[^>]+>")
_COMMENT = re.compile(r"(?s)<!--.*?-->")


def norm(s: str) -> str:
    """Collapse every run of whitespace (including non-breaking spaces) to one space."""
    return _WS.sub(" ", s).strip()


def html_to_text(raw: str) -> str:
    s = _COMMENT.sub(" ", raw)
    s = _DROP.sub(" ", s)
    s = _BLOCK.sub(" ", s)
    s = _CELL.sub(" ", s)
    s = _TAG.sub("", s)
    s = html.unescape(s)
    return norm(s)


def render_text(path) -> str:
    """Deterministic text rendering of a cached file. JSON and plain text pass through."""
    path = Path(path)
    data = path.read_bytes()
    try:
        raw = data.decode("utf-8")
    except UnicodeDecodeError:
        raw = data.decode("latin-1")
    suffix = path.suffix.lower()
    head = raw[:2000].lower()
    if suffix in (".json",):
        return norm(raw)
    if suffix in (".htm", ".html", ".xml") or "<html" in head or "<document>" in head or "<?xml" in head:
        return html_to_text(raw)
    return norm(raw)


_text_cache: dict = {}


def doc_text(path) -> str:
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    key = (str(path), path.stat().st_mtime_ns)
    if key not in _text_cache:
        _text_cache.clear() if len(_text_cache) > 40 else None
        _text_cache[key] = render_text(path)
    return _text_cache[key]


def word_count(s: str) -> int:
    return len(norm(s).split())


# ---------------------------------------------------------------- domains and tiers

def domain_of(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def _match(host: str, dom: str) -> bool:
    return host == dom or host.endswith("." + dom)


def classify_domain(url: str, al: dict | None = None) -> dict:
    """Return {'tier': '1'|'2'|'market'|None, 'publisher':..., 'parent_company':..., 'group':...}."""
    al = al or allowlist()
    host = domain_of(url)
    for dom in al.get("excluded", []):
        if _match(host, dom):
            return {"tier": None, "reason": "excluded", "domain": host}
    for dom, meta in al.get("market_data", {}).items():
        if _match(host, dom):
            return {"tier": "market", "publisher": meta["publisher"], "parent_company": meta["publisher"], "group": "market_data", "domain": host}
    for dom, meta in al.get("tier2", {}).items():
        if _match(host, dom):
            return {"tier": "2", "publisher": meta["publisher"], "parent_company": meta["parent_company"], "group": "tier2", "domain": host}
    t1 = al.get("tier1", {})
    for group in ("sec", "regulators_courts", "lien_registries", "rating_agencies"):
        for dom in t1.get(group, []):
            if _match(host, dom):
                return {"tier": "1", "group": group, "domain": host}
    for ent, doms in t1.get("company_domains", {}).items():
        for dom in doms:
            if _match(host, dom):
                return {"tier": "1", "group": "company", "entity": ent, "domain": host}
    return {"tier": None, "reason": "not listed", "domain": host}


# ---------------------------------------------------------------- numbers

_SCALE_WORDS = {"thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12,
                "thousands": 1e3, "millions": 1e6, "billions": 1e9, "bn": 1e9, "mn": 1e6, "m": 1e6, "b": 1e9}
_NUM = re.compile(r"(?<![\w.])\(?\$?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\)?\s?(trillion|billion|million|thousand|bn|mn)?(?![\w])", re.I)
_TABLE_SCALE = re.compile(r"in\s+(thousands|millions|billions)", re.I)


def numbers_in(text: str) -> list[tuple[float, float | None]]:
    """Every number in text as (raw value, explicit scale or None)."""
    out = []
    for m in _NUM.finditer(text):
        raw = float(m.group(1).replace(",", ""))
        word = (m.group(2) or "").lower()
        out.append((raw, _SCALE_WORDS.get(word)))
    return out


def table_scale(text: str) -> float | None:
    m = _TABLE_SCALE.search(text)
    return _SCALE_WORDS[m.group(1).lower()] if m else None


def value_in_text(value: float, text: str, scale_hint: float | None = None, tol: float = 5e-4) -> bool:
    """True if `value` appears in `text` after unit normalisation.

    "$6.3 billion" matches 6.3e9. A bare table figure matches only through `scale_hint`
    (taken from the header at unit_scale_locator) or at face value.
    """
    if value is None:
        return False
    for raw, scale in numbers_in(text):
        cands = [raw * scale] if scale else [raw] + ([raw * scale_hint] if scale_hint else [])
        for c in cands:
            if value == c or (value != 0 and abs(c - value) <= tol * abs(value)):
                return True
    return False


BANNED_DASHES = "‒–—−"
