import tempfile
import unittest
from pathlib import Path
from intelligence.budget import Budget

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'budget.sqlite'
        self.b=Budget(self.path,working_usd=1,absolute_usd=2)
    def tearDown(self):
        self.b.close()
        self.temp.cleanup()
    def test_pending_reservations_count(self):
        self.b.reserve('a','test',.8)
        with self.assertRaises(ValueError): self.b.reserve('b','test',.3)
        self.b.settle('a',.2)
        self.b.reserve('b','test',.3)
        self.assertEqual(self.b.summary()['committed_usd'],.5)
    def test_reopen_cannot_reset_budget(self):
        self.b.reserve('a','test',.8)
        other=Budget(self.path,160,200)
        try:
            with self.assertRaises(ValueError): other.reserve('b','test',.3)
        finally: other.close()
    def test_duplicate_request_rejected(self):
        self.b.reserve('a','test',.1)
        with self.assertRaises(ValueError): self.b.reserve('a','test',.1)
    def test_underestimate_halts_new_dispatch(self):
        self.b.reserve('a','test',.1)
        with self.assertRaises(ValueError): self.b.settle('a',.2)
        with self.assertRaises(ValueError): self.b.reserve('b','test',.1)
    def test_invalid_amount(self):
        for amount in [-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError): self.b.reserve('a','test',amount)
