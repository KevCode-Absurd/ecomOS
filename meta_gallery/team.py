"""Team mode for the gallery server: invite code login, image caps and a usage log.

Off unless TEAM_MODE=1. Then every page and API call needs a signed session cookie,
which a person gets by entering their invite code. API keys stay in the server's
environment (ANTHROPIC_API_KEY, OPENAI_API_KEY); nothing here ever sends them out.

Settings (environment variables, set as secrets on the host):
  TEAM_MODE=1
  TEAM_SECRET          random string that signs session cookies (32+ characters)
  TEAM_CODES           name:sha256,name:sha256  (hashes of invite codes, never the codes)
  TEAM_OWNERS          names allowed to change shared settings (comma separated)
  TEAM_DAILY_IMAGES    images per person per day (default 50)
  TEAM_MONTHLY_IMAGES  images for the whole team per calendar month (default 1500)
  TEAM_DAILY_ASKS      text AI calls per person per day (default 200)
  TEAM_STATE           folder for the usage file and log (default data/meta-gallery/team)

Make a code:  python -m meta_gallery.team new NAME
"""
import datetime as dt
import hashlib
import hmac
import json
import os
import secrets
import sys
import threading
import time
from pathlib import Path

from .snapshot import DATA

COOKIE = 'eg_session'
SESSION_DAYS = 30
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
_lock = threading.Lock()
_fails = {}


def enabled():
    return os.environ.get('TEAM_MODE') == '1'


def _int(name, default):
    try:
        return max(0, int(os.environ.get(name, default)))
    except ValueError:
        return default


def limits():
    return {'daily_images': _int('TEAM_DAILY_IMAGES', 50), 'monthly_images': _int('TEAM_MONTHLY_IMAGES', 1500),
            'daily_asks': _int('TEAM_DAILY_ASKS', 200)}


def state_dir():
    d = Path(os.environ.get('TEAM_STATE') or DATA / 'team')
    d.mkdir(parents=True, exist_ok=True)
    return d


def check_config():
    """Refuse to start team mode with a weak or missing setup."""
    problems = []
    if len(os.environ.get('TEAM_SECRET', '')) < 32:
        problems.append('TEAM_SECRET must be at least 32 characters.')
    if not codes():
        problems.append('TEAM_CODES has no valid name:hash pairs.')
    return problems


def hash_code(code):
    return hashlib.sha256(code.strip().encode('utf-8')).hexdigest()


def codes():
    out = {}
    for part in os.environ.get('TEAM_CODES', '').split(','):
        name, _, h = part.strip().partition(':')
        if name and len(h) == 64:
            out[h.lower()] = name.strip()[:40]
    return out


def owners():
    return {x.strip() for x in os.environ.get('TEAM_OWNERS', '').split(',') if x.strip()}


def _sign(payload):
    return hmac.new(os.environ['TEAM_SECRET'].encode(), payload.encode(), hashlib.sha256).hexdigest()


def login(code, ip):
    """Returns (cookie value, name) or raises ValueError. Slows guessing: 5 misses a minute per address."""
    now = time.time()
    with _lock:
        recent = [t for t in _fails.get(ip, []) if now - t < 60]
        _fails[ip] = recent
        if len(recent) >= 5:
            raise ValueError('Too many tries. Wait a minute.')
    name = codes().get(hash_code(code or '')) if isinstance(code, str) and 8 <= len(code) <= 200 else None
    if not name:
        with _lock:
            _fails.setdefault(ip, []).append(now)
        raise ValueError('That code does not work.')
    exp = int(now) + SESSION_DAYS * 86400
    payload = f'{name}|{exp}'
    return f'{payload}|{_sign(payload)}', name


def who(cookie_header):
    """The signed-in name from the Cookie header, or None. A removed code ends its sessions."""
    if not cookie_header:
        return None
    for part in cookie_header.split(';'):
        k, _, v = part.strip().partition('=')
        if k != COOKIE:
            continue
        try:
            name, exp, sig = v.split('|')
        except ValueError:
            return None
        if not hmac.compare_digest(sig, _sign(f'{name}|{exp}')) or int(exp) < time.time():
            return None
        return name if name in codes().values() else None
    return None


def cookie(value, secure=True, clear=False):
    attrs = ['Path=/', 'HttpOnly', 'SameSite=Lax']
    if secure:
        attrs.append('Secure')
    attrs.append('Max-Age=0' if clear else f'Max-Age={SESSION_DAYS * 86400}')
    return f"{COOKIE}={'' if clear else value}; " + '; '.join(attrs)


def _today():
    return dt.datetime.now(IST).strftime('%Y-%m-%d')


def _load():
    p = state_dir() / 'usage.json'
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {'days': {}, 'months': {}}


def _save(u):
    p = state_dir() / 'usage.json'
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(u, indent=1), encoding='utf-8')
    tmp.replace(p)


def usage(name):
    lim = limits()
    with _lock:
        u = _load()
    day, month = _today(), _today()[:7]
    mine = u['days'].get(day, {}).get(name, {})
    return {'name': name, 'owner': name in owners(), 'images_today': mine.get('images', 0), 'asks_today': mine.get('asks', 0),
            'team_images_month': u['months'].get(month, 0), **lim}


