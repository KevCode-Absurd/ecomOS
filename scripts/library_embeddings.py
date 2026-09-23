"""Cached semantic vectors; shared budget, fixed OpenAI endpoint, no implicit retry."""
import hashlib
import json
import math
import sys
from calibration_client import ROOT
from bounded_process import run_bounded
from intelligence.budget import Budget

RATE = 0.10  # Conservative USD / million input tokens allowance, not an invoice quote.


def embed(texts):
    payload = {'model': 'text-embedding-3-small', 'input': texts, 'dimensions': 512}
    request_id = 'embedding-' + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    path = ROOT / 'data/library-v3/embeddings' / (request_id + '.json')
    if path.exists(): return json.loads(path.read_text(encoding='utf-8'))['vectors']
    budget = Budget(ROOT / 'data/spend.sqlite', 160, 200)
    try:
        bound = (sum(len(t.encode()) for t in texts) + 2048 * len(texts)) * RATE / 1_000_000
        budget.reserve(request_id, 'openai-embedding', bound)
        response = run_bounded([sys.executable, str(ROOT / 'scripts/http_worker.py')],
                               json.dumps({'provider': 'openai-embedding', 'payload': payload}), timeout=120)
        if response.returncode: raise ValueError('Embedding transport failed; reservation retained')
        envelope = json.loads(response.stdout)
        if envelope.get('status') != 200: raise ValueError('Embedding request failed; reservation retained')
        body = envelope['body']; tokens = body.get('usage', {}).get('total_tokens')
        if type(tokens) is not int or tokens < 0: raise ValueError('Missing usage; reservation retained')
        budget.settle(request_id, tokens * RATE / 1_000_000)
        rows = sorted(body['data'], key=lambda x: x['index'])
        if [r['index'] for r in rows] != list(range(len(texts))): raise ValueError('Embedding count mismatch')
        vectors = [r['embedding'] for r in rows]
        if any(len(v) != 512 or any(not math.isfinite(x) for x in v) for v in vectors):
            raise ValueError('Invalid vector')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({'vectors': vectors}), encoding='utf-8')
        return vectors
    finally: budget.close()


def main():
    directory = ROOT / 'data/library-v3'
    cards = json.loads((directory / 'cards.json').read_text(encoding='utf-8'))['cards']
    old_path = directory / 'vectors.json'
    old = json.loads(old_path.read_text(encoding='utf-8')) if old_path.exists() else {}
    vectors = {c['id']: old[c['id']] for c in cards if c['id'] in old}
    missing = [c for c in cards if c['id'] not in vectors]
    for start in range(0, len(missing), 64):
        batch = missing[start:start + 64]
        texts = [c['title'] + '\n' + c['summary'] + '\n' + c['use_when'] + '\n' + ' '.join(c['tags']) for c in batch]
        for card, vector in zip(batch, embed(texts)): vectors[card['id']] = vector
        old_path.write_text(json.dumps(vectors), encoding='utf-8')
    old_path.write_text(json.dumps(vectors), encoding='utf-8')
    print(json.dumps({'indexed_cards': len(vectors), 'new_cards': len(missing)}))


if __name__ == '__main__': main()
