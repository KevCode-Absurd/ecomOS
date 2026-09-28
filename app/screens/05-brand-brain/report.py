"""The weekly brain report and the founder round digest, in plain words, built from the other modules.

`weekly(brain, days, parts)`: what changed this week (by kind), decisions taken, questions answered and the top open
ones, conflicts settled, site changes, files in, the brain screen's top actions, and one brain health line. Numbers are
the modules' numbers; nothing is recomputed here. Text first, JSON beside it, so it prints and pastes.

`digest(brain, parts)`: the founder round (contract section 7.3): the top 5 questions with pull-first hints, the
proposed updates waiting in the review queue, one health line, the top 3 brain actions. Delivery to Slack or email
reads unavailable until a connector exists; copy it.
"""
from __future__ import annotations


def _line(items, none="none"):
    return ", ".join(items) if items else none


def weekly(brain, days: int, changes: dict, decisions: dict, questions: dict, conflicts: dict, site: dict, docs: dict, health: dict, rank_actions: list, market: dict) -> dict:
    week = changes.get("week") or []
    by_kind = changes.get("counts", {}).get("by_kind", {})
    dec = [d for d in decisions.get("items", []) if d.get("kind") == "action" and (d.get("date") or "") >= (brain.today.fromordinal(brain.today.toordinal() - days)).isoformat()]
    approved = [d for d in dec if d.get("choice") in ("agent", "person")]
    snoozed = [d for d in dec if d.get("choice") == "not_now"]
    q_open = [q for q in questions.get("questions", []) if not q.get("answered_on")]
    q_done = [c for c in week if c.get("kind") == "answer"]   # bank answers leave the list once answered; the changes log keeps them
    settled = [c for c in conflicts.get("settled", []) if (c.get("resolved_at") or "") >= (brain.today.fromordinal(brain.today.toordinal() - days)).isoformat()]
    site_open = [c for c in (site.get("changes") or []) if not c.get("reviewed")]
    new_docs = [d for d in docs.get("documents", []) if (d.get("added_at") or "") >= (brain.today.fromordinal(brain.today.toordinal() - days)).isoformat()]
    weak = [s for s in health.get("sections", []) if s.get("verdict", {}).get("kind") != "ok"]
    top = [a for a in rank_actions if a.get("status") != "unavailable"][:5]
    lines = [f"Brand brain, week to {brain.today.isoformat()}: {brain.brand}", ""]
    lines.append(f"What changed: {len(week)} changes this week" + (" (" + ", ".join(f"{n} {k.replace('_', ' ')}" for k, n in sorted(by_kind.items(), key=lambda kv: -kv[1])) + ")" if by_kind else "") + ".")
    lines.append(f"Decisions: {len(approved)} approved, {len(snoozed)} snoozed.")
    lines.append(f"Questions: {len(q_done)} answered this week, {len(q_open)} open. Top open: " + _line([q["question"][:70] for q in q_open[:3]]) + ".")
    lines.append(f"Conflicts settled: {len(settled)}. Open: {conflicts.get('counts', {}).get('open', 0)}.")
    if site.get("pair"):
        lines.append(f"Site: {site['counts']['changes']} changes between {site['old']} and {site['new']}, {len(site_open)} not reviewed.")
    else:
        lines.append("Site: " + (site.get("unavailable_reason") or "no diff yet").rstrip(".") + ".")
    lines.append(f"Files in: {len(new_docs)} this week, {docs.get('proposed_total', 0)} records waiting in the review queue.")
    lines.append(f"Competitors: snapshot {market.get('snapshot_age_days', 'unavailable')} days old, {len(market.get('gaps') or [])} format or hook gaps.")
    strong = health.get("strong_share")
    lines.append(f"Health: {health.get('records', 0)} records, " + (f"{round(strong * 100)} percent approved or backed, " if strong is not None else "") + f"{len(weak)} sections need an action" + (": " + _line([s['label'] + ' (' + s['verdict']['text'].lower() + ')' for s in weak[:4]]) if weak else "") + ".")
    lines.append("")
    lines.append("Top moves from the brain screen:")
    for i, a in enumerate(top, 1):
        lines.append(f"{i}. {a['title']} ({a['owner'].replace('_', ' ')}, {a['rubric']['total']}/100)")
    if not top:
        lines.append("none open")
    return {"days": days, "text": "\n".join(lines), "counts": {"changes": len(week), "approved": len(approved), "snoozed": len(snoozed), "questions_answered": len(q_done), "questions_open": len(q_open),
                                                            "conflicts_settled": len(settled), "site_open": len(site_open), "documents": len(new_docs), "weak_sections": len(weak), "top": len(top)},
            "top": [{"id": a["id"], "title": a["title"], "owner": a["owner"], "total": a["rubric"]["total"]} for a in top], "weak": [{"section": s["section"], "verdict": s["verdict"]["text"]} for s in weak[:6]],
            "note": "Built from the same numbers the blocks above show. Copy it or print it; it reads without the screen."}


def digest(brain, questions: dict, review: list, health: dict, rank_actions: list, connectors: dict) -> dict:
    top_q = [q for q in questions.get("questions", []) if not q.get("answered_on")][:5]
    weak = [s for s in health.get("sections", []) if s.get("verdict", {}).get("kind") != "ok"]
    top = [a for a in rank_actions if a.get("status") != "unavailable"][:3]
    lines = [f"Founder round, {brain.today.isoformat()}: 5 questions, {len(review)} proposed updates, 1 health line", ""]
    for i, q in enumerate(top_q, 1):
        lines.append(f"{i}. {q['question']}")
        lines.append(f"   {q['hint']} Unblocks: {', '.join(x.replace('_', ' ') for x in q.get('rooms', [])[:4])}.")
    if not top_q:
        lines.append("No question waits on you.")
    lines.append("")
    lines.append(f"Proposed updates waiting in the review queue: {len(review)}" + (" (" + _line(sorted({r.get('section', '') for r in review})[:5]) + ")" if review else "") + ".")
    strong = health.get("strong_share")
    lines.append("Brain health: " + (f"{round(strong * 100)} percent approved or backed, " if strong is not None else "") + f"{len(weak)} sections need an action, {connectors.get('counts', {}).get('connected', 0)} sources connected.")
    lines.append("")
    lines.append("Approve today: " + _line([f"{a['title']} ({a['owner'].replace('_', ' ')})" for a in top]) + ".")
    lines.append("")
    lines.append("Reply with a line per question, or drop a file in Files in. Nothing here needs more than a minute.")
    return {"text": "\n".join(lines), "questions": len(top_q), "proposed": len(review), "delivery": {"app": "this screen", "slack": None, "email": None,
            "reason": "no Slack or email connector yet; copy the digest"}, "note": "The weekly ask, pull first: a connected source removes its question before it is asked."}
