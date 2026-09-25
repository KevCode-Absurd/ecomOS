"""Check the 12 ad sets in ad_sets.json against the length rules.

Run: python3 reviews/copy-test/arm-a/raw/check_ads.py
Rules: first line under 125 characters, body under 300 words, headline under 40 characters,
description under 30 characters, at most 4 emojis in the body and 1 in the headline.
[confirm before launch] markers are not counted as copy.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ads = json.load(open(os.path.join(HERE, "ad_sets.json"), encoding="utf-8"))["ads"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✨\U0001F900-\U0001F9FF]")


def clean(t):
    return re.sub(r"\s*\[confirm before launch[^\]]*\]", "", t)


ok = True
for a in ads:
    body = clean(a["primary_text"])
    first = body.split("\n")[0]
    words = len(body.split())
    h, d = a["headline"], a["description"]
    checks = {
        "first_line_chars<125": (len(first), len(first) < 125),
        "body_words<300": (words, words < 300),
        "headline_chars<40": (len(h), len(h) < 40),
        "description_chars<30": (len(d), len(d) < 30),
        "body_emojis<=4": (len(EMOJI.findall(body)), len(EMOJI.findall(body)) <= 4),
        "headline_emojis<=1": (len(EMOJI.findall(h)), len(EMOJI.findall(h)) <= 1),
        "no_em_dash": ("—" in body + h + d, "—" not in body + h + d),
    }
    bad = [k for k, (v, p) in checks.items() if not p]
    ok &= not bad
    print(a["id"], {k: v for k, (v, p) in checks.items()}, "FAIL " + ", ".join(bad) if bad else "ok")
print("ALL OK" if ok else "SOME FAILED")
