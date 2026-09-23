import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import index_cro
class RelationNamespaceTests(unittest.TestCase):
    def test_round_local_ids_do_not_link_to_another_round(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);d=root/'data/cro-folder-v1';d.mkdir(parents=True)
            (root/'data/cro-folder-proposal.json').write_text(json.dumps({'batches':[{}]}))
            for round_index,ids in enumerate([['a','b'],['c','d']]):
                cards=[{'id':uid,'unit':{'id':'u'+str(i+1),'kind':'principle','claim':{'text':uid},'relations':[{'kind':'depends_on','target':'u2'}] if i==0 else []}} for i,uid in enumerate(ids)]
                row={'batch':0,'round':round_index,'request_id':str(round_index),'held':[],'errors':[],'candidates':cards,'more_units':False,'unresolved':[],'finish_reason':'stop'}
                (d/f'batch-000-round-{round_index}.json').write_text(json.dumps(row))
            with patch.object(index_cro,'ROOT',root),patch('builtins.print'):index_cro.main()
            cards={c['id']:c for c in json.loads((d/'candidate-index.json').read_text())['cards']}
            self.assertEqual(cards['a']['resolved_relations'][0]['target'],'b')
            self.assertEqual(cards['c']['resolved_relations'][0]['target'],'d')
            self.assertFalse(cards['a']['publication_allowed'])
