import unittest
from intelligence.segmentation import split_block

class SegmentationTests(unittest.TestCase):
    def test_lossless_coverage_and_offsets(self):
        for text in ['x'*35001, ('Sentence with spaces.\n'*1600), '你好🙂'*6000]:
            pieces=list(split_block(text,10000,500))
            covered=0
            rebuilt=''
            for p in pieces:
                self.assertLessEqual(len(p['text']),10000)
                self.assertEqual(p['text'],text[p['start']:p['end']])
                self.assertLessEqual(p['start'],covered)
                rebuilt += text[max(covered,p['start']):p['end']]
                covered=p['end']
            self.assertEqual(rebuilt,text)
    def test_empty(self):
        self.assertEqual(list(split_block('')),[])
    def test_invalid_bounds(self):
        with self.assertRaises(ValueError):
            list(split_block('abc',10,10))
