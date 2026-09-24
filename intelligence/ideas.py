"""Idea bank loader, filters and scoring.

The bank is ideas/v1/<folder>.json (see ideas/README.md). Scoring is arithmetic on the
record's own fields plus optional brand weights; the model never scores in prose.
"""
from __future__ import annotations
import glob, json, os, re
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(ROOT, "ideas", "v1")

BASIS = {"measured": 3, "source_claim": 2, "general_practice": 1}
CONF = {"high": 3, "medium": 2, "low": 1}
EFFORT = {"S": 3, "M": 2, "L": 1}
COST = {"none": 3, "low": 2, "medium": 1, "high": 0}
RISK = {"low": 2, "medium": 1, "high": 0}

DEFAULT_WEIGHTS = {"evidence": 1.0, "ease": 1.0, "safety": 0.7, "bottleneck_primary": 2.0}


def load(bank: str = BANK) -> list[dict]:
    ideas = []
    for p in sorted(glob.glob(os.path.join(bank, "*.json"))):
        if os.path.basename(p).startswith("_"):
            continue
        ideas.extend(json.load(open(p, encoding="utf-8")))
    return ideas


def applies(idea: dict, store_tags: set[str]) -> bool:
    tags = set(idea.get("applies_when", []))
    return "any" in tags or bool(tags & store_tags)


def filter_ideas(ideas, bottlenecks: set[str] | None = None, store_tags: set[str] | None = None,
                 domains: set[str] | None = None, query: str | None = None, exclude_ids: set[str] | None = None):
    out = []
    q = [w for w in re.findall(r"[a-z0-9]+", (query or "").lower()) if len(w) > 2]
    for it in ideas:
        if exclude_ids and it["id"] in exclude_ids:
            continue
        if bottlenecks and not (set(it["bottleneck"]) & bottlenecks):
            continue
        if store_tags and not applies(it, store_tags):
            continue
        if domains and it["domain"] not in domains:
            continue
        if q:
            hay = " ".join([it["title"], it["lever"], it["hypothesis"], it["signal"]["check"], " ".join(it.get("steps", []))]).lower()
            if not all(w in hay for w in q):
                continue
        out.append(it)
    return out


def score(idea: dict, bottlenecks: set[str] | None = None, weights: dict | None = None) -> float:
    w = dict(DEFAULT_WEIGHTS, **(weights or {}))
    ev = BASIS[idea["expected_effect"]["basis"]] + CONF[idea["confidence"]]
    ease = EFFORT[idea["effort"]["size"]] + COST[idea["cost"]]
    safe = RISK[idea["risk"]["level"]] + (1 if idea["risk"]["reversible"] else 0)
    fit = 0.0
    if bottlenecks:
        prim = idea["bottleneck"][0]
        fit = w["bottleneck_primary"] if prim in bottlenecks else (1.0 if set(idea["bottleneck"]) & bottlenecks else 0.0)
    return round(w["evidence"] * ev + w["ease"] * ease + w["safety"] * safe + fit, 2)


def rank(ideas, bottlenecks=None, weights=None):
    return sorted(ideas, key=lambda it: (-score(it, bottlenecks, weights), it["id"]))


def summary(ideas) -> dict:
    from collections import Counter
    return {
        "ideas": len(ideas),
        "domains": len({it["domain"] for it in ideas}),
        "by_primary_bottleneck": dict(Counter(it["bottleneck"][0] for it in ideas)),
        "general_practice": sum(1 for it in ideas if it["general_practice"]),
        "basis": dict(Counter(it["expected_effect"]["basis"] for it in ideas)),
    }
