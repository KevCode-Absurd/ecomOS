"""Write and test the positioning line against real shopper frames (BRAND-C20).

Shopper frames: the Reddit category frames the brain counts (positioning.reddit_frames: mentions, and in
positioning.reddit_frame_* how often the brand is named inside each). Our frame: positioning.frame.
Candidate lines are built by rules, never typed per brand:
  A  the current frame, as it is.
  B  the top shopper frame, answered with our proof for it (buy it for life -> the guarantee; worth the
     price -> price per wear; mission -> the giving proof; marketing brand -> a tested proof point).
  C  the contested corner of the positioning map, taken with the claim points we miss.
The test: a 5-second preference poll (200 shoppers, A against each other line), then the winner and the
current line as 2 ad first lines. positioning_test_score = share preferring the new line minus share
preferring A; unavailable until a test is on file.

Rule COMP-R28: the top shopper frame is not in our frame's words and no positioning test is on file.
"""
from __future__ import annotations

FRAME_WORDS = {"buy_it_for_life": ["last", "life", "durab", "guarantee"], "worth_the_price": ["worth", "value", "per wear"],
               "mission_giving": ["given", "donat", "giving"], "marketing_brand": ["tested", "proof", "honest"]}
FRAME_PROOF = {"buy_it_for_life": ["guarantee"], "worth_the_price": ["guarantee", "arch"], "mission_giving": ["donat"],
               "marketing_brand": ["arch", "tested", "b corp"]}
FRAME_LINE = {"buy_it_for_life": "Socks built to last, and if a pair fails, we make it right.",
              "worth_the_price": "Worth more than a multi-pack: comfort you feel every wear.",
              "mission_giving": "Every pair you buy gives a pair to someone who needs it.",
              "marketing_brand": "Not hype: comfort you can test, from arch to toe."}


def build(m: dict, brain, map_moves: list[dict] | None = None) -> dict:
    get = lambda k: (brain.get(f"{brain.brand}.{k}") or {}).get("value")  # noqa: E731
    frames = get("positioning.reddit_frames") or {}
    ours = str(get("positioning.frame") or "")
    proofs = [str(x) for x in (get("positioning.proof_points") or [])]
    rows = []
    for f, n in sorted(frames.items(), key=lambda kv: -kv[1]):
        named = (get(f"positioning.reddit_frame_{f}") or {}).get("mentions_brand")
        rows.append({"frame": f, "label": f.replace("_", " "), "mentions": n, "brand_named": named,
                     "in_our_frame": any(w in ours.lower() for w in FRAME_WORDS.get(f, [f]))})
    top = rows[0] if rows else None
    lines = [{"key": "A", "line": ours or "unavailable", "answers": "our current frame", "proof": None}]
    if top:
        proof = next((p for p in proofs if any(w in p.lower() for w in FRAME_PROOF.get(top["frame"], []))), None)
        lines.append({"key": "B", "line": FRAME_LINE.get(top["frame"], f"A line for {top['label']}"),
                      "answers": f"the top shopper frame: {top['label']} ({top['mentions']} mentions)", "proof": proof})
    contest = next((mv for mv in map_moves or [] if mv["kind"] == "contest"), None)
    if contest:
        lines.append({"key": "C", "line": f"Take the {contest['label']} corner: {contest['text']}", "answers": "the contested map corner",
                      "proof": None})
    tested = any("positioning_test" in str(r.get("field") or "") for r in brain.records("learnings"))
    fires = bool(top and not top["in_our_frame"] and not tested)
    return {"frames": rows, "our_frame": ours, "lines": lines, "tested": tested, "score": None, "fires": fires,
            "top": top, "rule": "Test when the top shopper frame is not in our frame's words and no positioning test is on file. "
                                "Score = share preferring the new line minus share preferring the current one."}


def draft(fr: dict) -> str:
    out = ["Positioning test: 5-second preference poll, 200 shoppers who bought socks in the last year.",
           "Lines:"] + [f"{x['key']}. {x['line']} (answers {x['answers']}" + (f"; proof: {x['proof']}" if x["proof"] else "") + ")"
                        for x in fr["lines"]]
    out += [f"Line {x['key']} has no proof on file: add it before the test." for x in fr["lines"] if x["key"] == "B" and not x["proof"]]
    out += ["Show A against each other line; ask which brand they would buy from. Randomise order.",
            "Then run the winner and A as 2 ad first lines for 7 days. Keep the line that wins both.",
            "Write the winner to the brain as an approved positioning record. Every claim must have its proof on file."]
    return "\n".join(out)
