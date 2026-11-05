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

import requests

FEED_URLS = [
    "https://medium.com/feed/@abhineetsharma77",
    "https://abhineetsharma77.medium.com/feed",
]
PROFILE = "https://abhineetsharma77.medium.com/"
TTL = 6 * 3600          # refresh every 6 hours
RETRY = 10 * 60         # after a failure, try again in 10 minutes
LIMIT = 3
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

_cache = {"items": None, "at": 0.0, "next": 0.0}
_lock = threading.Lock()


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
    for url in FEED_URLS:
        try:
            r = requests.get(url, timeout=6, headers={"User-Agent": "portfolio-feed/1.0"})
            if r.ok and "<rss" in r.text[:500]:
                items = parse(r.text)
                if items:
                    return items
        except (requests.RequestException, ET.ParseError):
            continue
    return None


def _refresh():
    items = _fetch()
    with _lock:
        now = time.time()
        if items:
            _cache.update(items=items, at=now, next=now + TTL)
        else:
            _cache["next"] = now + RETRY


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
