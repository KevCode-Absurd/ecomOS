"""Single-user local staging store. NOT an authenticated production service."""
import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from .parsing import digest, parse_document
from .conditions import validate as validate_condition

MODULES = set("PRD AVT OFF BRD SET MEA LPG SPD CRO MCR ADC GAD ORG EML SEO AEO CXP COG WLD FIN OPS AMZ SEC".split())


class Store:
    def __init__(self, directory):
        self.root = Path(directory)
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root / "knowledge.sqlite")
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS versions (
          id TEXT PRIMARY KEY, source_id TEXT NOT NULL, scope TEXT NOT NULL,
          hash TEXT NOT NULL, name TEXT NOT NULL, is_current INTEGER NOT NULL,
          permitted INTEGER NOT NULL DEFAULT 0, reviewer TEXT, media_json TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS passages (
          id TEXT PRIMARY KEY, version_id TEXT NOT NULL REFERENCES versions(id),
          locator TEXT NOT NULL, text TEXT NOT NULL, origin TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS cards (
          id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL,
          reviewer TEXT, reviewed_at TEXT);
        CREATE TABLE IF NOT EXISTS evidence (
          card_id TEXT REFERENCES cards(id), passage_id TEXT REFERENCES passages(id),
          PRIMARY KEY(card_id,passage_id));
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY, at TEXT NOT NULL, kind TEXT NOT NULL, subject TEXT NOT NULL);
        ''')

    def close(self):
        self.db.close()

    def event(self, kind, subject):
        self.db.execute("INSERT INTO events(at,kind,subject) VALUES(?,?,?)",
                        (datetime.now(timezone.utc).isoformat(), kind, subject))

    def ingest(self, source_id, scope, raw, name):
        if not source_id or not scope:
            raise ValueError("Explicit source identity and scope required")
        sha = digest(raw)
        vid = digest((scope + "\0" + source_id + "\0" + sha).encode())
        existing = self.db.execute("SELECT is_current FROM versions WHERE id=?", (vid,)).fetchone()
        if existing:
            # Reimport of an older version must not silently reactivate it.
            return {"version_id": vid, "changed": False, "is_current": bool(existing[0])}
        blocks, media = parse_document(raw, name)
        if not blocks:
            raise ValueError("No readable blocks; hold for review")
        snapshot = self.root / "objects" / sha
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        if not snapshot.exists():
            snapshot.write_bytes(raw)
        with self.db:
            self.db.execute("UPDATE versions SET is_current=0 WHERE source_id=? AND scope=?", (source_id, scope))
            self.db.execute("INSERT INTO versions VALUES(?,?,?,?,?,1,0,NULL,?)",
                            (vid, source_id, scope, sha, name, json.dumps(media)))
            for b in blocks:
                pid = digest((vid + "\0" + b["locator"]).encode())
                self.db.execute("INSERT INTO passages VALUES(?,?,?,?,?)",
                                (pid, vid, b["locator"], b["text"], b["origin"]))
            self.db.execute('''UPDATE cards SET status='stale' WHERE id IN
               (SELECT evidence.card_id FROM evidence JOIN passages p ON p.id=evidence.passage_id
                JOIN versions v ON v.id=p.version_id WHERE v.source_id=? AND v.scope=? AND v.is_current=0)''',
                            (source_id, scope))
            self.event("source_ingested", vid)
        return {"version_id": vid, "changed": True, "blocks": len(blocks), "media": len(media)}

    def review_source(self, version_id, reviewer, permitted):
        if not reviewer.strip():
            raise ValueError("Named reviewer required")
        with self.db:
            cur = self.db.execute("UPDATE versions SET permitted=?,reviewer=? WHERE id=?",
                                  (bool(permitted), reviewer, version_id))
            if cur.rowcount != 1:
                raise ValueError("Unknown source version")
            if not permitted:
                self.db.execute('''UPDATE cards SET status='held' WHERE id IN
                    (SELECT e.card_id FROM evidence e JOIN passages p ON p.id=e.passage_id
                     WHERE p.version_id=?)''', (version_id,))
            self.event("source_permitted" if permitted else "source_revoked", version_id)

    def classify_origin(self, passage_id, origin):
        if origin not in {"original", "generated_analysis", "human_annotation", "unknown"}:
            raise ValueError("Unknown origin")
        with self.db:
            cur = self.db.execute("UPDATE passages SET origin=? WHERE id=?", (origin, passage_id))
            if cur.rowcount != 1:
                raise ValueError("Unknown passage")
            if origin != "original":
                self.db.execute("UPDATE cards SET status='held' WHERE id IN (SELECT card_id FROM evidence WHERE passage_id=?)", (passage_id,))
            self.event("origin_" + origin, passage_id)

    def passages(self, version_id):
        return [dict(r) for r in self.db.execute("SELECT * FROM passages WHERE version_id=? ORDER BY locator", (version_id,))]

    def validate(self, card, require_publishable=False):
        fields = {"id", "scope", "title", "claim", "action", "modules", "applies_when",
                  "do_not_use_when", "unknowns", "evidence", "review_due", "dependencies"}
        if set(card) != fields:
            raise ValueError("Card fields do not match schema: " + str(fields ^ set(card)))
        for f in ["id", "scope", "title", "claim", "action", "review_due"]:
            if not isinstance(card[f], str) or not card[f].strip():
                raise ValueError(f + " must be a nonempty string")
        date.fromisoformat(card["review_due"])
        for f in ["modules", "unknowns", "dependencies"]:
            if not isinstance(card[f], list) or not all(isinstance(x, str) and x for x in card[f]):
                raise ValueError(f + " must be a string list")
        if not card["modules"] or not set(card["modules"]) <= MODULES:
            raise ValueError("Unknown or empty module list")
        if card["id"] in card["dependencies"]:
            raise ValueError("Self dependency")
        for f in ["applies_when", "do_not_use_when"]:
            validate_condition(card[f])
        if not isinstance(card["evidence"], list) or not card["evidence"]:
            raise ValueError("At least one supporting passage required")
        for e in card["evidence"]:
            if not isinstance(e,dict) or set(e) != {"passage_id", "quote"} or not isinstance(e["quote"],str) or not e["quote"].strip():
                raise ValueError("Evidence needs passage_id and nonempty quote")
            row = self.db.execute('''SELECT p.*,v.scope,v.permitted,v.is_current FROM passages p
                JOIN versions v ON v.id=p.version_id WHERE p.id=?''', (e["passage_id"],)).fetchone()
            if not row or e["quote"] not in row["text"]:
                raise ValueError("Evidence quote does not match its source passage")
            if row["scope"] not in {"global", card["scope"]}:
                raise ValueError("Evidence scope mismatch")
            if require_publishable and (not row["permitted"] or not row["is_current"] or row["origin"] != "original"):
                raise ValueError("Evidence is unreviewed, stale, restricted, or not original")
        if require_publishable:
            if date.fromisoformat(card["review_due"]) < date.today():
                raise ValueError("Review has expired")
            for dep in card["dependencies"]:
                row = self.db.execute("SELECT payload,status FROM cards WHERE id=?", (dep,)).fetchone()
                if not row or row["status"] != "approved" or json.loads(row["payload"])["scope"] not in {"global",card["scope"]}:
                    raise ValueError("Dependency is unavailable")

    def add_card(self, card):
        self.validate(card)
        with self.db:
            self.db.execute("INSERT INTO cards VALUES(?,?,'review_required',NULL,NULL)", (card["id"], json.dumps(card)))
            for e in card["evidence"]:
                self.db.execute("INSERT OR IGNORE INTO evidence VALUES(?,?)", (card["id"],e["passage_id"]))
            self.event("card_created", card["id"])

    def approve_card(self, card_id, reviewer):
        if not reviewer.strip():
            raise ValueError("Named reviewer required")
        row = self.db.execute("SELECT payload FROM cards WHERE id=?", (card_id,)).fetchone()
        if not row:
            raise ValueError("Unknown card")
        self.validate(json.loads(row[0]), require_publishable=True)
        with self.db:
            self.db.execute("UPDATE cards SET status='approved',reviewer=?,reviewed_at=? WHERE id=?",
                            (reviewer, datetime.now(timezone.utc).isoformat(), card_id))
            self.event("card_approved", card_id)

    def eligible_cards(self, authorized_scopes):
        # The production API must derive these scopes from authenticated membership.
        if not authorized_scopes:
            return []
        result = []
        for row in self.db.execute("SELECT payload FROM cards WHERE status='approved'"):
            card = json.loads(row[0])
            if card["scope"] not in authorized_scopes:
                continue
            try:
                self.validate(card, require_publishable=True)
            except ValueError:
                continue
            result.append(card)
        return result
