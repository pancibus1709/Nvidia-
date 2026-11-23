"""Formatting and the insight renderer. Numbers reach on-screen sentences only through here."""
from __future__ import annotations

import re

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty",
                "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion", "trillion",
                "half", "double", "triple", "dozen", "twice"}
CURRENCY_SYMBOLS = {"GBP": "\u00a3", "EUR": "\u20ac", "JPY": "\u00a5", "KRW": "\u20a9", "AUD": "A$", "CAD": "C$"}
PLACEHOLDER = re.compile(r"\{([a-z_.]+)(?::([a-z_]+))?\}")
AMOUNT_KEYS = ("headline", "committed_total", "funded", "contingent_max", "annual_obligation", "market_value", "carrying_value")


def money(v, currency="$") -> str:
    if v is None:
        return "Not disclosed"
    a = abs(v)
    if a >= 1e12:
        s, unit = a / 1e12, "trillion"
    elif a >= 1e9:
        s, unit = a / 1e9, "billion"
    elif a >= 1e6:
        s, unit = a / 1e6, "million"
    elif a >= 1e3:
        s, unit = a / 1e3, "thousand"
    else:
        return f"{'-' if v < 0 else ''}{currency}{a:,.0f}"
    txt = f"{s:.2f}" if s < 10 else f"{s:.1f}"
    txt = txt.rstrip("0").rstrip(".") if "." in txt else txt
    return f"{'-' if v < 0 else ''}{currency}{txt} {unit}"


def money_short(v) -> str:
    return money(v).replace(" trillion", "T").replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")


def date_long(d: str | None) -> str:
    if not d:
        return "Not disclosed"
    parts = d.split("-")
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    return f"{int(parts[2])} {MONTHS[int(parts[1]) - 1]} {parts[0]}"


def pct(v, digits=1) -> str:
    return "Not computable" if v is None else f"{v * 100:.{digits}f}%"


def amount_text(a: dict | None) -> str:
    """Display text for an amount object, applying the display rule."""
    if a is None:
        return "Not disclosed"
    if a.get("not_applicable"):
        return "Not applicable"
    if a.get("value") is None:
        if a.get("original_value") is not None and a.get("original_currency", "USD") != "USD":
            if not a.get("display_eligible"):
                return "Not confirmed"
            return money(a["original_value"], CURRENCY_SYMBOLS.get(a["original_currency"], a["original_currency"] + " "))
        return "Not disclosed"
    if not a.get("display_eligible"):
        return "Not confirmed"
    return (a["qualifier"] + " " if a.get("qualifier") else "") + money(a["value"])


def render_insight(template: str, rel: dict, entities: dict) -> tuple[str, list[str]]:
    """Fill placeholders from amounts, derived and dates. Returns (sentence, unresolved placeholders)."""
    unresolved = []

    def sub(m):
        key, mod = m.group(1), m.group(2)
        if key == "counterparty":
            ent = entities.get(rel["to"], {})
            return ent.get("short_name") or ent.get("name") or rel["to"]
        if key in AMOUNT_KEYS:
            a = rel["amounts"].get(key)
            t = amount_text(a)
            if t in ("Not disclosed", "Not confirmed", "Not applicable"):
                return {"Not disclosed": "an undisclosed amount", "Not confirmed": "an unconfirmed amount", "Not applicable": "no amount"}[t]
            return t
        if key in ("committed_unfunded", "gross_exposure"):
            v = (rel.get("derived") or {}).get(key)
            return money(v) if v is not None else "an undisclosed amount"
        if key.startswith("dates."):
            d = rel["dates"].get(key.split(".", 1)[1])
            if not d:
                return "an undisclosed date"
            if mod == "year":
                return d[:4]
            if mod == "month_year":
                return date_long(d[:7])
            return date_long(d)
        unresolved.append(m.group(0))
        return m.group(0)

    return PLACEHOLDER.sub(sub, template), unresolved


def template_number_violations(template: str) -> list[str]:
    bare = PLACEHOLDER.sub(" ", template)
    bad = []
    if re.search(r"\d", bare):
        bad.append("digit")
    for w in re.findall(r"[A-Za-z]+", bare):
        if w.lower() in NUMBER_WORDS:
            bad.append(w)
    return bad
