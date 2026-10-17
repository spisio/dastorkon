"""Generate a photo for every recipe that doesn't have one yet.

For each _recipes/<slug>.md without assets/photos/<slug>.jpg, combine
tools/photo_style.txt with the recipe's `photo_prompt` (falling back to its
title and blurb), ask the Gemini API for a 4:3 image, and save it as JPEG.
Reads the API key from GEMINI_API_KEY. Standard library only.

Usage: python3 tools/recipe_photos.py [--model gemini-3.1-flash-image] [slug ...]
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def front_matter_value(text, key):
    m = re.search(r'^' + key + r':\s*"?(.*?)"?\s*$', text, re.M)
    return m.group(1) if m else ""


def compress(path, max_width=1200, quality=82):
    """Shrink the photo for the web (about 200 KB). Needs Pillow; skipped without it."""
    try:
        from PIL import Image
    except ImportError:
        print("  Pillow not installed, keeping the original size")
        return
    with Image.open(path) as im:
        im = im.convert("RGB")
        if im.width > max_width:
            im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def generate(prompt, model, key):
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                             "imageConfig": {"aspectRatio": "4:3"}},
    }).encode()
    req = urllib.request.Request(API.format(model=model), data=body, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    # Gemini intermittently answers 403/429/5xx to identical requests, so retry with backoff.
    for attempt in range(1, 7):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if attempt == 6 or e.code not in (403, 429, 500, 503):
                raise
            print(f"  HTTP {e.code}, retrying ({attempt})...")
            time.sleep(5 * attempt)
    for part in resp["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            return part["inlineData"]["mimeType"], base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("no image returned: " + resp["candidates"][0].get("finishReason", "?"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3.1-flash-image")
    ap.add_argument("slugs", nargs="*")
    args = ap.parse_args()

    out_dir = ROOT / "assets" / "photos"
    todo = [md for md in sorted((ROOT / "_recipes").glob("*.md"))
            if (not args.slugs or md.stem in args.slugs) and not (out_dir / f"{md.stem}.jpg").exists()]
    if not todo:
        print("Every recipe already has a photo.")
        return
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set (add it under Settings > Secrets and variables > Actions)")

    style = (ROOT / "tools" / "photo_style.txt").read_text(encoding="utf-8").strip()
    out_dir.mkdir(parents=True, exist_ok=True)
    made = 0
    for md in todo:
        slug = md.stem
        out = out_dir / f"{slug}.jpg"
        text = md.read_text(encoding="utf-8")
        shot = front_matter_value(text, "photo_prompt") or \
            f"A plate of {front_matter_value(text, 'title')}: {front_matter_value(text, 'blurb')}"
        print(f"Generating {out.name}")
        mime, data = generate(f"{style}\n\n{shot}", args.model, key)
        out.write_bytes(data)
        compress(out)  # also turns a PNG answer into a real JPEG
        if mime != "image/jpeg":
            print(f"  note: model returned {mime}")
        made += 1
    print(f"Done: {made} new photo(s).")


if __name__ == "__main__":
    main()
