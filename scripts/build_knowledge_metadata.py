"""Generate a sidecar without changing card text, IDs or embeddings."""
from build_library import ROOT,DEST,read,write
from intelligence.knowledge_metadata import build_metadata,VERSION
from collections import Counter

def main():
 cards=read(DEST/'cards.json')['cards'];p=DEST/'metadata-overrides.json'
 metadata=build_metadata(cards,read(p) if p.exists() else {})
 old=read(DEST/'metadata.json')['cards'] if (DEST/'metadata.json').exists() else {}
 for k,m in metadata.items():
  if k in old and old[k].get('content_hash')==m['content_hash'] and m['classification_status']!='reviewed':metadata[k]=old[k]
 write(DEST/'metadata.json',{'schema_version':VERSION,'cards':metadata})
 print({'cards':len(metadata),'types':dict(Counter(m['knowledge_type'] for m in metadata.values())),
        'durability':dict(Counter(m['durability'] for m in metadata.values()))})
if __name__=='__main__':main()
