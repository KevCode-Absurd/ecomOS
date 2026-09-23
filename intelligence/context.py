"""Bounded, condition-preserving packets. No silent truncation of card meaning."""
import json
import re
from .conditions import evaluate, excluded


def conservative_units(text):
    """UTF-8 byte units, NOT measured provider tokens.

    Deliberately conservative for offline development. Production must inject a
    provider tokenizer/count API. Never advertise this as exact token counting.
    """
    return len(text.encode("utf-8"))


def render(cards):
    # Conditions and evidence stay intact. Full rationale can be fetched separately.
    return json.dumps({"cards": cards}, ensure_ascii=False, separators=(",", ":"))


def pack(cards, query, facts, budget=6000, count=conservative_units, max_cards=6):
    if budget < count(render([])) or max_cards < 1:
        raise ValueError("Budget must fit an empty packet; max_cards must be positive")
    by_id = {c["id"]: c for c in cards}
    reasons, chosen = {}, []

    def check(card):
        applicable = evaluate(card['applies_when'], facts)
        if applicable is None:
            return 'missing prerequisite facts'
        if not applicable:
            return 'prerequisite not met'
        exclusion = excluded(card['do_not_use_when'], facts)
        if exclusion is None:
            return 'unknown exclusion condition'
        if exclusion:
            return 'excluded by condition'
        return None

    def closure(card_id, visiting):
        if card_id in visiting:
            raise ValueError("dependency cycle")
        if card_id not in by_id:
            raise ValueError("unavailable dependency: " + card_id)
        card = by_id[card_id]
        problem = check(card)
        if problem:
            raise ValueError(problem)
        result = []
        for dep in card["dependencies"]:
            result.extend(closure(dep, visiting | {card_id}))
        result.append(card)
        return result

    terms = set(re.findall(r"\w+", query.lower()))
    def score(c):
        words = set(re.findall(r"\w+", " ".join([c["title"],c["claim"],c["action"]]).lower()))
        return len(terms & words)

    for card in sorted(cards, key=lambda c: (-score(c), c["id"])):
        if not score(card):
            continue
        try:
            additions = closure(card["id"], set())
        except ValueError as e:
            reasons[card["id"]] = str(e)
            continue
        merged = {c["id"]:c for c in chosen + additions}
        proposed = list(merged.values())
        if len(proposed) > max_cards or count(render(proposed)) > budget:
            reasons[card["id"]] = "complete card and dependencies exceed budget"
            continue
        chosen = proposed
    payload = render(chosen)
    return {"context": payload, "selected_ids": [c["id"] for c in chosen],
            "used_units": count(payload), "budget_units": budget, "omitted": reasons,
            "counter": "utf8_bytes" if count is conservative_units else "injected_token_counter",
            "retrieval": "lexical_baseline_only"}
