"""Agent-facing search: one compact context packet, no duplicate full-card objects."""
import argparse,json
from calibration_client import ROOT
from intelligence.knowledge_search import KnowledgeEngine
from library_embeddings import embed
_ENGINE=None

def engine():
 global _ENGINE
 if _ENGINE is None:_ENGINE=KnowledgeEngine(ROOT/'data/library-v3',embed_query=lambda text:embed([text])[0])
 return _ENGINE

def search_knowledge(task,**kwargs):return engine().search(task,**kwargs)
def get_knowledge_card(card_id):return engine().get_card(card_id)

def main():
 p=argparse.ArgumentParser();p.add_argument('task');p.add_argument('--keyword-only',action='store_true')
 p.add_argument('--complexity',choices=['focused','multi-part','broad'],default='focused')
 p.add_argument('--token-budget',type=int);p.add_argument('--max-cards',type=int)
 for f in ['domain','platform','role','knowledge-type','durability','brand-context']:p.add_argument('--'+f)
 a=vars(p.parse_args());a['semantic']=not a.pop('keyword_only')
 print(json.dumps(search_knowledge(**a),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
