import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prepare_cro_context import packet
class ContextPacketTests(unittest.TestCase):
    def test_neighbor_retrieval_preserves_primary_span_and_source_offsets(self):
        blocks=[{'locator':'p1','text':'Before: only above threshold.'},{'locator':'p2','text':'Do the analysis.'},{'locator':'p3','text':'Otherwise use an alternative.'}]
        batch={'source_id':'s','segments':[{'source_sha256':'v','locator':'p2','start':0,'end':16}]}
        p=packet(batch,blocks,neighbor_chars=100)
        self.assertEqual(p['text'][p['primary_start']:p['primary_end']],'Do the analysis.')
        self.assertIn('only above threshold',p['text']);self.assertIn('Otherwise',p['text'])
        for s in p['evidence_spans']:self.assertEqual(p['text'][s['packet_start']:s['packet_end']],s['text'])
