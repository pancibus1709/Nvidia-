"""The page builder's reader-copy helpers. Fixtures are fictional; no real figure appears here."""
import re

from pipeline import build_site


def _site():
    s = object.__new__(build_site.Site)
    s.ev = {"ev_1": {}, "ev_2": {}}
    s.relmap = {"rel_example_bk_2025": {"title": "Example backstop"}}
    s.ents = {"ent_example": {"short_name": "Example"}}
    return s


def test_prose_turns_internal_ids_and_iso_dates_into_reader_copy():
    out = _site().prose("Signed 2026-03-09 (ev_1, ev_2); see rel_example_bk_2025 and ent_example under spec/05, also ev_2.")
    visible = re.sub(r"<[^>]+>", "", out)
    assert "9 March 2026" in visible and "2026-03-09" not in visible
    assert not re.search(r"\b(ev|rel|ent)_", visible) and "spec/" not in visible
    assert "Example backstop" in visible and visible.count("Source") == 2
    assert out.count('data-ev="ev_1 ev_2"') == 1 and out.count('data-ev="ev_2"') == 1


def test_prose_drops_citations_that_do_not_resolve():
    assert "data-ev" not in _site().prose("A claim (ev_999).")


def test_summary_sentence_gives_every_figure_a_chip():
    x = {"text": "It paid $5 billion and can name $1 billion.",
         "figures": [{"text": "$5 billion", "evidence": ["ev_1"]}, {"text": "$1 billion", "measure": "funded", "rels": ["rel_example_bk_2025"]}]}
    out = _site().sentence(x)
    assert out.count('class="chip"') == 2 and 'data-ev="ev_1"' in out and 'data-measure="funded"' in out
    assert re.sub(r"<[^>]+>", "", out).replace(" Sources", "").replace(" Source", "") == x["text"]


def test_short_dates_and_money():
    assert build_site.ds("2026-08-17") == "17 Aug 2026" and build_site.ds("2026-08") == "Aug 2026" and build_site.ds(None) == ""
    assert build_site.money_s(30_200_000_000) == "$30.2B" and "<span" in build_site.money_u(30_200_000_000)
