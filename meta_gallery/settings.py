"""Local UI settings: targets, exclusion presets and report branding.

Stored in data/meta-gallery/settings.json (git-ignored). This is the only
thing the local server ever writes besides cached images. It never touches Meta.
"""
import json
import re
import threading
from pathlib import Path

from .snapshot import DATA

PATH = DATA / 'settings.json'
DEFAULTS = {'targets': {'roas': None, 'cpa': None}, 'presets': [], 'branding': {'agency': '', 'client': '', 'note': ''}}
MAX_PRESETS = 30
ID = re.compile(r'^[0-9]{5,25}$')
_lock = threading.Lock()


def _text(v, limit):
    v = '' if v is None else str(v)
    v = re.sub(r'[\x00-\x1f\x7f]', ' ', v).strip()
    return v[:limit]


def _pos(v):
    if v in (None, ''):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f'Not a number: {v!r}')
    if not 0 < f < 1e9:
        raise ValueError('Targets must be above 0.')
    return f


def validate(data):
    """Return a clean settings dict or raise ValueError. Unknown keys are dropped."""
    if not isinstance(data, dict):
        raise ValueError('Settings must be a JSON object.')
    out = json.loads(json.dumps(DEFAULTS))
    t = data.get('targets') or {}
    out['targets'] = {'roas': _pos(t.get('roas')), 'cpa': _pos(t.get('cpa'))}
    presets = []
    for p in (data.get('presets') or [])[:MAX_PRESETS]:
        name = _text(p.get('name'), 60)
        if not name:
            continue
        kws = [_text(k, 60).lower() for k in (p.get('keywords') or [])[:20]]
        ids = [str(i) for i in (p.get('campaign_ids') or [])[:200] if ID.match(str(i))]
        presets.append({'name': name, 'keywords': [k for k in kws if k], 'campaign_ids': ids})
    out['presets'] = presets
    b = data.get('branding') or {}
    out['branding'] = {'agency': _text(b.get('agency'), 80), 'client': _text(b.get('client'), 80),
                       'note': _text(b.get('note'), 400)}
    return out


def load(path=None):
    path = Path(path or PATH)
    try:
        return validate(json.loads(path.read_text(encoding='utf-8')))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return json.loads(json.dumps(DEFAULTS))


def save(data, path=None):
    path = Path(path or PATH)
    clean = validate(data)
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        path = Path(path).resolve()  # a link to the host's persistent disk is followed, not replaced
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(clean, ensure_ascii=False, indent=1), encoding='utf-8')
        tmp.replace(path)
    return clean


# ---------- team notes on ads ----------
NOTES_PATH = DATA / 'notes.json'
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
MAX_NOTES_ADS = 2000
MAX_NOTES_PER_AD = 200


def validate_notes(data):
    """Return clean notes {ad_id: [{text, by, date}]} or raise ValueError."""
    if not isinstance(data, dict):
        raise ValueError('Notes must be a JSON object.')
    if len(data) > MAX_NOTES_ADS:
        raise ValueError('Too many ads with notes.')
    out = {}
    for ad_id, items in data.items():
        if not ID.match(str(ad_id)) or not isinstance(items, list):
            raise ValueError('Bad notes entry.')
        clean = []
        for n in items[:MAX_NOTES_PER_AD]:
            if not isinstance(n, dict):
                raise ValueError('Bad note.')
            text = _text(n.get('text'), 500)
            date = str(n.get('date') or '')
            if not text or not DATE.match(date):
                raise ValueError('Each note needs text and a date.')
            clean.append({'text': text, 'by': _text(n.get('by'), 40), 'date': date})
        if clean:
            out[str(ad_id)] = clean
    return out


def load_notes(path=None):
    path = Path(path or NOTES_PATH)
    try:
        return validate_notes(json.loads(path.read_text(encoding='utf-8')))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return {}


def save_notes(data, path=None):
    path = Path(path or NOTES_PATH)
    clean = validate_notes(data)
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        path = Path(path).resolve()  # a link to the host's persistent disk is followed, not replaced
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(clean, ensure_ascii=False, indent=1), encoding='utf-8')
        tmp.replace(path)
    return clean
