#!/usr/bin/env python3
"""Mirror the public karemairodnare JSON API into this repository."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://260816-karemairodnare.vercel.app"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "api" / "v1"
USER_AGENT = "karemairodnare-archive/1.0 (+github.com/momoyuki/karemairodnare-archive)"
CORE = ["records.json", "meta.json", "index.json", "provinces.json", "districts.json", "agencies.json", "openapi.json"]


def get(path: str, retries: int = 3):
    url = f"{BASE}/api/v1/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt + 1 == retries:
                raise
            time.sleep(2 ** attempt)


def save(path: str, data) -> dict:
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    target.write_bytes(raw)
    return {"path": f"api/v1/{path}", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def discover_paths(data):
    """Discover API JSON paths advertised by index/category payloads."""
    found = set()
    for value in strings(data):
        if "/api/v1/" in value and ".json" in value:
            path = value.split("/api/v1/", 1)[1].split("?", 1)[0].split("#", 1)[0]
            if path.endswith(".json"):
                found.add(path.lstrip("/"))
    return found


def category_paths(category: str, payload):
    """Derive detail paths from common slug/code/id fields when available."""
    result = set()
    rows = payload if isinstance(payload, list) else []
    if isinstance(payload, dict):
        for key in (category, "data", "items", "results"):
            if isinstance(payload.get(key), list):
                rows = payload[key]
                break
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key in ("slug", "code", "id"):
            value = row.get(key)
            if isinstance(value, (str, int)) and str(value).strip():
                result.add(f"{category}/{urllib.parse.quote(str(value).strip(), safe='')}.json")
                break
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = []
    payloads = {}
    pending = set(CORE)

    # Fetch core/category indexes first.
    for path in CORE:
        try:
            data = get(path)
        except Exception as exc:
            print(f"WARN {path}: {exc}")
            continue
        payloads[path] = data
        files.append(save(path, data))
        pending.update(discover_paths(data))

    for category in ("provinces", "districts", "agencies"):
        data = payloads.get(f"{category}.json")
        if data is not None:
            pending.update(category_paths(category, data))

    # Mirror all discovered detail endpoints. Missing derived paths are tolerated;
    # advertised paths failing to download remain visible in the workflow log.
    already = {x["path"].removeprefix("api/v1/") for x in files}
    for path in sorted(pending - already):
        try:
            data = get(path)
            files.append(save(path, data))
        except Exception as exc:
            print(f"WARN {path}: {exc}")

    files.sort(key=lambda x: x["path"])
    manifest = {
        "source": BASE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "files": files,
    }
    (ROOT / "backup-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Backed up {len(files)} JSON files")


if __name__ == "__main__":
    main()
