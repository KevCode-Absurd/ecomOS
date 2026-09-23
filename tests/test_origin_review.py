import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prepare_origin_review import classify_blocks

class OriginReviewTests(unittest.TestCase):
    def test_editorial_precedes_length_rule(self):
        result=classify_blocks([{'locator':'a','text':'Topics. '+'x'*5000}])[0]
        self.assertEqual(result['proposed_origin'],'editorial_candidate')
        self.assertEqual(result['verified_origin'],'unknown')
    def test_frontmatter_continuations(self):
        rows=[{'locator':str(i),'text':t} for i,t in enumerate(['---','why: summary','continued summary','---','short original passage'])]
        labels=classify_blocks(rows)
        self.assertEqual(labels[2]['proposed_origin'],'metadata_candidate')
        self.assertEqual(labels[4]['proposed_origin'],'needs_review')
    def test_long_text_not_certified(self):
        row=classify_blocks([{'locator':'a','text':'Transcript text '*500}])[0]
        self.assertEqual(row['proposed_origin'],'body_candidate')
        self.assertEqual(row['verified_origin'],'unknown')
    def test_internal_horizontal_rule_does_not_hide_body(self):
        rows=[{'locator':str(i),'text':t} for i,t in enumerate(['Introduction','---','Transcript '*500])]
        self.assertEqual(classify_blocks(rows)[2]['proposed_origin'],'body_candidate')
    def test_unclosed_frontmatter_does_not_hide_body(self):
        rows=[{'locator':str(i),'text':t} for i,t in enumerate(['---','why: note','Transcript '*500])]
        self.assertEqual(classify_blocks(rows)[2]['proposed_origin'],'body_candidate')
