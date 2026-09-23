"""Durable, conservative USD reservations for cooperating model workers.

Callers must reserve a valid upper bound before dispatch. Unknown outcomes retain
their reservation. This controls this pipeline, not unrelated account spending.
"""
import sqlite3
from decimal import Decimal, ROUND_CEILING

def micros(value):
    number=Decimal(str(value))
    if not number.is_finite() or number<0:
        raise ValueError('Expected finite nonnegative USD')
    return int((number*1_000_000).to_integral_value(rounding=ROUND_CEILING))

class Budget:
    def __init__(self,path,working_usd=160,absolute_usd=200):
        self.db=sqlite3.connect(path,timeout=30)
        working,absolute=micros(working_usd),micros(absolute_usd)
        if working>absolute:
            raise ValueError('Working limit exceeds absolute ceiling')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS budget_config
          (id INTEGER PRIMARY KEY CHECK(id=1), working INTEGER, absolute INTEGER);
          CREATE TABLE IF NOT EXISTS spend
          (request_id TEXT PRIMARY KEY, provider TEXT NOT NULL, reserved INTEGER NOT NULL,
           actual INTEGER, status TEXT NOT NULL);''')
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO budget_config VALUES(1,?,?)',(working,absolute))
        # Existing persisted limits take precedence; reopening cannot increase them.

    def reserve(self,request_id,provider,upper_bound_usd):
        amount=micros(upper_bound_usd)
        if not request_id or not provider or amount<=0:
            raise ValueError('Request, provider and positive bound required')
        try:
            self.db.execute('BEGIN IMMEDIATE')
            if self.db.execute('SELECT 1 FROM spend WHERE request_id=?',(request_id,)).fetchone():
                raise ValueError('Request already recorded; do not dispatch twice')
            limit=self.db.execute('SELECT MIN(working,absolute) FROM budget_config WHERE id=1').fetchone()[0]
            used=self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM spend').fetchone()[0]
            if used+amount>limit:
                raise ValueError('Budget exhausted including pending requests')
            self.db.execute("INSERT INTO spend VALUES(?,?,?,NULL,'reserved')",(request_id,provider,amount))
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def settle(self,request_id,actual_usd):
        amount=micros(actual_usd)
        with self.db:
            row=self.db.execute('SELECT reserved,actual FROM spend WHERE request_id=?',(request_id,)).fetchone()
            if not row or row[1] is not None:
                raise ValueError('Missing or already settled request')
            self.db.execute("UPDATE spend SET actual=?,status=? WHERE request_id=?",
                            (amount,'bound_exceeded' if amount>row[0] else 'settled',request_id))
            if amount>row[0]:
                self.db.execute('UPDATE budget_config SET working=0 WHERE id=1')
        if amount>row[0]:
            raise ValueError('Reservation underestimated: dispatch halted')

    def summary(self):
        total=self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM spend').fetchone()[0]
        pending=self.db.execute('SELECT COUNT(*) FROM spend WHERE actual IS NULL').fetchone()[0]
        return {'committed_usd':total/1_000_000,'pending_requests':pending}

    def close(self):
        self.db.close()
