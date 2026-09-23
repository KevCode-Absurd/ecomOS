"""Snapshot every inventoried file locally and parse supported source documents."""
import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.runtime'), str(ROOT)]
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from intelligence.parsing import parse_document

local = threading.local()

def session():
    if not hasattr(local, 'session'):
        credentials = service_account.Credentials.from_service_account_file(
            ROOT / 'secrets/drive-reader.json', scopes=['https://www.googleapis.com/auth/drive.readonly'])
        local.session = AuthorizedSession(credentials)
    return local.session

def process(item):
    result = {'id': item['id'], 'name': item['name'], 'folder_path': item['folder_path'],
              'modifiedTime': item.get('modifiedTime'), 'status': 'failed'}
    try:
        target = ROOT / 'data/snapshots' / item['id']
        target.mkdir(parents=True, exist_ok=True)
        prior = target / 'result.json'
        if prior.exists():
            cached = json.loads(prior.read_text(encoding='utf-8'))
            if cached.get('modifiedTime') == item.get('modifiedTime') and cached.get('status') in {'parsed','supporting_file'}:
                raw_path = target / cached['sha256']
                if raw_path.exists() and hashlib.sha256(raw_path.read_bytes()).hexdigest() == cached['sha256']:
                    return cached
        response = session().get('https://www.googleapis.com/drive/v3/files/' + item['id'],
                                 params={'alt':'media','supportsAllDrives':'true'},timeout=90)
        if response.status_code != 200:
            result['http_status'] = response.status_code
            return result
        raw = response.content
        if item.get('md5Checksum') and hashlib.md5(raw).hexdigest() != item['md5Checksum']:
            result['error_type'] = 'ChecksumMismatch'
            return result
        sha = hashlib.sha256(raw).hexdigest()
        (target / sha).write_bytes(raw)
        result.update(sha256=sha,bytes=len(raw))
        if item['name'].lower().endswith('.docx'):
            blocks, media = parse_document(raw,item['name'])
            result.update(status='parsed' if blocks else 'empty', blocks=len(blocks),
                          characters=sum(len(b['text']) for b in blocks),
                          words=sum(len(b['text'].split()) for b in blocks),
                          tables=sum('rows' in b for b in blocks),media_items=len(media))
            (target / (sha + '.parsed.json')).write_text(json.dumps({'blocks':blocks,'media':media},ensure_ascii=False),encoding='utf-8')
        else:
            result['status'] = 'supporting_file'
        prior.write_text(json.dumps(result,indent=2),encoding='utf-8')
    except Exception as error:
        result['error_type'] = type(error).__name__
    return result

def main():
    inventory = json.loads((ROOT / 'data/inventory/latest.json').read_text(encoding='utf-8'))
    items = [r for r in inventory['records'] if r['mimeType'] != 'application/vnd.google-apps.folder']
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(process,item) for item in items]
        for future in as_completed(futures):
            results.append(future.result())
            if len(results)%25 == 0:
                print(json.dumps({'completed':len(results),'total':len(items)}),flush=True)
    parsed = [r for r in results if r['status']=='parsed']
    summary = {'files':len(results),'parsed_docx':len(parsed),
               'supporting_files':sum(r['status']=='supporting_file' for r in results),
               'failed_or_empty':sum(r['status'] not in {'parsed','supporting_file'} for r in results),
               'characters':sum(r['characters'] for r in parsed),
               'words':sum(r['words'] for r in parsed),'tables':sum(r['tables'] for r in parsed),
               'embedded_media_items':sum(r['media_items'] for r in parsed),
               'limitations':['Basic DOCX body extraction; images inventoried but not interpreted.',
                              'Source origin and claim quality not yet validated.','Token count not yet measured.']}
    report = ROOT / 'data/snapshot-report.json'
    report.write_text(json.dumps({'summary':summary,'results':results},indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)
    return bool(summary['failed_or_empty'])

if __name__=='__main__':
    sys.exit(main())