def reserve(name, images=0, asks=0):
    """Take images/asks from the caps before a paid call. Raises ValueError when a cap would be passed."""
    lim = limits()
    day, month = _today(), _today()[:7]
    with _lock:
        u = _load()
        mine = u['days'].setdefault(day, {}).setdefault(name, {'images': 0, 'asks': 0})
        if images and mine['images'] + images > lim['daily_images']:
            left = max(0, lim['daily_images'] - mine['images'])
            raise ValueError(f'Daily limit: {left} of {lim["daily_images"]} images left for you today.')
        if images and u['months'].get(month, 0) + images > lim['monthly_images']:
            raise ValueError('The team has used this month\'s image budget. Ask the owner to raise it.')
        if asks and mine['asks'] + asks > lim['daily_asks']:
            raise ValueError(f'Daily limit of {lim["daily_asks"]} AI text calls reached.')
        mine['images'] += images
        mine['asks'] += asks
        u['months'][month] = u['months'].get(month, 0) + images
        u['days'] = {k: v for k, v in u['days'].items() if k >= (dt.date.fromisoformat(day) - dt.timedelta(days=60)).isoformat()}
        _save(u)


def refund(name, images=0, asks=0):
    """Give back what a failed call did not use."""
    day, month = _today(), _today()[:7]
    with _lock:
        u = _load()
        mine = u['days'].setdefault(day, {}).setdefault(name, {'images': 0, 'asks': 0})
        mine['images'] = max(0, mine['images'] - images)
        mine['asks'] = max(0, mine['asks'] - asks)
        u['months'][month] = max(0, u['months'].get(month, 0) - images)
        _save(u)


def log(name, route, images=0, asks=0, ok=True, note=''):
    line = json.dumps({'at': dt.datetime.now(IST).isoformat(timespec='seconds'), 'who': name, 'route': route,
                       'images': images, 'asks': asks, 'ok': ok, 'note': note[:200]})
    with _lock:
        with open(state_dir() / 'usage_log.jsonl', 'a', encoding='utf-8') as f:
            f.write(line + '\n')


LOGIN_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Sign in</title>
<style>
:root{--bg:#f6f4ef;--card:#fff;--ink:#1d1b18;--muted:#6b665d;--line:#e2ddd3;--acc:#8a5a14;--bad:#b3261e}
@media (prefers-color-scheme: dark){:root{--bg:#171614;--card:#211f1c;--ink:#f1ede6;--muted:#a59f94;--line:#35322d;--acc:#d9a441;--bad:#f2b8b5}}
body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif}
form{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:28px;width:min(360px,calc(100vw - 32px));box-sizing:border-box}
h1{font-size:20px;margin:0 0 6px}p{margin:0 0 18px;color:var(--muted);font-size:14px}
input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:transparent;color:var(--ink);font-size:16px}
button{margin-top:12px;width:100%;padding:10px;border:0;border-radius:8px;background:var(--acc);color:#fff;font-weight:600;font-size:15px;cursor:pointer}
#err{color:var(--bad);font-size:14px;min-height:20px;margin-top:10px}
</style></head><body>
<form id="f"><h1>Ad dashboard</h1><p>Enter the invite code you were given.</p>
<input id="c" type="password" autocomplete="current-password" placeholder="Invite code" required>
<button>Sign in</button><div id="err"></div></form>
<script>
document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const r = await fetch('/team/login', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({code: document.getElementById('c').value})});
  const j = await r.json().catch(() => ({}));
  if (r.ok) location.href = '/'; else document.getElementById('err').textContent = j.error || 'Sign in failed.';
};
</script></body></html>"""

BADGE = """<div id="teamBadge" style="position:fixed;right:12px;bottom:12px;z-index:9999;background:#1d1b18;color:#f1ede6;border-radius:999px;padding:6px 12px;font:12px/1.4 system-ui,sans-serif;opacity:.9"></div>
<script>
(async () => {
  const el = document.getElementById('teamBadge');
  const load = async () => {
    const r = await fetch('/team/me'); if (!r.ok) return;
    const m = await r.json();
    el.textContent = '';
    el.append(`${m.name}: ${m.images_today} of ${m.daily_images} images today · `);
    const a = document.createElement('a'); a.href = '#'; a.textContent = 'Sign out'; a.style.color = 'inherit';
    a.onclick = async (e) => { e.preventDefault(); await fetch('/team/logout', {method: 'POST'}); location.href = '/'; };
    el.append(a);
  };
  load(); setInterval(load, 60000);
})();
</script>"""


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) == 2 and args[0] == 'new':
        name = ''.join(ch for ch in args[1] if ch.isalnum() or ch in '-_')[:40]
        if not name:
            print('Use: python -m meta_gallery.team new NAME')
            return 1
        code = secrets.token_urlsafe(12)
        print(f'Invite code for {name} (send it to them privately; it is not stored anywhere):')
        print(f'  {code}')
        print('Add this to TEAM_CODES on the host (comma separated with the others):')
        print(f'  {name}:{hash_code(code)}')
        return 0
    if args == ['secret']:
        print(secrets.token_urlsafe(48))
        return 0
    print('Use: python -m meta_gallery.team new NAME   |   python -m meta_gallery.team secret')
    return 1


if __name__ == '__main__':
    sys.exit(main())
