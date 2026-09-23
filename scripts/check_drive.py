"""Read-only credential check. Never prints tokens, keys, or response bodies on failure."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime'))

def main():
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    credentials = service_account.Credentials.from_service_account_file(
        ROOT / 'secrets' / 'drive-reader.json',
        scopes=['https://www.googleapis.com/auth/drive.readonly'])
    if credentials.service_account_email != 'ecomos-drive-reader@ecomos-509406.iam.gserviceaccount.com':
        raise ValueError('Unexpected service account')
    folder = '1wo7oScCia-h3XiwW_Ogjcvkr60_S11Ax'
    session = AuthorizedSession(credentials)
    response = session.get(f'https://www.googleapis.com/drive/v3/files/{folder}',
                           params={'fields': 'id,name,mimeType', 'supportsAllDrives': 'true'}, timeout=45)
    if response.status_code != 200:
        print(json.dumps({'root_access': False, 'http_status': response.status_code}))
        return 1
    result = response.json()
    count, folders, page = 0, 0, None
    while True:
        params = {'q': f"'{folder}' in parents and trashed=false", 'pageSize': 1000,
                  'fields': 'nextPageToken,files(id,mimeType)', 'supportsAllDrives': 'true',
                  'includeItemsFromAllDrives': 'true'}
        if page:
            params['pageToken'] = page
        response = session.get('https://www.googleapis.com/drive/v3/files', params=params, timeout=45)
        if response.status_code != 200:
            print(json.dumps({'root_access': True, 'listing_http_status': response.status_code}))
            return 1
        listing = response.json()
        count += len(listing.get('files', []))
        folders += sum(f['mimeType'] == 'application/vnd.google-apps.folder' for f in listing.get('files', []))
        page = listing.get('nextPageToken')
        if not page:
            break
    print(json.dumps({'root_access': True, 'root_is_folder': result['mimeType'] == 'application/vnd.google-apps.folder',
                      'immediate_items': count, 'immediate_folders': folders, 'mode': 'read_only'}))
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'check_failed': True, 'error_type': type(error).__name__}))
        sys.exit(1)
