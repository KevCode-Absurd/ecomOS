import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ingest_cro import assemble,validate
from intelligence.units import bind
class FolderEvidenceTests(unittest.TestCase):
    def test_mapping_preserves_original_offsets(self):
        source,spans=assemble({'source_id':'s','segments':[{'source_id':'s','source_sha256':'h','locator':'p1','start':7,'text':'First.'},{'source_id':'s','source_sha256':'h','locator':'p2','start':13,'text':'Second.'}]})
        self.assertEqual(source['text'],'First.\n\nSecond.')
        unit={'id':'u','kind':'principle','title':'A','claim':{'text':'Second','quote':'Second.'},'action':None,'trigger':{'op':'all','args':[]},'prerequisites':{'op':'all','args':[]},'exclusions':{'op':'any','args':[]},'completion':[],'unknowns':[],'relations':[]}
        checked=validate({'output':{'units':[unit],'more_units':False,'unresolved':[]}},source,spans)
        e=checked['candidates'][0]['evidence'][0]
        self.assertEqual((e['locator'],e['start'],e['end']),('p2',13,20))
        unit['claim']['quote']='First.\n\nSecond.'
        checked=validate({'output':{'units':[unit],'more_units':False,'unresolved':[]}},source,spans)
        self.assertEqual(len(checked['candidates']),1)
        self.assertEqual([(e['locator'],e['start'],e['quote']) for e in checked['candidates'][0]['evidence']],[('p1',7,'First.'),('p2',13,'Second.')])
        self.assertEqual(checked['held'],[])
