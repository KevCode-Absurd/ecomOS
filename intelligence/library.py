"""Compact, private card storage and budgeted keyword retrieval."""
import hashlib
import json
import re
import sqlite3


def validate_cards(output):
    if not isinstance(output, dict) or not isinstance(output.get('cards'), list):
        raise ValueError('Expected cards list')
    cards = []
    for card in output['cards']:
        if not isinstance(card, dict):
            raise ValueError('Invalid card')
        for key in ('title', 'summary', 'use_when'):
            if not isinstance(card.get(key), str) or not card[key].strip():
                raise ValueError('Missing ' + key)
        for key in ('steps', 'caveats', 'tags'):
            if not isinstance(card.get(key), list) or any(not isinstance(x, str) for x in card[key]):
                raise ValueError('Invalid ' + key)
        if not card['steps'] or not card['tags']:
            raise ValueError('Empty instructions or tags')
        cards.append({k: card[k] for k in ('title', 'summary', 'use_when', 'steps', 'caveats', 'tags')})
    return cards


def card_id(source_id, card):
    return hashlib.sha256((source_id + json.dumps(card, sort_keys=True)).encode()).hexdigest()[:24]


def render_card(card):
    return '\n'.join([card['title'], 'Use when: ' + card['use_when'],
                      *['- ' + x for x in card['steps']],
                      *['Caveat: ' + x for x in card['caveats']]])


def build_index(path, cards):
    db = sqlite3.connect(path)
    with db:
        db.execute('DROP TABLE IF EXISTS cards')
        db.execute('DROP TABLE IF EXISTS search')
        db.execute('CREATE TABLE cards(id TEXT PRIMARY KEY, body TEXT NOT NULL)')
        db.execute("CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED,title,summary,tags,body,tokenize='porter unicode61')")
        for card in cards:
            db.execute('INSERT INTO cards VALUES(?,?)', (card['id'], json.dumps(card, ensure_ascii=False)))
            db.execute('INSERT INTO search VALUES(?,?,?,?,?)', (card['id'], card['title'],
                       card['summary'], ' '.join(card['tags']), render_card(card)))
    db.close()


def search_cards(path, query, token_budget=3000, max_cards=6, domain=None, count_tokens=None):
    # UTF-8 bytes are a conservative token ceiling, avoiding a runtime tokenizer dependency.
    counter = count_tokens or (lambda value: len(value.encode('utf-8')))
    unit = 'tokens' if count_tokens else 'utf8-byte-token-upper-bound'
    terms = re.findall(r'\w+', query.lower(), flags=re.UNICODE)
    stop = {'the','a','an','to','of','for','and','with','how','i','we','my','our','is','in','what','should'}
    terms = list(dict.fromkeys(t for t in terms if t not in stop))[:40]
    if not terms or token_budget <= 0 or max_cards <= 0:
        return {'cards': [], 'context': '', 'budget_units_used': 0, 'budget_unit': unit}
    db = sqlite3.connect(path)
    hits = db.execute('SELECT cards.body FROM search JOIN cards ON cards.id=search.id WHERE search MATCH ? ORDER BY bm25(search,0,5,3,4,1) LIMIT 100',
                      (' OR '.join('"' + x + '"' for x in terms),)).fetchall()
    db.close()
    selected, texts, used = [], [], 0
    for (body,) in hits:
        card = json.loads(body)
        if domain and card['domain'] != domain:
            continue
        text = '[' + card['id'] + '] ' + render_card(card)
        total = counter('\n\n'.join(texts + [text]))
        if total > token_budget:
            continue
        selected.append(card); texts.append(text); used = total
        if len(selected) >= max_cards:
            break
    return {'cards': selected, 'context': '\n\n'.join(texts), 'budget_units_used': used,
            'budget_unit': unit}
