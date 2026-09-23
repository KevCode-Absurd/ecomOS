"""Resumable text-to-card ingestion: CRO first, then numbered folders. No visual work."""
import argparse
import collections
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from calibration_client import ROOT, run_call
from intelligence.library import validate_cards, card_id, build_index, render_card

DEST = ROOT / 'data/library-v3'
STAGE = 'library-v3'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def sections(blocks, maximum=55000):
    texts = [re.sub(r'[ \t]+', ' ', b['text']).strip() for b in blocks if b['text'].strip()]
    # Remove opening YAML frontmatter only when closed. Keep the complete body.
    if texts and texts[0] == '---':
        try: texts = texts[texts.index('---', 1) + 1:]
        except ValueError: pass
    parts = []
    for text in texts:
        if parts and text == parts[-1]: continue
        while len(text) > maximum:
            cut = text.rfind('. ', 0, maximum)
            cut = cut + 1 if cut > maximum // 2 else maximum
            parts.append(text[:cut]); text = text[cut:]
        parts.append(text)
    chunk = ''
    result = []
    for text in parts:
        if chunk and len(chunk) + len(text) + 2 > maximum:
            result.append(chunk)
            chunk = chunk[-1200:] + '\n\n' + text
        else: chunk += ('\n\n' if chunk else '') + text
    if chunk: result.append(chunk)
    return result


def prepare():
    catalog = read(ROOT / 'data/source-catalog.json')['sources']
    prior = collections.defaultdict(list)
    for card in read(ROOT / 'data/cro-folder-v1/revision-index.json')['cards']:
        if card['source_support_verdict'] in ('revise', 'unsupported'): continue
        evidence = card.get('evidence', [])
        if evidence:
            u = card['unit']
            prior[evidence[0]['source_id']].append({'title': u['title'], 'claim': u['claim']['text'],
                                                   'action': u.get('action'), 'unknowns': u.get('unknowns')})
    jobs = []
    for source in sorted(catalog, key=lambda s: (0 if '/09-' in s['folder'] else 1, s['folder'], s['name'])):
        parsed = read(ROOT / 'data/snapshots' / source['source_id'] / (source['source_sha256'] + '.parsed.json'))
        chunks = sections(parsed['blocks'])
        domain = source['folder'].strip('/').split('-', 2)[-1]
        notes = prior[source['source_id']]
        for i, text in enumerate(chunks):
            # Reuse notes where their distinctive words occur in this source section.
            lower = text.lower()
            relevant = [n for n in notes if sum(t in lower for t in re.findall(r'\w{5,}', n['title'].lower())) >= 3]
            job = {'source_id': source['source_id'], 'source_sha256': source['source_sha256'],
                   'source_name': source['name'], 'folder': source['folder'], 'domain': domain,
                   'section': i, 'section_count': len(chunks), 'text': text, 'prior_notes': relevant[:70]}
            job['id'] = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()[:24]
            jobs.append(job)
    write(DEST / 'manifest.json', {'jobs': jobs})
    return jobs


def export(jobs):
    cards, seen, counts = [], set(), collections.Counter()
    for job in jobs:
        path = DEST / 'results' / (job['id'] + '.json')
        if not path.exists(): continue
        for card in read(path)['cards']:
            fingerprint = json.dumps({k:card[k] for k in ('title','summary','use_when','steps','caveats','tags')}, sort_keys=True)
            if fingerprint in seen: continue
            seen.add(fingerprint); cards.append(card); counts[job['folder']] += 1
    write(DEST / 'cards.json', {'cards': cards})
    build_index(DEST / 'search.sqlite', cards)
    markdown = DEST / 'markdown'; markdown.mkdir(exist_ok=True)
    for folder in counts:
        (markdown / (folder.strip('/') + '.md')).write_text('\n\n---\n\n'.join(
            '## ' + render_card(c) + '\n\nTags: ' + ', '.join(c['tags']) + '\nSource: ' + c['source_name']
            for c in cards if c['folder'] == folder), encoding='utf-8')
    folders = []
    for folder in dict.fromkeys(j['folder'] for j in jobs):
        group = [j for j in jobs if j['folder'] == folder]
        complete = sum((DEST / 'results' / (j['id'] + '.json')).exists() for j in group)
        folders.append({'folder': folder, 'sections': len(group), 'completed': complete, 'cards': counts[folder]})
    write(DEST / 'progress.json', {'folders': folders, 'cards': len(cards)})
    return folders


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--folder', help='Folder prefix, e.g. 09 or 01; omitted processes all in order')
    parser.add_argument('--workers', type=int, choices=range(1, 9), default=4)
    parser.add_argument('--max-jobs', type=int)
    args = parser.parse_args()
    DEST.mkdir(parents=True, exist_ok=True)
    jobs = prepare()
    if not args.execute:
        print(json.dumps(export(jobs))); return
    auth = read(DEST / 'authorization.json')
    if auth.get('overall_ceiling_usd') != 200 or auth.get('text_only') is not True:
        raise ValueError('Missing current authorization')
    prompt = (ROOT / 'prompts/cards-v3.md').read_text(encoding='utf-8')
    pending = [j for j in jobs if not (DEST / 'results' / (j['id'] + '.json')).exists()
               and (not args.folder or j['folder'].startswith('/' + args.folder))]
    if args.max_jobs: pending = pending[:args.max_jobs]
    def process(job):
        result = run_call(STAGE, 'deepseek', 'none', prompt, job, limit=16384, stage_limit=200)
        if result['finish_reason'] != 'stop': raise ValueError('Incomplete response; saved for inspection')
        cards = validate_cards(result['output'])
        if not cards and len(job['text']) > 10000: raise ValueError('Unexpected empty extraction')
        for card in cards:
            card.update(id=card_id(job['source_id'], card), source_id=job['source_id'],
                        source_sha256=job['source_sha256'], source_name=job['source_name'],
                        folder=job['folder'], domain=job['domain'], section=job['section'])
        write(DEST / 'results' / (job['id'] + '.json'), {'cards': cards, 'request_id': result['request_id'], 'ecommerce_scope_version': 1})
        print(json.dumps({'folder': job['folder'], 'source': job['source_name'], 'section': job['section'],
                          'cards': len(cards), 'cost_usd': result['booked_cost_usd']}), flush=True)
    for folder in dict.fromkeys(j['folder'] for j in pending):
        group = [j for j in pending if j['folder'] == folder]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for start in range(0, len(group), args.workers):
                futures = [pool.submit(process, j) for j in group[start:start + args.workers]]
                errors = []
                for f in futures:
                    try: f.result()
                    except Exception as error: errors.append(type(error).__name__)
                export(jobs)
                if errors: raise ValueError('Batch stopped; inspect saved results: ' + ','.join(errors))
        progress = export(jobs)
        status = next(x for x in progress if x['folder'] == folder)
        print(json.dumps({'folder_status': status}), flush=True)
        if status['completed'] == status['sections']:
            from library_embeddings import main as refresh_embeddings
            refresh_embeddings()


if __name__ == '__main__':
    main()
