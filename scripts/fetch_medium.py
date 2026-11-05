"""Refresh assets/medium.json from the Medium RSS feed. Run by .github/workflows/medium.yml."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import medium  # noqa: E402

items, source, errors = medium._fetch()
for e in errors:
    print("warn:", e)
if not items:
    print("No articles fetched; leaving the existing snapshot untouched.")
    sys.exit(0)

path = medium.SNAPSHOT
old = None
if os.path.exists(path):
    with open(path, encoding="utf-8") as f:
        old = json.load(f).get("items")
if old == items:
    print("No change in articles.")
    sys.exit(0)
with open(path, "w", encoding="utf-8") as f:
    json.dump({"fetched_at": time.strftime("%Y-%m-%d", time.gmtime()), "source": source, "items": items},
              f, ensure_ascii=False, indent=2)
print(f"Wrote {len(items)} articles from {source}:", *[f"  - {i['title']}" for i in items], sep="\n")
