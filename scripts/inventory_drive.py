"""Read-only recursive inventory. Persists metadata locally, never credentials."""
import json
import sys
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime'))
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

def main():
    credentials = service_account.Credentials.from_service_account_file(
        ROOT / 'secrets/drive-reader.json', scopes=['https://www.googleapis.com/auth/drive.readonly'])
    session = AuthorizedSession(credentials)
    root_id = '1wo7oScCia-h3XiwW_Ogjcvkr60_S11Ax'
    queue, seen, records, failures = deque([(root_id, '')]), set(), [], []
    while queue:
        folder, path = queue.popleft()
        if folder in seen:
            continue
        seen.add(folder)
        page = None
        try:
            while True:
                params = {'q': f"'{folder}' in parents and trashed=false", 'pageSize': 1000,
                          'fields': 'nextPageToken,files(id,name,mimeType,size,modifiedTime,md5Checksum,webViewLink,shortcutDetails)',
                          'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}
                if page:
                    params['pageToken'] = page
                response = session.get('https://www.googleapis.com/drive/v3/files', params=params, timeout=45)
                if response.status_code != 200:
                    raise RuntimeError('HTTP_' + str(response.status_code))
                payload = response.json()
                for item in payload.get('files', []):
                    item['parent_id'], item['folder_path'] = folder, path
                    records.append(item)
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        queue.append((item['id'], path + '/' + item['name']))
                page = payload.get('nextPageToken')
                if not page:
                    break
        except Exception as error:
            failures.append({'folder_id': folder, 'error_type': type(error).__name__})
        print(json.dumps({'folders_scanned': len(seen), 'items_discovered': len(records)}), flush=True)
    files = [r for r in records if r['mimeType'] != 'application/vnd.google-apps.folder']
    summary = {'created_at': datetime.now(timezone.utc).isoformat(), 'root_id': root_id,
               'folders_excluding_root': len(seen)-1, 'files': len(files),
               'mime_counts': dict(Counter(r['mimeType'] for r in files)),
               'bytes': sum(int(r.get('size',0)) for r in files), 'failed_folders': len(failures),
               'note': 'Point-in-time crawl; change-feed reconciliation not yet implemented.'}
    target = ROOT / 'data/inventory'
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (target / (stamp + '.json')).write_text(json.dumps({'summary':summary,'records':records,'failures':failures},indent=2),encoding='utf-8')
    (target / 'latest.json').write_text(json.dumps({'summary':summary,'records':records,'failures':failures},indent=2),encoding='utf-8')
    print(json.dumps(summary), flush=True)
    return bool(failures)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'failed': True, 'error_type': type(error).__name__}))
        sys.exit(1)
