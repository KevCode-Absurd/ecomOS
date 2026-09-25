"""Print one source document's parsed text and its cards as markdown, for playbook distillation.

Usage: python3 scripts/export_source.py SOURCE_ID [--cards-only] [--text-only]
Read-only. No API calls.
"""
import json, sys, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load_cards(source_id):
    cards = json.load(open(ROOT/'data/library-v3/cards.json'))['cards']
    return [c for c in cards if c['source_id'] == source_id]

def load_text(source_id):
    d = ROOT/'data/snapshots'/source_id
    if not d.is_dir():
        return None, None
    res = json.load(open(d/'result.json'))
    parsed = d/(res['sha256']+'.parsed.json')
    if not parsed.exists():
        return res, None
    j = json.load(open(parsed))
    blocks = j.get('blocks', j if isinstance(j, list) else [])
    out = []
    for b in blocks:
        if isinstance(b, dict):
            t = b.get('text') or b.get('content') or ''
            if b.get('type') == 'table' and isinstance(b.get('rows'), list):
                t = '\n'.join(' | '.join(str(x) for x in r) for r in b['rows'])
        else:
            t = str(b)
        if t.strip():
            out.append(t.strip())
    return res, '\n\n'.join(out)

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    sid = args[0]
    res, text = load_text(sid)
    cards = load_cards(sid)
    name = res['name'] if res else (cards[0]['source_name'] if cards else sid)
    folder = res.get('folder_path') if res else (cards[0]['folder'] if cards else '')
    ov = json.load(open(ROOT/'data/library-v3/folder-overrides.json'))['sources'] if (ROOT/'data/library-v3/folder-overrides.json').exists() else {}
    if sid in ov:
        folder = ov[sid]['to'] + ' (moved from ' + ov[sid]['from'] + ')'
    print(f'# {name}\n\nsource_id: {sid}\nfolder: {folder}\nmodified: {res.get("modifiedTime") if res else "unknown"}\ncards: {len(cards)}\nwords_in_text: {len(text.split()) if text else 0}\n')
    if '--cards-only' not in args:
        print('## Source text\n')
        print(text if text else '(no parsed text found)')
        print()
    if '--text-only' not in args:
        print(f'## Cards ({len(cards)})\n')
        for c in cards:
            print(f'### [{c["id"]}] {c["title"]}')
            print(f'Summary: {c["summary"]}')
            print(f'Use when: {c["use_when"]}')
            for s in c['steps']: print(f'- {s}')
            for v in c['caveats']: print(f'Caveat: {v}')
            print(f'Tags: {", ".join(c["tags"])}\n')

if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
