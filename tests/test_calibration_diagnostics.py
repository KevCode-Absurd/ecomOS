import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from summarize_calibration import quote_status


class DiagnosticTests(unittest.TestCase):
    def test_wrapper_is_diagnostic_only(self):
        self.assertEqual(quote_status('"exact text"','Some exact text here'),'added_quote_wrapper')
        self.assertEqual(quote_status('exact text','Some exact text here'),'exact')
        self.assertEqual(quote_status('"different text"','Some exact text here'),'unmatched')
