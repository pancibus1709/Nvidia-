"""Local review page for the queue (spec/11 U3). `make review` runs this.

  python3 -m pipeline.review                    open http://127.0.0.1:8765 and review the queue
  python3 -m pipeline.review --port 9000 --reviewer "Thomas" --no-git --no-browser
  python3 -m pipeline.review --auto             approve by rule what config/auto_approve.json allows (used by triage.yml)
  python3 -m pipeline.review --list             print the queue

The page lists every queue item with its summary, the current and proposed values side by side,
evidence links and quotes, check results and critic notes. Actions: Approve, Edit then approve,
Reject with reason, Hold. Re-verification items where nothing moved are confirmed together on the
batch confirm screen. A paywalled article waits as "needs quote" until the sentence is pasted.

Approve writes data/approved/<id>.json and commits it; pushing that commit starts publish.yml.
Only an item whose checks all pass can be approved. Nothing here writes to data/register or data/published.
The server listens on this machine only and every action carries a one-time session token.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import secrets
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import triage
from .common import load_json, norm, sha256_file, word_count
from .update_common import Paths, get_path, load_collections, needs_human, now_iso, queue_items, save_item, touched_amounts

APPROVABLE = ("ready",)


# ---------------------------------------------------------------- actions (also used by tests and the workflows)

def rechecked_amounts(item: dict) -> list[str]:
    """Amount objects the diff touches: the ones a person approving this item has re-checked."""
    return touched_amounts(item.get("diff", []))


def _git(paths: Paths, message: str, git: bool) -> None:
    if not git or not (paths.root / ".git").exists():
        return
    subprocess.run(["git", "add", "-A", "data/approved", "data/queue", "data/inbox"], cwd=paths.root, check=False)
    subprocess.run(["git", "commit", "-q", "-m", message, "--", "data/approved", "data/queue", "data/inbox"], cwd=paths.root, check=False)


def approve(item_id: str, paths: Paths | None = None, by: str | None = None, mode: str = "human", edited_diff: list | None = None,
            rechecked: list | None = None, git: bool = False) -> dict:
    """Move a queue item to data/approved/. Raises ValueError if it may not be approved."""
    paths = paths or Paths()
    f = paths.queue / f"{item_id}.json"
    if not f.exists():
        raise ValueError(f"{item_id} is not in the queue")
    item = load_json(f)
    if edited_diff is not None:
        item["diff"] = edited_diff
        item["edited"] = True
        if item.get("state") != "hold":
            item["state"] = "ready"
        triage.finalize(item, paths)
        save_item(paths.queue, item)
    if item["state"] not in APPROVABLE:
        raise ValueError(f"{item_id} is '{item['state']}' and cannot be approved")
    if any(c["result"] == "fail" for c in item.get("checks", [])):
        raise ValueError(f"{item_id} has a failed check and cannot be approved")
    human, why = needs_human(item, paths.cfg("auto_approve.json", {"auto": []}))
    if mode == "auto":
        if human:
            raise ValueError(f"{item_id} needs a person: {why}")
        record = {"mode": "auto", "by": None, "rule": item["change_type"], "at": now_iso(), "rechecked": []}
    else:
        if not by:
            raise ValueError("an approval needs the approver's name")
        record = {"mode": "human", "by": by, "rule": None, "at": now_iso(), "edited": bool(item.get("edited")),
                  "rechecked": rechecked_amounts(item) if rechecked is None else rechecked}
    item["approval_record"] = record
    paths.approved.mkdir(parents=True, exist_ok=True)
    save_item(paths.approved, item)
    f.unlink()
    _git(paths, f"Approve {item_id}: {item['summary'][:60]}", git)
    return item


def reject(item_id: str, reason: str, paths: Paths | None = None, by: str | None = None, git: bool = False) -> dict:
    paths = paths or Paths()
    if not reason.strip():
        raise ValueError("a rejection needs a reason")
    f = paths.queue / f"{item_id}.json"
    item = load_json(f)
    item.update({"state": "rejected", "rejection": {"reason": reason.strip(), "by": by, "at": now_iso()}})
    paths.rejected.mkdir(parents=True, exist_ok=True)
    save_item(paths.rejected, item)
    f.unlink()
    _git(paths, f"Reject {item_id}", git)
    return item


def hold(item_id: str, paths: Paths | None = None, release: bool = False) -> dict:
    paths = paths or Paths()
    item = load_json(paths.queue / f"{item_id}.json")
    if release:
        item["state"] = "ready" if item.get("diff") else "needs extraction"
        triage.finalize(item, paths)
    else:
        item["state"] = "hold"
    save_item(paths.queue, item)
    return item


def paste_quote(item_id: str, sentence: str, quote: str, paths: Paths | None = None) -> dict:
    """A reviewer pastes the sentence from a paywalled article. It is cached as the grounding window and grounded like any source."""
    paths = paths or Paths()
    item = load_json(paths.queue / f"{item_id}.json")
    sentence, quote = norm(sentence), norm(quote or sentence)
    if not sentence:
        raise ValueError("paste the sentence from the article")
    if quote not in sentence:
        raise ValueError("the quote must appear word for word inside the pasted sentence")
    if word_count(quote) >= 15:
        raise ValueError("the quote must be under fifteen words; give the shorter passage that carries the figure")
    url = item["source"]["url"]
    from .common import classify_domain
    info = classify_domain(url)
    if info.get("tier") != "2":
        raise ValueError("pasting a quote is only for tier 2 articles")
    wdir = paths.root / "research" / "cache" / "news"
    wdir.mkdir(parents=True, exist_ok=True)
    wpath = wdir / (hashlib.sha256((url + quote).encode()).hexdigest()[:20] + ".txt")
    wpath.write_text(sentence[:600 + len(quote)], encoding="utf-8")
    n = len([e for e in item.get("evidence", []) if str(e.get("id", "")).startswith("new:")]) + 1
    item.setdefault("evidence", []).append({
        "id": f"new:{n}", "tier": "2", "kind": "news", "publisher": info["publisher"], "title": item["source"].get("title") or "Article",
        "url": url, "accession": None, "section": "", "published": item["source"].get("date") or now_iso()[:10], "retrieved": now_iso(),
        "quote": quote, "locator": str(sentence.find(quote)), "unit_scale_locator": None, "parent_company": info["parent_company"],
        "cites_publisher": [], "cache_path": str(wpath.resolve().relative_to(paths.root.resolve())), "content_hash": sha256_file(wpath),
        "sourcing": "anonymous", "paywalled": True, "pasted_by_reviewer": True, "supports": []})
    item["state"] = "needs extraction"
    item["checks"] = [{"check": "proposal", "result": "pending", "detail": f"quote pasted and cached as new:{n}; the change still has to be drafted (Edit then approve, or the extraction job)"}]
    save_item(paths.queue, item)
    return item


def auto_approve(paths: Paths | None = None, git: bool = False) -> list[str]:
    """Approve by rule every ready item the auto rule covers. Everything else waits for a person."""
    paths = paths or Paths()
    done = []
    for item in queue_items(paths):
        if item.get("state") == "ready" and not item.get("needs_human"):
            try:
                approve(item["id"], paths, mode="auto", git=False)
                done.append(item["id"])
            except ValueError as err:
                print(f"not auto-approved: {err}", file=sys.stderr)
    if done:
        _git(paths, f"Auto-approve {len(done)} item(s) by rule", git)
    return done


def batch_items(paths: Paths) -> list[dict]:
    return [i for i in queue_items(paths) if i.get("batch_confirm") and i.get("state") == "ready"]


def batch_confirm(paths: Paths | None = None, by: str | None = None, ids: list | None = None, git: bool = False) -> list[str]:
    paths = paths or Paths()
    done = []
    for item in batch_items(paths):
        if ids is not None and item["id"] not in ids:
            continue
        approve(item["id"], paths, by=by, git=False)
        done.append(item["id"])
    if done:
        _git(paths, f"Confirm {len(done)} re-verification item(s)", git)
    return done


# ---------------------------------------------------------------- page

CSS = """
*{box-sizing:border-box} body{font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#f6f6f3;color:#1a1a1a}
header{background:#111;color:#fff;padding:14px 24px;display:flex;gap:24px;align-items:baseline;flex-wrap:wrap}
header a{color:#cfe3ff} main{max-width:1180px;margin:0 auto;padding:20px 24px 80px}
.item{background:#fff;border:1px solid #dcdcd4;border-radius:8px;margin:0 0 20px;padding:18px 20px}
.item h2{font-size:17px;margin:0 0 6px} .meta{color:#555;font-size:13px;margin-bottom:10px}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;background:#e8e8e2;margin-right:6px}
.tag.ready{background:#d9f0dc}.tag.fail{background:#f7d4d0}.tag.wait{background:#fbeccb}.tag.human{background:#dfe6fb}
table{border-collapse:collapse;width:100%;margin:8px 0;table-layout:fixed} th,td{border:1px solid #e2e2da;padding:6px 8px;text-align:left;vertical-align:top;font-size:13px;word-wrap:break-word}
th{background:#f1f1ec} td.old{background:#fdf1ef} td.new{background:#eef8ef} code,pre{font:12px/1.45 ui-monospace,Menlo,monospace}
pre{white-space:pre-wrap;margin:0;max-height:260px;overflow:auto} blockquote{margin:4px 0;padding:4px 10px;border-left:3px solid #999;background:#fafaf7}
.checks li.fail{color:#a11} .checks li.pass{color:#276b2f} .checks li.pending,.checks li.review{color:#8a5a00}
form.inline{display:inline-block;margin:6px 8px 0 0} button{font:inherit;padding:6px 14px;border-radius:6px;border:1px solid #888;background:#fff;cursor:pointer}
button.go{background:#1d6b2c;color:#fff;border-color:#1d6b2c} button.no{background:#fff;color:#a11;border-color:#a11} button[disabled]{opacity:.45;cursor:not-allowed}
textarea{width:100%;font:12px/1.45 ui-monospace,Menlo,monospace} input[type=text]{font:inherit;padding:5px 8px;width:340px;max-width:100%}
details{margin-top:8px} .note{background:#fff8dc;border:1px solid #e6d58a;padding:8px 12px;border-radius:6px;margin:0 0 16px} .alert{background:#fde3e0;border-color:#e2a59f}
"""


def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def show(v) -> str:
    if v is None:
        return "<em>none</em>"
    if isinstance(v, (dict, list)):
        return f"<pre>{esc(json.dumps(v, indent=1, ensure_ascii=False))}</pre>"
    if isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v) >= 1e6:
        return f"{v:,.0f}"
    return esc(v)


def render_item(item: dict, data: dict, token: str) -> str:
    ev_known = {e["id"]: e for e in data["evidence"]}
    state = item.get("state")
    cls = "ready" if state == "ready" else ("fail" if "failed" in (state or "") else "wait")
    h = [f'<section class="item" id="{esc(item["id"])}"><h2>{esc(item.get("summary"))}</h2>',
         f'<div class="meta"><span class="tag {cls}">{esc(state)}</span><span class="tag">{esc(item.get("change_type"))}</span>'
         f'<span class="tag {"human" if item.get("needs_human", True) else "ready"}">{"needs a person" if item.get("needs_human", True) else "auto rule"}</span>'
         f'{esc(item["id"])} · created {esc(item.get("created"))} · {esc(item.get("approval_reason"))}</div>']
    src = item.get("source") or {}
    if src.get("url"):
        h.append(f'<div class="meta">Source: <a href="{esc(src["url"])}" target="_blank" rel="noopener">{esc(src.get("title") or src["url"])}</a>'
                 f' {esc(src.get("form") or "")} {esc(src.get("date") or "")}</div>')
    m = item.get("match") or {}
    if m:
        h.append(f'<div class="meta">Match: {esc(m.get("kind"))}. Relationships: {esc(", ".join(m.get("relationships") or []) or "none")}. '
                 f'Links between other parties: {esc(", ".join(m.get("complex_links") or []) or "none")}.</div>')
    if item.get("diff"):
        h.append("<table><tr><th style='width:34%'>Field</th><th>Now in the register</th><th>Proposed</th></tr>")
        for ch in item["diff"]:
            now = get_path(data, ch["path"])
            drift = "" if now == ch.get("old") else "<br><strong>The register has changed since this was drafted.</strong>"
            h.append(f'<tr><td><code>{esc(ch["path"])}</code></td><td class="old">{show(ch.get("old"))}{drift}</td><td class="new">{show(ch.get("new"))}</td></tr>')
        h.append("</table>")
    else:
        h.append("<p><em>No proposed change yet.</em></p>")
    evs = list(item.get("evidence") or [])
    cited = {i for ch in item.get("diff", []) for i in triage.checks._ev_ids({"x": ch.get("new")}) if isinstance(ch.get("new"), (dict, list))}
    evs += [ev_known[i] for i in sorted(cited) if i in ev_known and i not in {e.get("id") for e in evs}]
    if evs:
        h.append("<h3>Evidence</h3>")
        for e in evs:
            h.append(f'<div><a href="{esc(e.get("source_link") or e.get("url"))}" target="_blank" rel="noopener">{esc(e.get("publisher"))}: {esc(e.get("title"))}</a> '
                     f'<span class="meta">{esc(e.get("id"))} · tier {esc(e.get("tier"))} · {esc(e.get("published"))}{" · pasted by reviewer" if e.get("pasted_by_reviewer") else ""}</span>'
                     f'<blockquote>{esc(e.get("quote"))}</blockquote></div>')
    for hit in (item.get("hits") or [])[:3]:
        if hit.get("snippet"):
            h.append(f'<details><summary>Passage found by {esc(hit.get("watcher"))}</summary><blockquote>{esc(hit["snippet"][:1500])}</blockquote></details>')
    h.append('<h3>Checks</h3><ul class="checks">')
    for c in item.get("checks") or []:
        h.append(f'<li class="{esc(c["result"])}"><strong>{esc(c["check"])}</strong>: {esc(c["result"])}{" · " + esc(c["detail"]) if c.get("detail") else ""}</li>')
    h.append("</ul>")
    if item.get("counterparty_silence"):
        h.append(f"<p><strong>Other party's filings:</strong> {esc(item['counterparty_silence'])}</p>")
    h.append(f"<h3>Critic notes</h3><p>{esc(item.get('critic_notes')) if item.get('critic_notes') else '<em>None recorded.</em>'}</p>")
    tok = f'<input type="hidden" name="token" value="{esc(token)}"><input type="hidden" name="id" value="{esc(item["id"])}">'
    can = state in APPROVABLE and not any(c["result"] == "fail" for c in item.get("checks") or [])
    h.append(f'<form class="inline" method="post" action="/approve">{tok}<button class="go" {"" if can else "disabled"}>Approve</button></form>')
    h.append(f'<form class="inline" method="post" action="/hold">{tok}<input type="hidden" name="release" value="{"1" if state == "hold" else ""}">'
             f'<button>{"Release hold" if state == "hold" else "Hold"}</button></form>')
    h.append(f'<form class="inline" method="post" action="/reject">{tok}<input type="text" name="reason" placeholder="Reason for rejecting" required> <button class="no">Reject</button></form>')
    h.append(f'<details><summary>Edit then approve</summary><form method="post" action="/edit">{tok}'
             f'<p class="meta">Edit the proposed change. It is checked again; it is approved only if every check passes.</p>'
             f'<textarea name="diff" rows="12">{esc(json.dumps(item.get("diff") or [], indent=1, ensure_ascii=False))}</textarea>'
             f'<p><button class="go">Check and approve</button></p></form></details>')
    if state == "needs quote" or (src.get("watcher") == "news" and not item.get("diff")):
        h.append(f'<details open><summary>Paste the sentence from the article</summary><form method="post" action="/quote">{tok}'
                 f'<textarea name="sentence" rows="3" placeholder="The sentence, copied exactly from the article" required></textarea>'
                 f'<p><input type="text" name="quote" placeholder="The passage with the figure, under fifteen words"> <button>Cache the quote</button></p></form></details>')
    h.append("</section>")
    return "".join(h)


def page(paths: Paths, token: str, reviewer: str, view: str = "queue", flash: str = "") -> str:
    data = load_collections(paths.register)
    items = queue_items(paths)
    batch = batch_items(paths)
    from .watchers.run import alerts
    waiting = [f for f in paths.approved.glob("*.json")] if paths.approved.exists() else []
    h = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Review queue</title><style>{CSS}</style></head><body>",
         f"<header><strong>Review queue</strong><a href='/'>All items ({len(items)})</a><a href='/batch'>Batch confirm ({len(batch)})</a>"
         f"<span>Reviewer: {esc(reviewer)}</span><span>{len(waiting)} approved, waiting for publish</span></header><main>"]
    for a in alerts(paths):
        h.append(f'<div class="note alert">Watcher alert: {esc(a)}</div>')
    if flash:
        h.append(f'<div class="note">{esc(flash)}</div>')
    if waiting:
        h.append(f'<div class="note">{len(waiting)} approved item(s) are committed locally. Run <code>git push</code> to start the publish workflow, '
                 f'or <code>make apply</code> to publish from this machine.</div>')
    if view == "batch":
        h.append("<h1>Batch confirm</h1><p>Amounts past their re-verification limit where every quote still grounds and nothing newer has arrived. "
                 "Confirming sets the last verified date on each amount listed.</p>")
        if not batch:
            h.append("<p><em>Nothing to confirm.</em></p>")
        else:
            h.append(f'<form method="post" action="/batch"><input type="hidden" name="token" value="{esc(token)}"><table><tr><th style="width:5%"></th><th>Record</th><th>Amounts</th><th>Last verified</th><th>Checks</th></tr>')
            for i in batch:
                fields = ", ".join(p.split("/amounts/")[-1].replace("/last_verified", "") if "/amounts/" in p else p.rsplit("/", 2)[-2] for p in i.get("reverified_fields", []))
                olds = ", ".join(sorted({str(d.get("old")) for d in i["diff"]}))
                chk = "; ".join(f"{c['check']}: {c['result']}" for c in i.get("checks", []))
                h.append(f'<tr><td><input type="checkbox" name="ids" value="{esc(i["id"])}" checked></td><td>{esc(i["source"]["key"].replace("q_stale_", ""))}</td>'
                         f'<td>{esc(fields)}</td><td>{esc(olds)}</td><td>{esc(chk)}</td></tr>')
            h.append(f'</table><p><button class="go">Confirm the ticked items</button></p></form>')
    else:
        order = {"ready": 0, "failed grounding": 1, "failed checks": 1, "needs quote": 2, "needs extraction": 3, "hold": 4}
        shown = sorted([i for i in items if not (i.get("batch_confirm") and i.get("state") == "ready")], key=lambda i: (order.get(i.get("state"), 9), i["id"]))
        if not shown:
            h.append("<p><em>The queue is empty.</em></p>")
        h += [render_item(i, data, token) for i in shown]
    h.append("</main></body></html>")
    return "".join(h)


def make_handler(paths: Paths, reviewer: str, git: bool, token: str):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet
            pass

        def _send(self, body: str, code: int = 200):
            raw = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            u = urlparse(self.path)
            flash = (parse_qs(u.query).get("m") or [""])[0]
            if u.path in ("/", "/batch"):
                self._send(page(paths, token, reviewer, "batch" if u.path == "/batch" else "queue", flash))
            else:
                self._send("Not found", 404)

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            form = parse_qs(self.rfile.read(n).decode("utf-8"), keep_blank_values=True)
            g = lambda k: (form.get(k) or [""])[0]
            if not secrets.compare_digest(g("token"), token):
                return self._send("Session token missing or wrong. Reload the page.", 403)
            path, back = urlparse(self.path).path, "/"
            try:
                if path == "/approve":
                    msg = f"Approved {approve(g('id'), paths, by=reviewer, git=git)['id']}."
                elif path == "/edit":
                    diff = json.loads(g("diff"))
                    if not isinstance(diff, list) or not all(isinstance(c, dict) and "path" in c and "new" in c for c in diff):
                        raise ValueError("the change must be a list of {path, old, new}")
                    msg = f"Edited and approved {approve(g('id'), paths, by=reviewer, edited_diff=diff, git=git)['id']}."
                elif path == "/reject":
                    msg = f"Rejected {reject(g('id'), g('reason'), paths, by=reviewer, git=git)['id']}."
                elif path == "/hold":
                    msg = f"{'Released' if g('release') else 'Held'} {hold(g('id'), paths, release=bool(g('release')))['id']}."
                elif path == "/quote":
                    msg = f"Quote cached for {paste_quote(g('id'), g('sentence'), g('quote'), paths)['id']}."
                elif path == "/batch":
                    done = batch_confirm(paths, by=reviewer, ids=form.get("ids") or [], git=git)
                    msg, back = f"Confirmed {len(done)} item(s).", "/batch"
                else:
                    return self._send("Not found", 404)
            except (ValueError, json.JSONDecodeError, FileNotFoundError) as err:
                msg = f"Not done: {err}"
            from urllib.parse import quote
            self.send_response(303)
            self.send_header("Location", f"{back}?m={quote(msg)}")
            self.end_headers()
    return Handler


def default_reviewer() -> str:
    if os.environ.get("REVIEWER"):
        return os.environ["REVIEWER"]
    try:
        name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        name = ""
    return name or "Thomas"


def serve(paths: Paths, port: int, reviewer: str, git: bool, browser: bool) -> None:
    token = secrets.token_urlsafe(24)
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(paths, reviewer, git, token))
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"Review page: {url}  (reviewer: {reviewer}; Ctrl+C to stop)")
    if browser:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        srv.server_close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--reviewer")
    ap.add_argument("--no-git", action="store_true", help="do not commit approvals")
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--auto", action="store_true", help="approve by rule and exit")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    paths = Paths()
    if args.auto:
        done = auto_approve(paths, git=False)
        print(f"{len(done)} item(s) approved by rule" + (": " + ", ".join(done) if done else ""))
        return 0
    if args.list:
        for i in queue_items(paths):
            print(f"{i['id']}\t{i['state']}\t{'person' if i.get('needs_human', True) else 'auto'}\t{i['summary'][:120]}")
        return 0
    serve(paths, args.port, args.reviewer or default_reviewer(), not args.no_git, not args.no_browser)
    return 0


if __name__ == "__main__":
    sys.exit(main())
