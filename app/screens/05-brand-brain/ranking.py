"""rank(brand, window) for the brand brain screen: audit findings to actions with real titles, steps, artefacts and drafts.

Contract: app/contracts/depth.md sections 4 and 5. The rubric scores come from app/rank.py (`score`), then the
reputation overrides written next to each rule in audit.py are applied and the total recomputed with the fixed
weights. Owners: a brief that becomes an ad is `agent_drafts` (the founder approves before anything ships);
a brain refresh the agent can run read-only is `agent`; a conflict or a claim is the founder's call, `person`.
Unavailable findings keep the default connect action. Deterministic: no model call, no clock beyond the window.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]

_r = importlib.util.spec_from_file_location("ecomos_rank_for_bb", APP / "rank.py")
rank_mod = importlib.util.module_from_spec(_r)
sys.modules["ecomos_rank_for_bb"] = rank_mod
_r.loader.exec_module(rank_mod)

REPUTATION_OVERRIDE = {"BRN-R05": 3, "BRN-R06": 3, "BRN-R08": 3, "BRN-R09": 5, "BRN-R10": 3, "BRN-R04": 5, "BRN-R13": 5, "BRN-R15": 5, "BRN-R16": 5, "BRN-R19": 5}
CHECK_DAYS = {"BRN-R05": 14, "BRN-R06": 14, "BRN-R08": 14, "BRN-R07": 7, "BRN-R09": 14, "BRN-R10": 14}
TEST_BUDGET_USD = 300


def _pct(x) -> str:
    return f"{round(x * 100)} percent" if isinstance(x, (int, float)) else "unavailable"


def _ev(f: dict, metric: str):
    return next((e.get("value") for e in f.get("evidence") or [] if e.get("metric") == metric), None)


def _check_on(f: dict, days: int) -> str | None:
    end = f.get("last_seen") or f.get("first_seen")
    try:
        return (dt.date.fromisoformat(str(end)[:10]) + dt.timedelta(days=days)).isoformat() if end else None
    except ValueError:
        return None


def build(f: dict, nr: float | None) -> dict:
    """One action from one finding, with the rule's own title, steps and artefact."""
    a = rank_mod.action_from_finding(f, nr)
    rid = f.get("rule_id")
    ent = f.get("entity") or {}
    label = ent.get("label") or ent.get("id") or ""
    if f.get("status") == "unavailable":
        return a
    if rid == "BRN-R01":
        n = _ev(f, "stale_records")
        a.update(title=f"Refresh {label.replace('_', ' ')}: " + (f"{n} records past their shelf life" if n else "older than its shelf life"), owner="agent",
                 artefact={"kind": "brain_record", "label": f"fresh {label.replace('_', ' ')} records, old ones retired to history", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": f"Re-crawl the public source that fills {label.replace('_', ' ')}, read-only, inside its caps. Estimate first if it is paid."},
                        {"n": 2, "who": "agent", "text": "Diff the new records against the current ones. Changes go to the review queue and the changes log."},
                        {"n": 3, "who": "person", "text": "Accept the changes. Stale records retire, never delete."},
                        {"n": 4, "who": "agent", "text": "Run BRN-R01 again. The finding resolves when no record is past its shelf life."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R02":
        rooms, nf = _ev(f, "rooms_blocked"), _ev(f, "empty_fields")
        a.update(title=f"Fill {label.replace('_', ' ')}: {nf or 'the'} field{'s' if nf != 1 else ''} that {rooms or 'the'} rooms wait on", owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "approved records for the empty fields", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Check the connectors first: a source that fills the section beats a question."},
                        {"n": 2, "who": "agent", "text": "Draft one question per empty field, with the pull-first hint, into the open questions block."},
                        {"n": 3, "who": "person", "text": "Answer each in a line, or connect the source."},
                        {"n": 4, "who": "agent", "text": "Write the answers as approved records. The rooms read them on their next load."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=2)
    elif rid == "BRN-R03":
        q = (f.get("sentence") or "").replace("No answer yet to: ", "")
        a.update(title="Answer: " + (q[:80] + ("..." if len(q) > 80 else "")), owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "an approved founder record for the field", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Show the question with what the brain already holds and the pull-first hint."},
                        {"n": 2, "who": "person", "text": "Answer in a line in the open questions block, with a proof link when there is one."},
                        {"n": 3, "who": "agent", "text": "Write the answer as an approved record and re-run the rules that waited on it."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R04":
        a.update(title=f"Approve or replace the claim copy leans on: {label[:60]}", owner="person",
                 artefact={"kind": "brain_record", "label": "the claim tiered approved, or the copy pointed at an approved claim", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "List the claim, its source page and every rung and page that uses it."},
                        {"n": 2, "who": "person", "text": "In the brain health heatmap, approve the claim as is, or forbid it."},
                        {"n": 3, "who": "agent", "text": "If forbidden, re-point the rung at an approved claim and flag the live copy on the copy screen."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R05":
        us, them = _ev(f, "format_share_us"), _ev(f, "format_share_competitor_median")
        a.update(title=f"Test {label.lower()}: competitors run {_pct(them)}, we run {_pct(us)}", owner="agent_drafts",
                 artefact={"kind": "test_brief", "label": f"a test brief for 3 {label.lower()}", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Read the 3 competitor pages leading on this format for layout and mood only. Never their text, logos, products or faces."},
                        {"n": 2, "who": "agent", "text": "Write a test brief: 3 ads in this format, same product and offer as the current flight, hooks from the contested angles."},
                        {"n": 3, "who": "person", "text": "Approve the brief. The creative screen makes the ads."},
                        {"n": 4, "who": "agent", "text": f"Read cost per order at 1,000 impressions or more. Stop after ${TEST_BUDGET_USD} of spend with no winner."}],
                 size={"text": "3 ads, one format", "usd": None}, stop_rule=f"no ad beats the median cost per order after ${TEST_BUDGET_USD} of spend",
                 check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=6)
    elif rid == "BRN-R06":
        a.update(title=f"Put {label.lower()} in the next brief: we run none, competitors do", owner="agent_drafts",
                 artefact={"kind": "ad_brief", "label": f"3 first lines in the {label.lower().replace(' hooks', '')} form", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Take the 3 strongest contested angles and write each as this hook form: 3 first lines."},
                        {"n": 2, "who": "person", "text": "Approve the lines. They join the next ad brief."},
                        {"n": 3, "who": "agent", "text": "Read the hook rate against the statement hooks in the same flight after 14 days."}],
                 size={"text": "3 first lines", "usd": None}, stop_rule="hook rate below the statement hooks after 14 days", check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=2)
    elif rid == "BRN-R07":
        a.update(title=f"Re-pull {label} from the Ad Library by page id", owner="agent",
                 artefact={"kind": "brain_record", "label": "a fresh competitor snapshot: formats, hooks, run lengths", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Show the estimate from the connector against the per-run and weekly caps. Pages by id only, never a search term."},
                        {"n": 2, "who": "agent", "text": "Run the pull. Records land in the review queue with the capture date."},
                        {"n": 3, "who": "person", "text": "Accept the snapshot. The coverage matrix and the gaps recompute."}],
                 check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=1)
    elif rid == "BRN-R08":
        n = _ev(f, "competitor_pages_running_angle")
        a.update(title=f"Brief the {label.lower()} angle: {n} competitor page{'s run' if n != 1 else ' runs'} it, we run 0", owner="agent_drafts",
                 artefact={"kind": "ad_brief", "label": f"a concept brief on {label.lower()}, 3 concepts", "draft": f.get("draft")},
                 steps=[{"n": 1, "who": "agent", "text": "Write 3 concepts from the drafted brief: a first line and a first frame each, proof only from approved or site-backed claims."},
                        {"n": 2, "who": "person", "text": "Approve the concepts, or send the brief back with a note."},
                        {"n": 3, "who": "agent", "text": "Hand the approved concepts to the creative screen as an ad brief."},
                        {"n": 4, "who": "agent", "text": f"Read cost per order at 1,000 impressions or more after 7 days. Stop after ${TEST_BUDGET_USD} of spend with no winner."}],
                 size={"text": "3 concepts", "usd": None}, stop_rule=f"no concept beats the median cost per order after ${TEST_BUDGET_USD} of spend",
                 win_rule="a concept beats the current median cost per order in 7 days", check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=4)
        if f.get("own_positioning"):
            a["why"] = (a.get("why") or "") + " The brain names this angle as who we are."
    elif rid == "BRN-R09":
        where = f.get("where") or []
        a.update(title=f"Answer the {label} comparison where buyers make it", owner="agent_drafts",
                 artefact={"kind": "copy", "label": "one proof line for each surface: " + ", ".join(where[:4]), "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Name the doubt behind the recommendation and the proof the brain holds for it. If the ladder rung has no proof, raise the open question first."},
                        {"n": 2, "who": "agent", "text": "Draft one proof line per surface: " + (", ".join(where[:4]) or "PDP, retargeting ad, CX macro") + ". Never quote the thread."},
                        {"n": 3, "who": "person", "text": "Approve the lines. Each ships from its own screen."},
                        {"n": 4, "who": "agent", "text": "Re-read the public threads on the next pull and count the recommendations again."}],
                 check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=3)
    elif rid == "BRN-R10":
        a.update(title=f"Add a line for {label} to the positioning frame", owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "a positioning frame with the buyers' frame in it, approved", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Draft one sentence for the frame that answers it, from the proof points in the brain."},
                        {"n": 2, "who": "person", "text": "Edit and save it in the profile. It becomes approved and flows to copy, creative and landing pages."},
                        {"n": 3, "who": "agent", "text": "Re-check the frame against the next public pull."}],
                 check_on=_check_on(f, CHECK_DAYS[rid]), time_to_ship_hours=1)
    elif rid == "BRN-R11":
        a.update(title=f"Settle {label.replace('_', ' ')}: {_pct(_ev(f, 'weak_share'))} of it is inferred", owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "approved records in place of inferred ones", "draft": None},
                 steps=f.get("steps") or a["steps"], check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R22":
        idea = f.get("idea") or {}
        steps = [{"n": i + 1, "who": "agent", "text": str(st)} for i, st in enumerate((idea.get("steps") or [])[:4])]
        draft = f"Test brief for {idea.get('idea_id')}: {idea.get('title')}\nSignal to check first: {idea.get('signal')}\nMetric: {idea.get('metric')} {idea.get('direction')}\nEffort {idea.get('effort')}, cost {idea.get('cost')}, risk {idea.get('risk')}." + (f"\nWhy you picked it: {idea.get('why')}" if idea.get("why") else "")
        a.update(title=f"Write the test brief for {idea.get('idea_id')}: {str(idea.get('title'))[:60]}", owner="agent_drafts",
                 artefact={"kind": "test_brief", "label": "a test brief with the signal check, the metric and the read date", "draft": draft},
                 steps=(steps or [{"n": 1, "who": "agent", "text": "Check the idea's signal in the brand's data."}]) + [{"n": len(steps) + 1, "who": "agent", "text": "Draft the brief with the metric, the size and the read date; add it to the experiments registry."},
                                                                                                                       {"n": len(steps) + 2, "who": "person", "text": "Approve the brief. The experiments screen runs it."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=2)
    elif rid == "BRN-R23":
        rung = f.get("rung") or {}
        cands = rung.get("candidates") or []
        surfaces = ", ".join(str(u).replace("_", " ") for u in rung.get("uses") or [])
        a.update(title=f"Brief the proof for {str(rung.get('theme') or label).replace('_', ' ')} rung {rung.get('level')}: {str(rung.get('doubt'))[:60]}", owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": f"an approved proof record attached to the rung, read by {surfaces or 'every surface'}", "draft": rung.get("brief")},
                 steps=[{"n": 1, "who": "agent", "text": ("Show the " + str(len(cands)) + " records on file that name this doubt: " + ", ".join(c["id"] for c in cands[:3]) + ".") if cands else "Confirm nothing on file names this doubt; list the fact that would (a policy term, a product fact, an offer term or a tiered claim)."},
                        {"n": 2, "who": "agent", "text": "Draft the proof line from the record, sourced to the site or a policy; never a review quote as a testimonial."},
                        {"n": 3, "who": "person", "text": "Pick the record as proof, or approve the drafted fact as an approved record."},
                        {"n": 4, "who": "agent", "text": f"Attach it to the rung. The surfaces that use the rung ({surfaces or 'copy, page, listing, macro'}) read the proof on their next brief."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R43":
        ib = f.get("inbox") or []
        a.update(title=f"Read {len(ib)} brief{'s' if len(ib) != 1 else ''} other screens handed to the brain", owner="person",
                 artefact={"kind": "brain_record", "label": "each brief accepted into the review queue or dismissed with a why", "draft": "\n".join(f"- {x['title']} from {x['from_screen']} ({x['age_days']} days)" for x in ib) or None},
                 steps=[{"n": 1, "who": "person", "text": "Open the inbox on the brain screen and read each brief."}, {"n": 2, "who": "person", "text": "Accept the ones that carry facts (the extractor proposes records) or dismiss with a why."}, {"n": 3, "who": "agent", "text": "Proposed records wait in the review queue; the ledger shows what was done."}],
                 check_on=_check_on(f, 3), time_to_ship_hours=0.25)
    elif rid == "BRN-R42":
        rows = f.get("old_approvals") or []
        a.update(title=f"Still true? Confirm or retire {len(rows)} approval{'s' if len(rows) != 1 else ''} older than 3 shelf lives", owner="person",
                 artefact={"kind": "brain_record", "label": "each old approval confirmed with an expiry, or retired", "draft": "\n".join(f"- {x['id']}: {x['text']} ({x['age_days']} days, limit {x['limit_days']})" for x in rows) or None},
                 steps=[{"n": 1, "who": "agent", "text": "List each with what it says, when you approved it and the section's shelf life."}, {"n": 2, "who": "person", "text": "Confirm the ones that still hold in a click; retire the rest."}, {"n": 3, "who": "agent", "text": "A confirmed one gets an expiry and joins the weekly check from now on."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.25)
    elif rid == "BRN-R41":
        eg = f.get("evidence_gaps") or {}
        rows = eg.get("rows") or []
        bf = eg.get("by_fix") or {}
        a.update(title=f"Back or retire {len(rows)} strong record{'s' if len(rows) != 1 else ''} with no quote behind {'them' if len(rows) != 1 else 'it'}", owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "each record with its quote attached, approved on your word, or retired", "draft": "\n".join(f"- {x['id']} ({x['tier']}): {x['fix_kind']} from {x['ref'] or 'no source'}" for x in rows) or None},
                 steps=[{"n": 1, "who": "agent", "text": f"Re-read the {bf.get('re-read', 0)} url and file sources and attach the line that backs each record; list the {bf.get('attach', 0)} actor-run records with their item text."}, {"n": 2, "who": "person", "text": f"For the {bf.get('decide', 0)} with no source, and any the agent could not back: approve by hand or retire."}, {"n": 3, "who": "agent", "text": "The list empties; packages read only backed facts."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R40":
        ms = f.get("misses") or []
        a.update(title=f"Answer {len(ms)} question{'s' if len(ms) != 1 else ''} the brain could not: " + "; ".join(m["q"][:40] for m in ms[:2]) + ("..." if len(ms) > 2 else ""), owner="person",
                 artefact={"kind": "brain_record", "label": "one record per question, approved, so the next ask finds it", "draft": "\n".join(f"- {m['q']} (asked {m['times']}x by {', '.join(m['readers'])}, last {m['last']})" for m in ms)},
                 steps=[{"n": 1, "who": "agent", "text": "Open each as a question with the ask count as the why."}, {"n": 2, "who": "person", "text": "Answer each in the profile or the questions block; a fact you do not have goes to the person who does."}, {"n": 3, "who": "agent", "text": "The next ask finds the record; the miss reads as answered."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R39":
        h = f.get("handoff") or {}
        failed = h.get("state") == "failed"
        a.update(title=(f"Walk {h.get('to')} through the {len(h.get('misses') or [])} quiz misses" if failed else f"Chase {h.get('to')} for the quiz answers, {h.get('days')} days after the hand-off"), owner="person",
                 artefact={"kind": "brain_record", "label": "the hand-off closed with a passed quiz" , "draft": ("\n".join(f"- {m.get('n')}. {m.get('question')}" for m in (h.get("misses") or [])) or None)},
                 steps=([{"n": 1, "who": "agent", "text": "List each missed question with the right answer and its record."}, {"n": 2, "who": "person", "text": "Go through the misses with them, then have them answer again with their name."}, {"n": 3, "who": "agent", "text": "The hand-off closes at 70 percent or better."}] if failed else
                        [{"n": 1, "who": "person", "text": "Ask for the 10 answers, one per line."}, {"n": 2, "who": "person", "text": "Paste them in the quiz panel with their name; the hand-off takes the score."}]),
                 check_on=_check_on(f, 3), time_to_ship_hours=0.5)
    elif rid == "BRN-R38":
        st = f.get("settle") or {}
        left = st.get("left") or []
        a.update(title=f"Settle {len(left)} record{'s' if len(left) != 1 else ''} that still contradict {str(st.get('field')).replace('_', ' ')}", owner="person",
                 artefact={"kind": "brain_record", "label": "each contradicting record fixed, retired or confirmed as a different fact", "draft": "\n".join(f"- {c['id']} ({c.get('tier')}): {c.get('says')}" for c in left)},
                 steps=[{"n": 1, "who": "agent", "text": "List each record with what it says, its tier and where it came from, next to the value you saved."}, {"n": 2, "who": "person", "text": "For each: retire it when it is out of date, edit it when it is a different fact, or mark it done."}, {"n": 3, "who": "agent", "text": "The plan closes when none is left; agents read the saved value only."}],
                 check_on=_check_on(f, 2), time_to_ship_hours=0.5)
    elif rid == "BRN-R37":
        up = f.get("update") or {}
        left = up.get("left") or []
        a.update(title=f"Update {len(left)} place{'s' if len(left) != 1 else ''} that still say {up.get('before')}: {str(up.get('field')).replace('_', ' ')} is now {up.get('after')}", owner="agent_drafts",
                 artefact={"kind": "copy", "label": "every dependent rewritten with the new value, each marked done on the plan", "draft": "\n".join(f"- {d.get('kind')}: {d.get('label')} ({d['id']})" for d in left)},
                 steps=[{"n": 1, "who": "agent", "text": "Rewrite each dependent with the new value: records in the review queue, snippets and facts regenerated, ad copy drafted."}, {"n": 2, "who": "person", "text": "Approve each rewrite; live ads and pages change only through their own screens."}, {"n": 3, "who": "agent", "text": "Mark each dependent done on the plan; the plan closes when none is left."}],
                 check_on=_check_on(f, 3), time_to_ship_hours=1)
    elif rid == "BRN-R36":
        ex = f.get("expiring") or {}
        conf = ex.get("confirmable")
        a.update(title=(f"Confirm {ex.get('records')} {str(ex.get('source')).replace('_', ' ')} records before they go stale" if conf else f"Re-pull {str(ex.get('source')).replace('_', ' ')}: {ex.get('records')} records expire by {ex.get('earliest')}"), owner="person" if conf else "agent",
                 artefact={"kind": "brain_record", "label": "the records refreshed or confirmed, expiry moved on", "draft": None},
                 steps=([{"n": 1, "who": "agent", "text": "List the records with what each says and when it expires."}, {"n": 2, "who": "person", "text": "Confirm each still-true one in a click; retire what is no longer true."}, {"n": 3, "who": "agent", "text": "The expiry moves on by the section's shelf life."}] if conf else
                        [{"n": 1, "who": "agent", "text": f"Estimate first if it is paid, then {ex.get('refresh')}."}, {"n": 2, "who": "agent", "text": "Diff the new records against the current ones; changes go to the review queue."}, {"n": 3, "who": "person", "text": "Accept the changes; the old records retire to history."}]),
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R35":
        ow = f.get("owner_row") or {}
        who = ow.get("owner") or "the founder"
        a.update(title=f"Review {ow.get('label') or label}: {ow.get('days_since')} days since the last look, cadence {ow.get('cadence_days')}" + (f" ({who})" if ow.get("owner") else ", no owner yet"), owner="person",
                 artefact={"kind": "brain_record", "label": "the section read through, stale records retired or refreshed, the review date written", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": f"Open {ow.get('label')} in the records browser with the stale and unverified records first."}, {"n": 2, "who": "person", "text": f"{who.capitalize()} reads it: approve what is true, retire what is not, answer what is missing."}, {"n": 3, "who": "agent", "text": "Mark it reviewed; the clock restarts from today."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R34":
        rl = f.get("redlines") or {}
        n = _ev(f, "red_lines_without_reason")
        a.update(title=f"Give {n} red line{'s' if n != 1 else ''} a reason so agents keep them", owner="person",
                 artefact={"kind": "brain_record", "label": "every red line with its reason, on the record", "draft": "\n".join(f"- {x['text']}: why?" for x in rl.get("without_reason") or []) or None},
                 steps=[{"n": 1, "who": "agent", "text": "List the red lines with no reason, newest first."}, {"n": 2, "who": "person", "text": "Type one line of why for each in the register."}, {"n": 3, "who": "agent", "text": "The reason lands on the record; the brain file carries it under strict rules."}],
                 check_on=_check_on(f, 14), time_to_ship_hours=0.25)
    elif rid == "BRN-R33":
        au = f.get("audiences") or {}
        top = ", ".join(f"{x['name']} ({round((x['share'] or 0) * 100)} percent)" for x in au.get("top") or [])
        a.update(title="Approve the audience profiles and pick the default for ads", owner="person",
                 artefact={"kind": "brain_record", "label": "approved profiles and a default per surface every generator reads", "draft": ("Top profiles by share: " + top + ".") if top else None},
                 steps=[{"n": 1, "who": "agent", "text": "Show the profiles by share with the doubts each raises and the proof on file."}, {"n": 2, "who": "person", "text": "Approve the ones that are real, and pick the default for ads, email, the product page and CX."}, {"n": 3, "who": "agent", "text": "The brain file lists them under judgement rules; every brief names one."}],
                 check_on=_check_on(f, 14), time_to_ship_hours=0.5)
    elif rid == "BRN-R32":
        dz = f.get("drift") or {}
        a.update(title="Redraft the positioning frame with the words customers use" + (": " + ", ".join(dz.get("missing") or [])[:60] if dz.get("missing") else ""), owner="agent_drafts",
                 artefact={"kind": "brain_record", "label": "a positioning frame that customers echo, every claim tied to a record", "draft": dz.get("brief")},
                 steps=[{"n": 1, "who": "agent", "text": "Draft 2 frames from the drift brief: one that adds the customers' words, one that drops the contradicted ones."}, {"n": 2, "who": "person", "text": "Pick one, or edit it in the profile."}, {"n": 3, "who": "agent", "text": "Write it as the approved frame; the brain file and every brief read it. Re-run the drift check next month."}],
                 check_on=_check_on(f, 30), time_to_ship_hours=1)
    elif rid == "BRN-R31":
        cz = f.get("consent") or {}
        expired = cz.get("state") == "expired"
        a.update(title=(f"Renew or drop {cz.get('name')}'s quote: the consent expired" if expired else f"Renew {cz.get('name')}'s consent before {cz.get('expires_on')} ({cz.get('days_left')} days)"), owner="person" if expired else "agent_drafts",
                 artefact={"kind": "email", "label": "a renewal ask to the person, or the placements to take the quote off", "draft": f"Hi {cz.get('name')}, our permission to use your words (\"{str(cz.get('what'))[:120]}\") on {', '.join(cz.get('scope') or []) or 'our site'} {'ended on' if expired else 'ends on'} {cz.get('expires_on')}. May we keep using it for another 12 months on the same terms? Reply yes and we keep your reply on file. You can withdraw any time."},
                 steps=[{"n": 1, "who": "agent", "text": "Send the drafted ask on the channel the consent came on (" + str(cz.get("channel") or "the same channel") + ")."}, {"n": 2, "who": "person", "text": "On a yes, put the reply on file with the date; on no answer, take the quote off " + (", ".join(cz.get("scope") or []) or "the site") + "."}, {"n": 3, "who": "agent", "text": "Update the consent record; the review route reads it."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R30":
        az = f.get("asset") or {}
        act = az.get("action") or {}
        st = az.get("state")
        steps = {"expired_live": [{"n": 1, "who": "person", "text": f"Decide: take {az.get('name')} down from {', '.join(az.get('where') or []) or 'where it is live'} today, or renew."}, {"n": 2, "who": "agent", "text": "Send the drafted renewal request to the rights holder, or list the placements to remove."}, {"n": 3, "who": "person", "text": "Confirm the takedown or the new term; the record updates."}],
                 "inside_window": [{"n": 1, "who": "agent", "text": "Send the drafted renewal request to the rights holder with the current use listed."}, {"n": 2, "who": "person", "text": "Approve the price and the term."}, {"n": 3, "who": "agent", "text": "Write the new expiry date on the record."}]}.get(st, [{"n": 1, "who": "person", "text": f"Find the licence for {az.get('name')} and type the expiry date on the asset record."}, {"n": 2, "who": "agent", "text": "The window check runs from that date."}])
        a.update(title=act.get("title") or f"Check the right to {label}", owner=act.get("owner") or "person",
                 artefact={"kind": "email" if st in ("expired_live", "inside_window") else "brain_record", "label": "a renewal request to the rights holder, or the takedown list" if st in ("expired_live", "inside_window") else "the expiry date on the asset record", "draft": act.get("draft")},
                 steps=steps, check_on=_check_on(f, 3 if st == "expired_live" else 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R29":
        rj = f.get("rejected") or {}
        a.update(title=f"Review the rejected idea {rj.get('idea_id')}: keep it out or bring it back", owner="person",
                 artefact={"kind": "brain_record", "label": "the rejection extended with a new review date, or the idea back in the unlocks", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": f"Show the idea, the reason you gave ({rj.get('reason') or 'none'}) and what changed in the brain since {rj.get('rejected_on') or 'then'}."},
                        {"n": 2, "who": "person", "text": "Keep it out with a new review date, or bring it back so it can be picked."},
                        {"n": 3, "who": "agent", "text": "Write the record. Agents read the learnings before proposing."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.25)
    elif rid == "BRN-R28":
        vb = f.get("visibility") or {}
        nl, nr = len(vb.get("leaks") or []), len(vb.get("restricted") or [])
        a.update(title=("Keep " + str(_ev(f, "public_records_from_private_sources")) + " records inside: flip them to private" if nl else "Open " + str(_ev(f, "private_records_from_public_sources")) + " public-source records to public-facing agents"), owner="person",
                 artefact={"kind": "brain_record", "label": "every record on the right side of the public line", "draft": "\n".join(f"{x['id']}: {x['why']}" for x in (vb.get("leaks") or []) + (vb.get("restricted") or []))[:1200] or None},
                 steps=[{"n": 1, "who": "agent", "text": "List each record with its source and why the flag looks wrong, leaks first."},
                        {"n": 2, "who": "person", "text": "Fix all, or unpick the ones that should stay as they are."},
                        {"n": 3, "who": "agent", "text": "Flip the flags and log each change. Public-facing packages rebuild on the next load."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R27":
        vz = f.get("visual") or {}
        steps = []
        if not vz.get("colours"):
            steps.append({"n": 1, "who": "agent", "text": "Read the colour and font tokens from the site's stylesheet (read-only crawl) into the visual section."})
        if not vz.get("logo"):
            steps.append({"n": len(steps) + 1, "who": "person", "text": "Set the logo rules: minimum size, clear space, what never happens to it, which backgrounds."})
        if vz.get("fails"):
            steps.append({"n": len(steps) + 1, "who": "person", "text": "Pick a darker text or lighter background for: " + "; ".join(vz["fails"]) + "."})
        steps.append({"n": len(steps) + 1, "who": "agent", "text": "Every generated creative and email is checked against the palette, the fonts and the logo rules before review."})
        a.update(title="Complete the visual identity: " + ", ".join(vz.get("gaps") or [label]), owner="agent_drafts" if not vz.get("colours") else "person",
                 artefact={"kind": "brain_record", "label": "colour tokens, fonts and logo rules the creative checks read", "draft": None}, steps=steps, check_on=_check_on(f, 14), time_to_ship_hours=1)
    elif rid == "BRN-R26":
        pk = f.get("peak") or {}
        gaps = pk.get("gaps") or []
        when = f" ({pk['days_to']} days)" if pk.get("days_to") is not None else ""
        offer_gap = any(g["key"] == "offer" for g in gaps)
        steps = []
        for g in gaps[:5]:
            steps.append({"n": len(steps) + 1, "who": "person" if g["who"] == "person" else "agent", "text": g["fix"]})
        steps.append({"n": len(steps) + 1, "who": "agent", "text": f"Write the decisions as founder records; the site, email, ads and CX screens read them for {pk.get('label') or label}."})
        if len(steps) < 2:
            steps.insert(0, {"n": 1, "who": "agent", "text": "List the checks and what each one waits on."})
            steps = [dict(x, n=i + 1) for i, x in enumerate(steps)]
        draft = f"Peak plan: {pk.get('label')}" + (f", {pk.get('date')}" if pk.get("date") else "") + "\n" + "\n".join(f"- {g['label']}: {g['fix']}" for g in gaps) + ("\nNot checkable yet: " + ", ".join(pk.get("unavailable") or []) if pk.get("unavailable") else "")
        a.update(title=f"Get ready for {pk.get('label') or label}{when}: " + ", ".join(g["label"].lower() for g in gaps[:3]), owner="person" if offer_gap and len(gaps) == 1 else "agent_drafts",
                 artefact={"kind": "offer" if offer_gap else "brain_record", "label": f"the {pk.get('label') or label} plan as founder records: offer, window, cutoff, creative brief", "draft": draft},
                 steps=steps[:8], check_on=_check_on(f, 7), time_to_ship_hours=2)
    elif rid == "BRN-R24":
        r = f.get("router") or {}
        a.update(title="Regenerate BRAIN.md" + (f" and fix {len(r.get('broken') or [])} broken link{'s' if len(r.get('broken') or []) != 1 else ''}" if r.get("broken") else ": the router no longer matches the records"), owner="agent",
                 artefact={"kind": "brain_record", "label": "BRAIN.md rebuilt from the records, founder notes kept", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Regenerate BRAIN.md from the records. The founder notes block is kept word for word."}]
                       + ([{"n": 2, "who": "person", "text": "Create the missing files or point the rows at ones that exist: " + ", ".join(r["broken"][:3]) + "."}] if r.get("broken") else [])
                       + [{"n": 3 if r.get("broken") else 2, "who": "agent", "text": "Run the self audit again. The finding resolves when no row drifts and every link resolves."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R25":
        d = f.get("duplicates") or []
        n = _ev(f, "duplicate_pairs") or len(d)
        a.update(title=f"Retire {n} duplicate record{'s' if n != 1 else ''}, keeping the stronger of each pair", owner="agent",
                 artefact={"kind": "brain_record", "label": "one active record per fact; the weaker twin retired to history", "draft": "\n".join(f"keep {x['keep']} ({x['keep_tier']}), retire {x['retire']} ({x['retire_tier']}): {x['match']}" for x in d[:8]) or None},
                 steps=[{"n": 1, "who": "agent", "text": "List each pair with the record to keep (source rank, confidence, capture date) and the one to retire."},
                        {"n": 2, "who": "person", "text": "Approve the list, or unpick a pair where both should stay."},
                        {"n": 3, "who": "agent", "text": "Retire the weaker twins. Retire never deletes; the changes log keeps each."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=0.5)
    elif rid == "BRN-R21":
        a.update(title=f"Confirm or correct: {label}", owner="person",
                 artefact={"kind": "brain_record", "label": "your number as an approved record; the generator reads it next run", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Show the modelled value, the reasoning and the rooms that read it, in the assumptions register."},
                        {"n": 2, "who": "person", "text": "Confirm it as is, or type the real number."},
                        {"n": 3, "who": "agent", "text": "Write the approved record. The next generator run and every screen use your number."}],
                 check_on=_check_on(f, 14), time_to_ship_hours=1)
    elif rid == "BRN-R20":
        a.update(title="Set who sees which part of the brain", owner="person",
                 artefact={"kind": "policy", "label": "the permission map: sections by role", "draft": None},
                 steps=[{"n": 1, "who": "person", "text": "In the permissions block, set agency and specialist access per section. Restricted stays the default."},
                        {"n": 2, "who": "agent", "text": "Apply the map to every brain answer and every screen once hosting and auth are live."}],
                 check_on=_check_on(f, 30), time_to_ship_hours=1)
    elif rid == "BRN-R17":
        d = _ev(f, "days_to_renewal")
        a.update(title=f"Renegotiate or renew {label}" + (f": {d} days left" if isinstance(d, (int, float)) and d >= 0 else ": date passed"), owner="person",
                 artefact={"kind": "ticket", "label": "3 asks (rate, term, exit) and the notice, ready to send", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Pull the last terms and 12 months of spend with this vendor from finance, if connected."},
                        {"n": 2, "who": "agent", "text": "Draft 3 asks: rate, term, exit clause. Name 2 alternatives from the sources registry."},
                        {"n": 3, "who": "person", "text": "Send the notice before the notice deadline, or let it renew on purpose and log the decision."},
                        {"n": 4, "who": "agent", "text": "Write the new terms into the contract record."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=2)
    elif rid == "BRN-R18":
        many = ent.get("id") == "contracts_missing"
        a.update(title="Put the vendor contracts on file" if many else f"Add the renewal date for {label}", owner="person",
                 artefact={"kind": "brain_record", "label": "contract records with renewal dates and rate cards", "draft": None},
                 steps=[{"n": 1, "who": "person", "text": "Type the vendor, type, renewal date, notice days and rate card in the contracts block, or drop the contract in Files in."},
                        {"n": 2, "who": "agent", "text": "Set the alert window by vendor type and watch the date."}],
                 check_on=_check_on(f, 14), time_to_ship_hours=1)
    elif rid == "BRN-R19":
        a.update(title=f"Fix before going live: {label}", owner="person",
                 artefact={"kind": "policy", "label": "the disclosure in place on the page, checked", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Draft the missing text from the brain's policy records and the rule family named."},
                        {"n": 2, "who": "person", "text": "Sign it off with counsel where needed and publish it."},
                        {"n": 3, "who": "agent", "text": "Re-crawl the page and close the check."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=2)
    elif rid == "BRN-R15":
        a.update(title=f"Send a MAP notice for {label}", owner="agent_drafts",
                 artefact={"kind": "ticket", "label": "a MAP violation notice with the proof (listing, price, date)", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Capture the proof: listing url, price per pair, pack count, date, seller if known."},
                        {"n": 2, "who": "agent", "text": "Draft the notice from the brand's template with the proof attached."},
                        {"n": 3, "who": "person", "text": "Send it, or raise the price on our own listing if the seller is us."},
                        {"n": 4, "who": "agent", "text": "Re-pull the listing in 7 days and close the finding when the price is at or above MAP."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R16":
        a.update(title=f"Check the seller on {label}", owner="agent_drafts",
                 artefact={"kind": "ticket", "label": "an unauthorised seller report with the listing and the seller name", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Record the seller name, the listing and the price. Compare with the founder's seller list."},
                        {"n": 2, "who": "person", "text": "Confirm it is not a retail partner. If it is, add the name to the list."},
                        {"n": 3, "who": "agent", "text": "Draft the report for Amazon Brand Registry. You send it."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R14":
        sc = f.get("site_change") or {}
        act = sc.get("action") or {}
        a.update(title=act.get("title") or f"Review the site change: {label}", owner=act.get("owner") or "agent",
                 artefact={"kind": act.get("artefact") or "brain_record", "label": "the brain and every surface carrying the old value updated", "draft": None},
                 steps=act.get("steps") or a["steps"], check_on=_check_on(f, 7), time_to_ship_hours=2)
        if sc.get("section") in ("claims", "policies"):
            f = dict(f, entity={"type": "brand", "id": ent.get("id"), "label": "policy claim " + label})
    elif rid == "BRN-R13":
        a.update(title=f"Tier the {label} claim: approve it or forbid it", owner="person",
                 artefact={"kind": "brain_record", "label": "the claim tiered approved or forbidden by you", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Show the claim, its source and every rung and surface that uses it, in the claims desk."},
                        {"n": 2, "who": "person", "text": "Approve as is, or forbid it. One click."},
                        {"n": 3, "who": "agent", "text": "If forbidden, the scanner blocks the phrase in every draft and the rungs re-point at an approved claim."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    elif rid == "BRN-R12":
        a.update(title=f"Decide {label}: two sources disagree", owner="person",
                 artefact={"kind": "brain_record", "label": "an approved founder record for the field, decision logged", "draft": None},
                 steps=[{"n": 1, "who": "agent", "text": "Show both values with their sources and the default winner."},
                        {"n": 2, "who": "person", "text": "Pick one, or type the right value with a reason, in the conflicts block."},
                        {"n": 3, "who": "agent", "text": "Write the approved record and the decision. Every screen reads it on its next load."}],
                 check_on=_check_on(f, 7), time_to_ship_hours=1)
    # rubric with the documented reputation overrides, total recomputed with the fixed weights
    r = dict(rank_mod.score(dict(f, owner=a["owner"]), nr))
    if rid in REPUTATION_OVERRIDE:
        r["reputation"] = max(r["reputation"], REPUTATION_OVERRIDE[rid])
    if rid == "BRN-R08" and f.get("own_positioning"):
        r["reputation"] = 5
    if rid == "BRN-R12" and any(w in (label or "") for w in ("claim", "polic", "guarantee", "return")):
        r["reputation"] = 5
    r["ease"] = {"agent": 5, "agent_drafts": 4, "person": 3 if a["artefact"].get("draft") else 2}[a["owner"]]
    total = 0.0
    for k, w in rank_mod.WEIGHTS.items():
        v = r[k] if r[k] is not None else 2.5
        total += w * v / 5
    r["total"] = round(total, 1)
    a["rubric"] = r
    return a


def rank(brand: str, window: dict | None, audit_run) -> dict:
    window = window or rank_mod.default_window()
    nr = rank_mod.net_revenue_28d(brand, window)
    findings = audit_run(brand, window)
    actions = [build(f, nr) for f in findings if f.get("status") in ("open", "unavailable", None)]
    good = [a for a in actions if not rank_mod.validate_action(a)]
    good.sort(key=rank_mod.sort_key)
    return {"screen": "05-brand-brain", "brand": brand, "window": window, "simulated": True, "source": "screen", "net_revenue_28d": nr, "actions": good}
