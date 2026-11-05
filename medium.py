"""Latest Medium articles, fetched from the public RSS feed.

The feed is fetched in a background thread and cached for a few hours, so a
page request never waits on Medium. If the feed is unreachable, the section
falls back to a single "Read on Medium" card.
"""
import re
import threading
import time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import escape, unescape

import json
import logging
import os

import requests

log = logging.getLogger("medium")

FEED_URLS = [
    "https://medium.com/feed/@abhineetsharma77",
    "https://abhineetsharma77.medium.com/feed",
]
PROFILE = "https://abhineetsharma77.medium.com/"
# Medium sits behind Cloudflare, which often blocks datacenter IPs (Railway). rss2json relays the same feed.
RSS2JSON = "https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fmedium.com%2Ffeed%2F%40abhineetsharma77"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.5",
    "Accept-Language": "en-US,en;q=0.9",
}
TTL = 6 * 3600          # refresh every 6 hours
RETRY = 10 * 60         # after a failure, try again in 10 minutes
LIMIT = 3
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

_cache = {"items": None, "at": 0.0, "next": 0.0, "source": None, "errors": []}
_lock = threading.Lock()

# Snapshot written daily by .github/workflows/medium.yml (GitHub's runners can reach Medium even when
# Railway is blocked). Loaded at startup so the section is never empty; a live refresh may update it.
SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "medium.json")
try:
    with open(SNAPSHOT, encoding="utf-8") as _f:
        _snap = json.load(_f)
    if _snap.get("items"):
        _cache.update(items=_snap["items"][:LIMIT], source=f"snapshot {_snap.get('fetched_at', '')}".strip())
except (OSError, ValueError):
    pass


def _item(title, link, date, body, tags, thumb=None):
    img = re.search(r'<img[^>]+src="([^"]+)"', body)
    src = thumb or (img.group(1) if img else None)
    if src and "stat?event" in src:
        src = None
    text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", body))).strip()
    excerpt = text[:190].rsplit(" ", 1)[0] + "…" if len(text) > 190 else text
    return {"title": (title or "").strip(), "link": (link or PROFILE).split("?")[0], "date": date, "img": src,
            "excerpt": excerpt, "mins": max(1, round(len(text.split()) / 230)), "tags": [t for t in tags if t][:3]}


def parse_rss2json(text):
    data = json.loads(text)
    if data.get("status") != "ok":
        raise ValueError(data.get("message", "rss2json error"))
    out = []
    for it in data.get("items", []):
        try:
            date = time.strftime("%b %Y", time.strptime(it.get("pubDate", "")[:10], "%Y-%m-%d"))
        except ValueError:
            date = ""
        out.append(_item(it.get("title"), it.get("link"), date, it.get("content") or it.get("description") or "",
                         it.get("categories") or [], it.get("thumbnail") or None))
    return [i for i in out if i["title"]][:LIMIT]


def parse(xml_text):
    root = ET.fromstring(xml_text)
    items = []
    for it in root.iter("item"):
        body = it.findtext("content:encoded", default="", namespaces=NS) or it.findtext("description", default="")
        img = re.search(r'<img[^>]+src="([^"]+)"', body)
        text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", body))).strip()
        words = len(text.split())
        # skip Medium's "continue reading" stubs in the excerpt
        excerpt = text[:190].rsplit(" ", 1)[0] + "…" if len(text) > 190 else text
        try:
            date = parsedate_to_datetime(it.findtext("pubDate", "")).strftime("%b %Y")
        except (TypeError, ValueError):
            date = ""
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or PROFILE).split("?")[0],
            "date": date,
            "img": img.group(1) if img and "stat?event" not in img.group(1) else None,
            "excerpt": excerpt,
            "mins": max(1, round(words / 230)),
            "tags": [c.text for c in it.findall("category") if c.text][:3],
        })
    return [i for i in items if i["title"]][:LIMIT]


def _fetch():
    errors = []
    for url in FEED_URLS:
        try:
            r = requests.get(url, timeout=8, headers=HEADERS)
            if r.ok and "<rss" in r.text[:500]:
                items = parse(r.text)
                if items:
                    return items, url, errors
                errors.append(f"{url}: feed had no items")
            else:
                errors.append(f"{url}: HTTP {r.status_code}, {r.text[:60]!r}")
        except (requests.RequestException, ET.ParseError) as e:
            errors.append(f"{url}: {type(e).__name__}: {e}"[:200])
    try:
        r = requests.get(RSS2JSON, timeout=10, headers={"User-Agent": HEADERS["User-Agent"]})
        items = parse_rss2json(r.text)
        if items:
            return items, "rss2json", errors
        errors.append("rss2json: no items")
    except (requests.RequestException, ValueError) as e:
        errors.append(f"rss2json: {type(e).__name__}: {e}"[:200])
    return None, None, errors


def _refresh():
    items, source, errors = _fetch()
    for e in errors:
        log.warning("medium feed: %s", e)
    with _lock:
        now = time.time()
        _cache["errors"] = errors
        if items:   # keep the snapshot when the live fetch fails
            _cache.update(items=items, at=now, next=now + TTL, source=source)
        else:
            _cache["next"] = now + RETRY


def status():
    return {"articles": [a["title"] for a in (_cache["items"] or [])], "source": _cache["source"],
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(_cache["at"])) if _cache["at"] else None,
            "next_refresh_in_s": max(0, int(_cache["next"] - time.time())), "last_errors": _cache["errors"]}


def warm():
    """Fetch once at startup so the first visitor gets articles, not the fallback."""
    threading.Thread(target=_refresh, daemon=True).start()
    with _lock:
        _cache["next"] = time.time() + RETRY


def articles():
    """Cached articles (or None). Kicks off a background refresh when stale."""
    with _lock:
        stale = time.time() >= _cache["next"]
        if stale:
            _cache["next"] = time.time() + RETRY   # one refresh at a time
    if stale:
        threading.Thread(target=_refresh, daemon=True).start()
    return _cache["items"]


def render(items):
    if not items:
        return (f'<a class="article-card article-fallback" href="{PROFILE}" target="_blank" rel="noopener">'
                f'<div class="article-body"><div class="article-meta">Medium</div>'
                f'<h3 class="article-title">Read my articles on Medium</h3>'
                f'<p class="article-excerpt">Long-form notes on GenAI, RAG and building agents that ship.</p>'
                f'<span class="article-cta">abhineetsharma77.medium.com <i class="fa-solid fa-arrow-right"></i></span>'
                f'</div></a>')
    out = []
    for a in items:
        thumb = (f'<div class="article-thumb"><img src="{escape(a["img"])}" alt="" loading="lazy" '
                 f'referrerpolicy="no-referrer"></div>') if a["img"] else '<div class="article-thumb empty"><span>書</span></div>'
        tags = "".join(f'<span class="also-chip">{escape(t)}</span>' for t in a["tags"])
        out.append(
            f'<a class="article-card" href="{escape(a["link"])}" target="_blank" rel="noopener">{thumb}'
            f'<div class="article-body"><div class="article-meta">{escape(a["date"])} · {a["mins"]} min read</div>'
            f'<h3 class="article-title">{escape(a["title"])}</h3>'
            f'<p class="article-excerpt">{escape(a["excerpt"])}</p>'
            f'<div class="article-tags">{tags}</div></div></a>'
        )
    return "".join(out)
