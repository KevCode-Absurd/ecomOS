"""Creative lab: explain why an image ad worked, then make new image ads like it.

Runs only on the local server, so API keys stay in .env on this machine and never
reach the browser. Nothing here touches the Meta ad account.

- Breakdown: Claude (ANTHROPIC_API_KEY) reads the ad image, copy and numbers and
  returns a JSON breakdown. Falls back to OpenAI (OPENAI_API_KEY) if there is no
  Anthropic key.
- Variants: OpenAI image edits (OPENAI_API_KEY) with the ad image as the reference.

Models can be changed in .env: AI_TEXT_MODEL, AI_OPENAI_TEXT_MODEL, AI_IMAGE_MODEL.
Results are saved under data/meta-gallery/ (breakdowns.json, variants/<ad id>/).
"""
import base64
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .graph_client import load_env
from .snapshot import DATA, ROOT

BREAKDOWNS = DATA / 'breakdowns.json'
BRAND = DATA / 'brand.json'
VARIANTS = DATA / 'variants'
DEFAULTS = {
    'AI_TEXT_MODEL': 'claude-sonnet-5',
    'AI_OPENAI_TEXT_MODEL': 'gpt-6-luna',
    'AI_IMAGE_MODEL': 'gpt-image-2.5-sunburst',
    'AI_IMAGE_FALLBACK': 'gpt-image-2',
}
SIZES = {'square': '1024x1024', 'portrait': '1024x1280', 'story': '1024x1824'}
QUALITIES = ('low', 'medium', 'high')
SAFE_ID = re.compile(r'^[0-9]{5,25}$')
SAFE_FILE = re.compile(r'^[A-Za-z0-9_-]{1,80}\.(png|jpg|jpeg|webp)$')
_lock = threading.Lock()


class AIError(Exception):
    """A message that is safe to show in the page (never contains a key)."""


def settings(env_path=None):
    # .env on this machine first, then the host's environment (secrets on a server like Render).
    env = {k: os.environ[k] for k in list(DEFAULTS) + ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY'] if os.environ.get(k)}
    env.update(load_env(Path(env_path) if env_path else ROOT / '.env'))
    # Pasted secrets often carry a trailing newline or space. Strip them so they are valid header values.
    env = {k: (v or '').strip() for k, v in env.items()}
    cfg = {k: env.get(k) or v for k, v in DEFAULTS.items()}
    cfg['anthropic_key'] = env.get('ANTHROPIC_API_KEY') or ''
    cfg['openai_key'] = env.get('OPENAI_API_KEY') or ''
    return cfg


def status(env_path=None):
    """What the page may offer. Never includes keys."""
    cfg = settings(env_path)
    text = 'claude' if cfg['anthropic_key'] else 'openai' if cfg['openai_key'] else None
    return {'breakdown': text is not None, 'breakdown_provider': text,
            'breakdown_model': cfg['AI_TEXT_MODEL'] if text == 'claude' else cfg['AI_OPENAI_TEXT_MODEL'] if text else None,
            'variants': bool(cfg['openai_key']), 'image_model': cfg['AI_IMAGE_MODEL'],
            'sizes': list(SIZES), 'qualities': list(QUALITIES)}


def _scrub(text, cfg):
    text = str(text)
    for k in (cfg.get('anthropic_key'), cfg.get('openai_key')):
        if k:
            for form in (k, repr(k)[1:-1], k.strip()):
                if form:
                    text = text.replace(form, '[key]')
    text = re.sub(r'sk-[A-Za-z0-9_\-]{8,}', '[key]', text)
    # Anything else that looks like a long secret token (40+ key-like characters) is hidden too.
    return re.sub(r'[A-Za-z0-9_\-]{40,}', '[hidden]', text)


def scrub(text):
    """Remove any API key or key-like token from a message before it leaves the server."""
    try:
        cfg = settings()
    except Exception:
        cfg = {}
    return _scrub(text, cfg)


def _post(url, headers, body, cfg, timeout=240):
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8', 'replace')
        try:
            msg = json.loads(raw).get('error', {})
            msg = msg.get('message') if isinstance(msg, dict) else str(msg)
        except ValueError:
            msg = raw[:300]
        raise AIError(_scrub(f'{e.code}: {msg}', cfg)) from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise AIError(_scrub(f'Could not reach the API: {getattr(e, "reason", e)}', cfg)) from None
    except Exception:
        # Never pass the raw error on: some (like a bad header) print the key itself.
        raise AIError('The AI request failed before it was sent. Check the API key setting on the server.') from None


def _json_from(text):
    text = text.strip()
    fence = re.search(r'```(?:json)?\s*(.*?)```', text, re.S)
    if fence:
        text = fence.group(1)
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end <= start:
        raise AIError('The model did not return a breakdown. Try again.')
    return json.loads(text[start:end + 1])


# ---------- breakdown ----------
BREAKDOWN_SHAPE = '''{
  "verdict": "worked" | "mixed" | "did_not_work",
  "summary": "one sentence, plain words",
  "why": [{"point": "short reason", "evidence": "what in the image, copy or numbers shows it"}],
  "structure": {"hook": "", "layout": "", "product": "", "text_on_image": "", "offer": "", "proof": "", "cta": "", "look": ""},
  "keep": ["element to keep in new versions"],
  "test_next": ["one idea per line for a new version"],
  "watch_out": ["risk or weak spot"]
}'''


def breakdown_prompt(ad):
    """Text prompt shared by the local server and the shared page (same wording)."""
    return (
        "You are a senior performance creative strategist for Meta ads. Study this image ad from Gehna, "
        "an Indian fine jewellery brand, and explain why it performed the way it did.\n\n"
        f"Ad data (JSON):\n{json.dumps(ad, ensure_ascii=False)}\n\n"
        "Rules:\n- Use the image, the copy and the numbers. Compare the ad's ROAS, CPA and link CTR with the account "
        "averages given. If the numbers are weak, say so honestly and set verdict accordingly.\n"
        "- Plain, short sentences. No jargon. Use digits. No em dashes.\n"
        "- 3 to 5 items in why. 3 to 6 items in keep and test_next. 1 to 3 in watch_out.\n"
        "- structure: describe what is actually in the image. Use \"none\" when a part is missing.\n\n"
        f"Reply with only this JSON:\n{BREAKDOWN_SHAPE}"
    )


def _images(image_bytes, media_type):
    """Normalise one image (bytes) or several [(bytes, media_type)] into a list of (base64, media_type)."""
    if not image_bytes:
        return []
    items = image_bytes if isinstance(image_bytes, (list, tuple)) else [(image_bytes, media_type)]
    return [(base64.b64encode(b).decode(), t or 'image/jpeg') for b, t in items if b]


def _ask(cfg, prompt, image_bytes, media_type='image/jpeg', max_tokens=2500):
    """One text answer from Claude (preferred) or OpenAI. Returns (text, model, provider).
    image_bytes is one image, or a list of (bytes, media_type) when a competitor reference goes along."""
    imgs = _images(image_bytes, media_type)
    if cfg['anthropic_key']:
        content = [{'type': 'image', 'source': {'type': 'base64', 'media_type': t, 'data': b}} for b, t in imgs] + [{'type': 'text', 'text': prompt}]
        body = json.dumps({'model': cfg['AI_TEXT_MODEL'], 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': content}]}).encode()
        out = _post('https://api.anthropic.com/v1/messages', {'x-api-key': cfg['anthropic_key'], 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}, body, cfg, timeout=180)
        text = ''.join(b.get('text', '') for b in out.get('content', []) if b.get('type') == 'text')
        model, provider = cfg['AI_TEXT_MODEL'], 'claude'
    elif cfg['openai_key']:
        content = [{'type': 'input_text', 'text': prompt}] + [{'type': 'input_image', 'image_url': f'data:{t};base64,{b}'} for b, t in imgs]
        body = json.dumps({'model': cfg['AI_OPENAI_TEXT_MODEL'], 'input': [{'role': 'user', 'content': content}]}).encode()
        out = _post('https://api.openai.com/v1/responses', {'Authorization': f"Bearer {cfg['openai_key']}", 'Content-Type': 'application/json'}, body, cfg, timeout=180)
        text = out.get('output_text') or ''.join(c.get('text', '') for item in out.get('output', []) for c in item.get('content', []) or [] if c.get('type') == 'output_text')
        model, provider = cfg['AI_OPENAI_TEXT_MODEL'], 'openai'
    else:
        raise AIError('AI is not set up on this computer yet.')
    return text, model, provider


def load_brand(path=None):
    try:
        return json.loads(Path(path or BRAND).read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        return {}


def brand_brief(brand=None):
    """A short brand block for image prompts."""
    b = brand if brand is not None else load_brand()
    if not b:
        return ''
    colors = ', '.join(f"{c.get('name')} {c.get('hex')}" for c in b.get('colors', [])[:5])
    photo = '; '.join(b.get('photography', [])[:5])
    return (f"Brand: {b.get('one_liner', '')}\n" + (f"Brand colours: {colors}.\n" if colors else '')
            + (f"Photography style: {photo}.\n" if photo else ''))


def ask_json(prompt, image_bytes=None, media_type='image/jpeg', env_path=None, max_tokens=4000):
    """Any JSON task from the page (copy packs, playbook, ideas). Returns parsed JSON."""
    cfg = settings(env_path)
    text, _, _ = _ask(cfg, prompt, image_bytes, media_type, max_tokens=max_tokens)
    return _json_from(text)


def breakdown(ad, image_bytes, media_type='image/jpeg', env_path=None):
    cfg = settings(env_path)
    text, model, provider = _ask(cfg, breakdown_prompt(ad), image_bytes, media_type)
    data = clean_breakdown(_json_from(text))
    data.update({'model': model, 'provider': provider, 'date': time.strftime('%Y-%m-%d')})
    return data


def _txt(v, n):
    return re.sub(r'[\x00-\x1f\x7f]', ' ', str(v or '')).strip()[:n]


def clean_breakdown(d):
    """Validate a breakdown (from a model or from the page) into a safe, bounded shape."""
    if not isinstance(d, dict):
        raise AIError('Bad breakdown.')
    lst = lambda v, n, m: [_txt(x, m) for x in (v if isinstance(v, list) else [])[:n] if _txt(x, m)]
    why = []
    for w in (d.get('why') if isinstance(d.get('why'), list) else [])[:6]:
        if isinstance(w, dict) and _txt(w.get('point'), 200):
            why.append({'point': _txt(w.get('point'), 200), 'evidence': _txt(w.get('evidence'), 400)})
        elif isinstance(w, str) and w.strip():
            why.append({'point': _txt(w, 200), 'evidence': ''})
    st = d.get('structure') if isinstance(d.get('structure'), dict) else {}
    out = {
        'verdict': d.get('verdict') if d.get('verdict') in ('worked', 'mixed', 'did_not_work') else 'mixed',
        'summary': _txt(d.get('summary'), 400),
        'why': why,
        'structure': {k: _txt(st.get(k), 300) for k in ('hook', 'layout', 'product', 'text_on_image', 'offer', 'proof', 'cta', 'look')},
        'keep': lst(d.get('keep'), 8, 200),
        'test_next': lst(d.get('test_next'), 8, 240),
        'watch_out': lst(d.get('watch_out'), 4, 240),
    }
    for k in ('model', 'provider', 'date'):
        if d.get(k):
            out[k] = _txt(d.get(k), 60)
    if not out['summary'] and not out['why']:
        raise AIError('The breakdown came back empty. Try again.')
    return out


def load_breakdowns(path=None):
    try:
        data = json.loads(Path(path or BREAKDOWNS).read_text(encoding='utf-8'))
        return {k: clean_breakdown(v) for k, v in data.items() if SAFE_ID.match(k)}
    except (FileNotFoundError, ValueError, AIError):
        return {}


def save_breakdown(ad_id, data, path=None):
    if not SAFE_ID.match(str(ad_id)):
        raise AIError('Bad ad id.')
    path = Path(path or BREAKDOWNS)
    with _lock:
        all_ = load_breakdowns(path)
        all_[str(ad_id)] = clean_breakdown(data)
        path.parent.mkdir(parents=True, exist_ok=True)
        path = Path(path).resolve()  # a link to the host's persistent disk is followed, not replaced
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(all_, ensure_ascii=False, indent=1), encoding='utf-8')
        tmp.replace(path)
    return all_[str(ad_id)]


# ---------- variants ----------
DIRECTIONS = [
    ('Same idea, new scene', 'Keep the same layout and message. Change the background, lighting and props so it feels like a fresh shoot.'),
    ('Product close-up', 'Make the jewellery the hero in a tight, sharp close-up on a clean premium background. Keep any headline short.'),
    ('Worn by a model', 'Show the same jewellery worn by an Indian woman in natural light, face partly visible, warm and aspirational.'),
    ('Proof-led', 'Lead with trust: a clean card layout that puts the proof from the original ad (reviews, certification, customers) next to the product.'),
]


PLAN_SHAPE = '''{"concepts": [
  {"name": "2 to 4 word concept name",
   "closeness": "close" | "new",
   "principle": "which reason from the breakdown this concept carries forward, in plain words",
   "idea": "the new creative idea in 1 sentence",
   "scene": "what the photo shows: setting, model or no model, props, light",
   "layout": "where product, text and proof sit",
   "text_on_image": "exact short text to print, taken only from the original ad copy, or empty"}
]}'''


def plan_prompt(ad, bd, n, has_ref=False, ref_role='layout'):
    return (
        "You are a creative director for Meta ads at an Indian fine jewellery brand, Gehna. Below is an image ad that "
        "performed well and a breakdown of why. Write " + str(n) + " creative concepts for new image ads.\n\n"
        + (("Image 1 is Gehna's winning ad. Image 2 is a Gehna product photo. Every concept must feature the exact piece from image 2, using the layout, framing, text style and mood that made image 1 work. Do not show the piece from image 1.\n\n" if ref_role == 'product' else
            "Image 1 is Gehna's ad. Image 2 is a reference ad the team picked. Every concept should use the reference's "
            "layout, framing, format or mood, with Gehna's product. Never copy the reference's text, logo, product, models or faces.\n\n")
           if has_ref else "")
        +
        "Concept 1 must be close to the original: same structure and message, fresh execution.\n"
        "Every other concept must be a genuinely different ad that keeps the PRINCIPLE behind the win (the reasons in "
        "the breakdown), not the layout. Change the scene, format and angle. Each new concept should carry a different "
        "reason from the breakdown, so the set tests different ideas.\n\n"
        "Rules: the jewellery shown stays the exact same piece. Never invent prices, discounts, ratings, certifications "
        "or claims; text_on_image may only reuse words from the original copy. Plain short sentences, digits, no em dashes.\n\n"
        f"Ad data (JSON):\n{json.dumps(ad, ensure_ascii=False)[:6000]}\n\nBreakdown (JSON):\n{json.dumps(bd or {}, ensure_ascii=False)[:6000]}\n\n"
        f"Brand kit (JSON):\n{json.dumps(load_brand(), ensure_ascii=False)[:4000]}\n\n"
        f"Reply with only this JSON:\n{PLAN_SHAPE}"
    )


def plan_concepts(cfg, ad, bd, n, image_bytes, media_type, ref_bytes=None, ref_role='layout'):
    """Creative briefs for n variants. Falls back to fixed directions if planning fails."""
    try:
        imgs = [(image_bytes, media_type), (ref_bytes, 'image/jpeg')] if ref_bytes else image_bytes
        text, _, _ = _ask(cfg, plan_prompt(ad, bd, n, bool(ref_bytes), ref_role), imgs, media_type, max_tokens=3000)
        raw = _json_from(text).get('concepts') or []
        out = []
        for c in raw[:n]:
            if not isinstance(c, dict) or not _txt(c.get('idea'), 400):
                continue
            out.append({k: _txt(c.get(k), 400) for k in ('name', 'closeness', 'principle', 'idea', 'scene', 'layout', 'text_on_image')})
        if len(out) >= min(2, n):
            out[0]['closeness'] = 'close'
            return out[:n]
    except (AIError, ValueError, AttributeError):
        pass
    return [{'name': label, 'closeness': 'close' if i == 0 else 'new', 'principle': '', 'idea': d, 'scene': '', 'layout': '', 'text_on_image': ''}
            for i, (label, d) in enumerate(DIRECTIONS[:n])]


def competitor_prompt(comp, ad, bd, n, has_ref=False):
    return (
        "You are a creative director for Meta ads at Gehna, an Indian fine jewellery brand. A competitor ad has been "
        f"running for {comp.get('days_running', '?')} days, which usually means it works. Competitor: {comp.get('brand', '')}. "
        f"Its headline: \"{comp.get('headline', '')}\". Format: {comp.get('format', 'unknown')}. CTA: {comp.get('cta', '')}.\n"
        f"Its text: \"{str(comp.get('body', ''))[:800]}\"\n"
        + ("Image 1 is Gehna's ad. Image 2 is the competitor ad.\n" if has_ref else "Gehna's ad image is attached.\n")
        + "Write " + str(n) + " concepts for new Gehna image ads. Borrow only the competitor's layout, format, framing and mood. "
        "Use Gehna's own product from Gehna's ad, Gehna's proof and Gehna's voice. Never copy the competitor's text, logo, "
        "product, models or faces, and never name them.\n"
        "Rules: the jewellery shown stays the exact piece from Gehna's ad. Never invent prices, discounts, ratings or claims; "
        "text_on_image may only reuse words from Gehna's own copy. Plain short sentences, digits, no em dashes.\n\n"
        f"Gehna ad data (JSON):\n{json.dumps(ad, ensure_ascii=False)[:5000]}\n\nWhy it worked (JSON):\n{json.dumps(bd or {}, ensure_ascii=False)[:5000]}\n\n"
        f"Brand kit (JSON):\n{json.dumps(load_brand(), ensure_ascii=False)[:4000]}\n\n"
        f"Reply with only this JSON (closeness is always \"new\"):\n{PLAN_SHAPE}"
    )


def _concepts_from(text, n):
    raw = _json_from(text).get('concepts') or []
    out = []
    for c in raw[:n]:
        if isinstance(c, dict) and _txt(c.get('idea'), 400):
            out.append({k: _txt(c.get(k), 400) for k in ('name', 'closeness', 'principle', 'idea', 'scene', 'layout', 'text_on_image')})
    return out


def make_competitor_variants(base_id, comp, ad, image_bytes, bd, n=3, size='square', quality='medium', env_path=None, out_dir=None, media_type='image/jpeg', ref_bytes=None):
    cfg = settings(env_path)
    if not cfg['openai_key']:
        raise AIError('Image making is not set up on this computer yet.')
    if not image_bytes:
        raise AIError('The product image is not downloaded yet. Open that ad once, then try again.')
    n = max(1, min(4, int(n)))
    both = [(image_bytes, media_type)] + ([(ref_bytes, 'image/jpeg')] if ref_bytes else [])
    text, _, _ = _ask(cfg, competitor_prompt(comp, ad, bd, n, bool(ref_bytes)), both, media_type, max_tokens=3000)
    concepts = _concepts_from(text, n)
    if not concepts:
        raise AIError('Could not plan ideas from this ad. Try again.')
    for c in concepts:
        c['closeness'] = 'new'
        c['has_ref'] = bool(ref_bytes)
    extra = {'source': 'competitor', 'comp_brand': _txt(comp.get('brand'), 60), 'comp_headline': _txt(comp.get('headline'), 200),
             'comp_ad_id': _txt(comp.get('ad_id'), 30)}
    images = [image_bytes] + ([ref_bytes] if ref_bytes else [])
    return _render(cfg, base_id, ad, bd, concepts, images, size, quality, out_dir, extra)


def concept_prompt(ad, bd, c):
    keep = '; '.join((bd or {}).get('keep', [])[:6])
    text = c.get('text_on_image') or ''
    return (
        ("Create a new Meta feed ad image for Gehna, an Indian fine jewellery brand. Image 1 is Gehna's winning ad: keep its layout, "
         "framing, text style and mood. Image 2 is the product photo: show exactly this piece and not the piece from image 1.\n"
         if c.get('ref_role') == 'product' else
         "Create a new Meta feed ad image for Gehna, an Indian fine jewellery brand. Image 1 is Gehna's ad: take the product from it. "
         "Image 2 is a reference ad: use it only for layout, framing, format and mood. Never copy its text, logo, product, models "
         "or faces.\n" if c.get('has_ref') else
         "Create a new Meta feed ad image for Gehna, an Indian fine jewellery brand. The attached image is the reference ad.\n")
        + "The jewellery must stay exactly the same piece: same metal colour, stones, shape and proportions. Do not invent new pieces.\n"
        + ("This version stays close to the reference: same structure and message, fresh execution.\n" if c.get('closeness') == 'close'
           else "This is a NEW ad, not a copy of the reference layout. Use the reference only for the product and the brand feel.\n")
        + (f"Principle to carry forward: {c['principle']}\n" if c.get('principle') else '')
        + f"Concept: {c.get('idea', '')}\n"
        + (f"Scene: {c['scene']}\n" if c.get('scene') else '')
        + (f"Layout: {c['layout']}\n" if c.get('layout') else '')
        + (f"Keep what worked: {keep}.\n" if keep else '')
        + (f"Text on the image, exactly: \"{text}\". No other text.\n" if text else "Keep text to a minimum; only short words from the original ad, or none.\n")
        + "Never add prices, discounts, ratings, certifications or claims that are not in the original. Spell text correctly. "
        "Photographic, premium, clear space near the edges, no watermarks.\n" + brand_brief()
    )


def variant_prompt(ad, bd, direction):
    keep = '; '.join((bd or {}).get('keep', [])[:6]) or 'the product, the brand feel and the main message'
    head = ad.get('headline') or ''
    return (
        "Create a new square-safe Meta feed ad image for Gehna, an Indian fine jewellery brand, based on the attached ad.\n"
        "The jewellery must stay exactly the same design: same metal colour, stones, shape and proportions. Do not invent new pieces.\n"
        f"Keep what made the original work: {keep}.\n"
        f"Direction for this version: {direction}\n"
        "Text on the image: use only short text that already appears in the original ad"
        + (f" (for example the headline \"{head}\")" if head else "")
        + ". Do not invent prices, discounts, ratings, certifications or claims. Keep text crisp and spelled correctly, or leave text out.\n"
        "Leave some clear space near the edges. Photographic, premium, no watermarks, no logos other than what the original shows."
    )


def _multipart(fields, files):
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for name, filename, ctype, data in files:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{filename}"\r\nContent-Type: {ctype}\r\n\r\n'.encode() + data + b'\r\n')
    parts.append(f'--{boundary}--\r\n'.encode())
    return b''.join(parts), f'multipart/form-data; boundary={boundary}'


_EXT = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}


def _kind(b):
    return 'image/png' if b[:8] == b'\x89PNG\r\n\x1a\n' else 'image/webp' if b[8:12] == b'WEBP' else 'image/jpeg'


def _edit(cfg, model, prompt, image_bytes, size, quality, fidelity=True):
    fields = {'model': model, 'prompt': prompt, 'size': size, 'quality': quality, 'n': '1', 'output_format': 'png'}
    if fidelity:
        fields['input_fidelity'] = 'high'
    images = image_bytes if isinstance(image_bytes, (list, tuple)) else [image_bytes]
    body, ctype = _multipart(fields, [('image[]', f'reference{i + 1}.{_EXT[_kind(b)]}', _kind(b), b) for i, b in enumerate(images) if b])
    return _post('https://api.openai.com/v1/images/edits', {'Authorization': f"Bearer {cfg['openai_key']}", 'Content-Type': ctype}, body, cfg, timeout=300)


def make_variant(cfg, prompt, image_bytes, size, quality):
    """One image. Tries the configured model, then the fallback; drops input_fidelity if refused."""
    last = None
    for model in dict.fromkeys([cfg['AI_IMAGE_MODEL'], cfg['AI_IMAGE_FALLBACK']]):
        for fidelity in (True, False):
            try:
                out = _edit(cfg, model, prompt, image_bytes, size, quality, fidelity)
                item = (out.get('data') or [{}])[0]
                if not item.get('b64_json'):
                    raise AIError('The image API returned no image.')
                return base64.b64decode(item['b64_json']), model
            except AIError as e:
                last = e
                msg = str(e).lower()
                if fidelity and 'input_fidelity' in msg:
                    continue          # this model does not take input_fidelity: retry without it
                if 'model' in msg and ('not found' in msg or 'does not exist' in msg or 'access' in msg or 'invalid' in msg):
                    break             # try the fallback model
                raise
    raise last


def make_variants(ad_id, ad, image_bytes, bd, n=3, size='square', quality='medium', env_path=None, out_dir=None, media_type='image/jpeg', plan=True, ref_bytes=None, ref_role='layout'):
    cfg = settings(env_path)
    if not cfg['openai_key']:
        raise AIError('Image making is not set up on this computer yet.')
    if not SAFE_ID.match(str(ad_id)):
        raise AIError('Bad ad id.')
    if not image_bytes:
        raise AIError('The ad image is not downloaded yet. Open the ad once so its image loads, then try again.')
    n = max(1, min(5, int(n)))
    size_px = SIZES.get(size, SIZES['square'])
    quality = quality if quality in QUALITIES else 'medium'
    ref_role = 'product' if ref_role == 'product' and ref_bytes else 'layout'
    concepts = plan_concepts(cfg, ad, bd, n, image_bytes, media_type, ref_bytes, ref_role) if plan and (cfg['anthropic_key'] or cfg['openai_key']) else \
        [{'name': l, 'closeness': 'close' if i == 0 else 'new', 'principle': '', 'idea': d} for i, (l, d) in enumerate(DIRECTIONS[:n])]
    if ref_bytes:
        for c in concepts:
            c['has_ref'] = True
            c['ref_role'] = ref_role
    images = [image_bytes, ref_bytes] if ref_bytes else image_bytes
    return _render(cfg, ad_id, ad, bd, concepts, images, size, quality, out_dir, {'source': 'variant', 'with_reference': bool(ref_bytes), 'ref_role': ref_role if ref_bytes else ''})


def _render(cfg, ad_id, ad, bd, concepts, image_bytes, size, quality, out_dir, extra):
    return _render_in(cfg, Path(out_dir or VARIANTS) / str(ad_id), concepts, image_bytes, size, quality, extra,
                      lambda c: concept_prompt(ad, bd, c))


def _render_in(cfg, folder, concepts, image_bytes, size, quality, extra, prompt_of, keep=()):
    """Make one image per concept in parallel and save each with a .json note. keep: concept fields saved too."""
    size_px = SIZES.get(size, SIZES['square'])
    quality = quality if quality in QUALITIES else 'medium'
    folder.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime('%Y%m%d-%H%M%S')

    def run(i_c):
        i, c = i_c
        label = c.get('name') or f'Version {i + 1}'
        try:
            png, model = make_variant(cfg, prompt_of(c), image_bytes, size_px, quality)
        except AIError as e:
            return {'label': label, 'error': str(e), **{k: c.get(k) or '' for k in keep}}
        name = f'{stamp}_{i + 1}.png'
        (folder / name).write_bytes(png)
        meta = {'label': label, 'closeness': c.get('closeness') or 'new', 'principle': c.get('principle') or '', 'idea': c.get('idea') or '',
                'file': name, 'model': model, 'size': size_px, 'quality': quality, 'date': time.strftime('%Y-%m-%d %H:%M'), **extra,
                **{k: c.get(k) or '' for k in keep}}
        (folder / (name + '.json')).write_text(json.dumps(meta), encoding='utf-8')
        return meta

    with ThreadPoolExecutor(max_workers=min(len(concepts), 3)) as pool:
        return list(pool.map(run, enumerate(concepts)))


def list_variants(ad_id, out_dir=None):
    if not SAFE_ID.match(str(ad_id)):
        return []
    folder = Path(out_dir or VARIANTS) / str(ad_id)
    out = []
    for meta in sorted(folder.glob('*.png.json'), reverse=True):
        try:
            m = json.loads(meta.read_text(encoding='utf-8'))
            if SAFE_FILE.match(m.get('file', '')) and (folder / m['file']).exists():
                out.append(m)
        except ValueError:
            continue
    return out[:24]


def variant_path(ad_id, name, out_dir=None):
    if not SAFE_ID.match(str(ad_id)) or not SAFE_FILE.match(name):
        return None
    p = Path(out_dir or VARIANTS) / str(ad_id) / name
    return p if p.is_file() else None


# ---------- ads for a best-selling product, from its site photos ----------
PRODUCT_ADS = DATA / 'product_ads'
SAFE_SLUG = re.compile(r'^[a-z0-9][a-z0-9-]{1,120}$')
COPY_FIELDS = ('primary_text', 'primary_alt', 'headline', 'headline_alt', 'description', 'uses')
PRODUCT_SHAPE = '''{"concepts": [
  {"name": "2 to 4 word concept name",
   "angle": "the selling angle in a few words, for example proof it sells, gifting, everyday wear, price, craft",
   "idea": "the ad idea in 1 sentence",
   "scene": "what the photo shows: setting, model or no model, props, light",
   "layout": "where product, text and proof sit",
   "text_on_image": "exact short text to print on the image, or empty",
   "uses": ["the page facts this ad is built on, copied short"],
   "primary_text": "Meta primary text: 2 to 4 short lines",
   "primary_alt": ["2 more primary texts that test other page facts"],
   "headline": "Meta headline, 40 characters or less",
   "headline_alt": ["2 more headlines, 40 characters or less"],
   "description": "Meta link description, 30 characters or less"}
]}'''


def _facts_line(p):
    bits = [f"Product: {p.get('name', '')}"]
    if p.get('code'):
        bits.append(f"Code: {p['code']}")
    if isinstance(p.get('price'), (int, float)):
        bits.append(f"Price on the site: Rs {int(p['price']):,}")
    if p.get('emi_months'):
        bits.append(f"EMI on the site: up to {p['emi_months']} months")
    if p.get('badge'):
        bits.append(f"Site badge: {p['badge']}")
    if p.get('sold'):
        bits.append(f"Website sales (context for you, not a claim for the ads): {p['sold']}")
    facts = [str(x)[:400] for x in p.get('facts') or [] if str(x).strip()][:40]
    if facts:
        bits.append('Facts from the product page (the only claims you may use):\n' + '\n'.join(f'- {x}' for x in facts))
    return '\n'.join(bits)


def product_prompt(p, n, n_photos, has_ref, fmt='square'):
    """Plan n image ads plus Meta copy for one product. Also used, as text only, by the shared page."""
    return (
        "You are a creative director and copywriter for Meta ads at Gehna, an Indian fine jewellery brand. "
        f"Write {n} ad concepts for 1 best-selling piece, each with its own Meta copy.\n\n"
        + (f"Images 1 to {n_photos} are the site photos of the exact piece. " if n_photos else "No product photo is attached; describe the piece only from the facts. ")
        + (f"Image {n_photos + 1} is a style reference: borrow its layout, framing, text style and mood only. Never copy its product, text, logo, models or faces.\n" if has_ref else "\n")
        + f"Format: {fmt} ({SIZES.get(fmt, SIZES['square'])}).\n\n"
        + _facts_line(p) + "\n"
        + (f"Site description: {p.get('description')}\n" if p.get('description') and not p.get('facts') else '')
        + "\nMake each concept test a different angle, and build each one on a different group of page facts: 1 close to a clean product ad, "
        "then for example craft and stones, trust (hallmark, exchange, returns), reviews and ratings, price and EMI, fast delivery, gifting "
        "or worn on the body. Pick the angles the facts support best. Quote customer words only without names.\n"
        "Rules: the piece shown is always this exact piece. Use only facts given here: never invent discounts, ratings, "
        "certifications, stock claims or delivery promises. A price may be used only as given. Copy: plain short sentences, "
        "digits for numbers, no em dashes, no hashtags, at most 1 emoji in primary text, and no words like elevate, timeless or stunning. "
        "Headlines and names in sentence case, never Title Case. Never claim a rank like number 1 or best seller unless a page fact says it.\n\n"
        f"Brand kit (JSON):\n{json.dumps(load_brand(), ensure_ascii=False)[:4000]}\n\n"
        f"Reply with only this JSON:\n{PRODUCT_SHAPE}"
    )


def product_image_prompt(p, c, n_photos, has_ref):
    text = c.get('text_on_image') or ''
    return (
        "Create a new Meta feed ad image for Gehna, an Indian fine jewellery brand.\n"
        + (f"Images 1 to {n_photos} are site photos of the product: show exactly this piece. " if n_photos else '')
        + (f"Image {n_photos + 1} is a style reference: use only its layout, framing, text style and mood. Never copy its product, text, logo, models or faces.\n" if has_ref else '\n')
        + "The jewellery must stay exactly the same piece: same metal colour, stones, shape and proportions. Do not invent new pieces.\n"
        + f"Product: {p.get('name', '')}.\n"
        + f"Concept: {c.get('idea', '')}\n"
        + (f"Scene: {c['scene']}\n" if c.get('scene') else '')
        + (f"Layout: {c['layout']}\n" if c.get('layout') else '')
        + (f"Text on the image, exactly: \"{text}\". No other text.\n" if text else "No text on the image.\n")
        + (f"This ad is built on: {'; '.join(c['uses'][:4])}.\n" if isinstance(c.get('uses'), list) and c.get('uses') else '')
        + "Never add discounts, ratings, certifications or claims. Spell text correctly. Photographic, premium, clear space near the edges, no watermarks.\n"
        + brand_brief()
    )


def _product_concepts(text, n):
    raw = _json_from(text).get('concepts') or []
    out = []
    for c in raw[:n]:
        if isinstance(c, dict) and _txt(c.get('idea'), 400):
            item = {k: _txt(c.get(k), 400) for k in ('name', 'angle', 'idea', 'scene', 'layout', 'text_on_image')}
            lines = [re.sub(r'[ \t]+', ' ', x).strip() for x in str(c.get('primary_text') or '').splitlines()]
            lst = lambda v, n, m: [(_txt(x, m) if m < 200 else '\n'.join(y.strip() for y in str(x).splitlines() if y.strip())[:m]) for x in (v if isinstance(v, list) else [])[:n] if str(x).strip()]
            item.update({'primary_text': '\n'.join(x for x in lines if x)[:700], 'headline': _txt(c.get('headline'), 60), 'description': _txt(c.get('description'), 60),
                         'primary_alt': lst(c.get('primary_alt'), 2, 700), 'headline_alt': lst(c.get('headline_alt'), 2, 60), 'uses': lst(c.get('uses'), 6, 160)})
            out.append(item)
    return out


def product_copy(p, n=4, photos=None, ref_bytes=None, fmt='square', env_path=None):
    """Concepts and Meta copy only (no images)."""
    cfg = settings(env_path)
    n = max(1, min(5, int(n)))
    photos = list(photos or [])
    imgs = photos + ([(ref_bytes, _kind(ref_bytes))] if ref_bytes else [])
    text, _, _ = _ask(cfg, product_prompt(p, n, len(photos), bool(ref_bytes), fmt), imgs, 'image/jpeg', max_tokens=4000)
    out = _product_concepts(text, n)
    if not out:
        raise AIError('Could not write ideas for this product. Try again.')
    return out


def make_product_ads(p, photos, n=4, size='square', quality='medium', ref_bytes=None, env_path=None, out_dir=None, extra=None):
    """Plan concepts with copy, then make 1 image per concept from the product photos (+ style reference)."""
    cfg = settings(env_path)
    if not cfg['openai_key']:
        raise AIError('Image making is not set up on this computer yet.')
    slug = str(p.get('slug') or '')
    if not SAFE_SLUG.match(slug):
        raise AIError('Bad product.')
    photos = list(photos or [])
    if not photos:
        raise AIError('No site photo of this product could be loaded, so an image ad would show the wrong piece.')
    concepts = product_copy(p, n, photos, ref_bytes, size, env_path)
    images = [b for b, _ in photos] + ([ref_bytes] if ref_bytes else [])
    info = {'source': 'product', 'product': _txt(p.get('name'), 160), 'product_code': _txt(p.get('code'), 40),
            'with_reference': bool(ref_bytes), **(extra or {})}
    return _render_in(cfg, Path(out_dir or PRODUCT_ADS) / slug, concepts, images, size, quality, info,
                      lambda c: product_image_prompt(p, c, len(photos), bool(ref_bytes)), keep=('angle', 'text_on_image') + COPY_FIELDS)


def list_product_ads(slug, out_dir=None):
    if not SAFE_SLUG.match(str(slug)):
        return []
    folder = Path(out_dir or PRODUCT_ADS) / str(slug)
    out = []
    for meta in sorted(folder.glob('*.png.json'), reverse=True):
        try:
            m = json.loads(meta.read_text(encoding='utf-8'))
            if SAFE_FILE.match(m.get('file', '')) and (folder / m['file']).exists():
                out.append(m)
        except ValueError:
            continue
    return out[:60]


def product_ad_path(slug, name, out_dir=None):
    if not SAFE_SLUG.match(str(slug)) or not SAFE_FILE.match(str(name)):
        return None
    p = Path(out_dir or PRODUCT_ADS) / str(slug) / name
    return p if p.is_file() else None


# ---------- catalog refresh and product story ----------
CATALOG_REFRESH = DATA / 'catalog_refresh'
PRODUCT_STORY = DATA / 'product_story'
SAFE_CODE = re.compile(r'^[A-Za-z0-9._-]{3,40}$')
_STUDIO_END = (" Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. "
               "The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. "
               "No text, no logo, no hands, no model, no other jewellery, no watermark.")
# Background styles for the premium photo. Ivory is the plain catalog look; the rest are for the feed.
CATALOG_STYLES = {
    'ivory': ("Ivory studio", "Premium studio photo of this jewellery piece for a luxury online catalog. Seamless warm ivory "
              "background with a very soft gradient, a touch lighter behind the piece. Large soft light from the top left and a "
              "gentle fill, so the gold glows with warm, true-to-life highlights and the stones catch small crisp sparkles. "
              "A soft natural contact shadow under the piece." + _STUDIO_END),
    'silk': ("Champagne silk", "Luxury campaign photo of this jewellery piece resting on softly draped champagne silk with "
             "gentle folds. Warm low side light, so the gold glows and the stones sparkle. Shallow depth of field: the silk "
             "falls into a creamy blur behind the piece. Rich, warm and calm, like a high-end jewellery brand ad." + _STUDIO_END),
    'stone': ("Stone plinth", "Editorial photo of this jewellery piece placed on a small honed ivory travertine block, with a "
              "warm beige plaster wall behind. Soft window light from one side and a long soft shadow. Calm, minimal and "
              "expensive, like a luxury brand's website. The block is simple and plain; the piece stays true to its real size."
              + _STUDIO_END),
    'sunlit': ("Sunlit shadows", "Golden hour photo of this jewellery piece on a warm sand-coloured surface. Soft dappled "
               "sunlight with a blurred leaf shadow falling across the background, but the piece itself in clear, even light. "
               "Warm, fresh and natural, made to stop the scroll in a social feed." + _STUDIO_END),
    'velvet': ("Deep velvet", "Dramatic luxury photo of this jewellery piece on deep emerald green velvet. Dark, rich "
               "background with a focused soft spotlight on the piece and a thin rim light, so the gold edges glow and the "
               "stones sparkle. High contrast but true colours for the metal and stones." + _STUDIO_END),
}
CATALOG_PROMPT = CATALOG_STYLES['ivory'][1]
# Always added after the team's prompt, so no prompt can change the piece itself.
KEEP_PIECE = ("\nThis must stay the exact same piece: same metal colour, stones, stone colours, shape, size, proportions, "
              "clasp and every detail, at its real size. Do not add, remove, straighten or redesign any part of the jewellery.")


def make_catalog_image(code, image_bytes, prompt='', quality='high', out_dir=None, env_path=None, size='square'):
    """1 premium catalog photo from the current catalog image. Returns the saved note (or an error)."""
    cfg = settings(env_path)
    if not cfg['openai_key']:
        raise AIError('Image making is not set up on this computer yet.')
    if not SAFE_CODE.match(str(code)):
        raise AIError('Bad product code.')
    if not image_bytes:
        raise AIError('The catalog image could not be loaded.')
    text = (str(prompt or '').strip()[:2000] or CATALOG_PROMPT) + KEEP_PIECE
    made = _render_in(cfg, Path(out_dir or CATALOG_REFRESH) / str(code), [{'name': 'Premium catalog photo', 'prompt': text}], [image_bytes],
                      size if size in SIZES else 'square', quality, {'source': 'catalog', 'code': str(code)}, lambda c: c['prompt'], keep=('prompt',))
    return made[0]


def list_catalog_images(out_dir=None):
    root = Path(out_dir or CATALOG_REFRESH)
    out = {}
    if root.is_dir():
        for folder in root.iterdir():
            if folder.is_dir() and SAFE_CODE.match(folder.name):
                items = []
                for meta in sorted(folder.glob('*.png.json'), reverse=True):
                    try:
                        m = json.loads(meta.read_text(encoding='utf-8'))
                        if SAFE_FILE.match(m.get('file', '')) and (folder / m['file']).exists():
                            items.append({k: m.get(k) for k in ('file', 'date', 'quality', 'model')})
                    except ValueError:
                        continue
                if items:
                    out[folder.name] = items[:12]
    return out


def catalog_image_path(code, name, out_dir=None):
    if not SAFE_CODE.match(str(code)) or not SAFE_FILE.match(str(name)):
        return None
    p = Path(out_dir or CATALOG_REFRESH) / str(code) / name
    return p if p.is_file() else None


BODY_PART = {'Earrings': 'ears', 'Chains': 'neck', 'Pendants': 'neck', 'Bracelets': 'wrist', 'Rings': 'finger', 'Nosepins': 'nose'}
# The product story: up to 15 images, in this order. {part} is where it is worn; {facts} are page facts.
STORY_SHOTS = [
    ('hero', 'Premium hero', 'A premium hero shot of the piece on a clean seamless warm off-white background, soft studio light, gentle shadow, centred. No text.'),
    ('lifestyle', 'Lifestyle hero', 'The piece styled on soft ivory silk with a few fresh flowers, warm natural window light, shallow depth of field. No text.'),
    ('macro', 'Close-up of the work', 'An extreme macro close-up of the stones and gold work, showing texture, setting and shine. No text.'),
    ('worn', 'Worn', 'The piece worn on the {part} of an Indian woman, natural light, face only partly visible, elegant and real. No text.'),
    ('worn_outfit', 'Worn with an outfit', 'The piece worn on the {part} with a simple elegant outfit (a saree or a plain dress), warm light, editorial feel. No text.'),
    ('scale', 'True size', 'The piece held in an open palm or next to a common object so its real size is clear, clean background. No text.'),
    ('gift', 'Gift box', 'The piece in an open premium jewellery gift box on a soft surface, ready to gift. No text.'),
    ('craft', 'Handmade', 'Close-up of a jeweller\'s hands finishing this piece at a workbench, warm light, no face. No text.'),
    ('benefits', 'Why buy', 'A clean product card: the piece on the left, and on the right these 3 short lines as crisp text: {facts3}. Plenty of space, premium look.'),
    ('details', 'Details', 'A clean product card with the piece and these details as crisp small text: {facts_detail}. Premium, easy to read.'),
    ('flatlay', 'Flat lay', 'A top-down flat lay of the piece on textured linen with soft shadows and a few minimal props. No text.'),
    ('festive', 'Festive', 'The piece in a warm festive setting with soft diya light and marigold petals, tasteful, not busy. No text.'),
    ('proof', 'Loved by buyers', 'A clean card with the piece and this line as crisp text: {proof}. Premium, simple.'),
    ('price', 'Price and EMI', 'A clean card with the piece and this line as crisp text: {price}. Premium, simple.'),
    ('pair', 'Side view', 'The same piece from a different angle (side or three-quarter view) on a clean background, showing depth. No text.'),
]


def story_concepts(p, n=10):
    facts = [str(f.get('text') if isinstance(f, dict) else f) for f in p.get('facts') or []]
    pick = lambda words: [f for f in facts if any(w in f.lower() for w in words)]
    trust = pick(['hallmark', 'exchange', 'return', 'natural gemstones'])[:3] or ['BIS hallmarked gold', 'Lifetime exchange', '7 day return']
    detail = (pick(['gold weight', 'stones:', 'length', 'k yellow', 'k rose', 'k white'])[:4]) or [p.get('name', '')]
    proof = (pick(['rated', 'badge'])[:1] or [''])[0]
    price = (pick(['price', 'emi'])[:2])
    fill = {'part': BODY_PART.get(p.get('cat') or '', 'body'), 'facts3': '; '.join(trust), 'facts_detail': '; '.join(detail),
            'proof': proof.replace('Site badge: ', ''), 'price': ' | '.join(price)}
    out = []
    for key, name, tmpl in STORY_SHOTS:
        if key == 'proof' and not proof or key == 'price' and not price:
            continue
        out.append({'name': name, 'shot': key, 'prompt': tmpl.format(**fill)})
    return out[:max(1, min(15, int(n)))]


def story_prompt(p, c):
    return ("Create 1 image for the product page and ads of Gehna, an Indian fine jewellery brand. The attached photos show the product: "
            f"{p.get('name', '')}.\n" + c['prompt'] + KEEP_PIECE +
            "\nOnly use text given here, spelled exactly. Photographic, premium, no watermark, no logo.\n" + brand_brief())


def make_story(p, photos, n=10, size='square', quality='medium', env_path=None, out_dir=None):
    cfg = settings(env_path)
    if not cfg['openai_key']:
        raise AIError('Image making is not set up on this computer yet.')
    slug = str(p.get('slug') or '')
    if not SAFE_SLUG.match(slug):
        raise AIError('Bad product.')
    if not photos:
        raise AIError('No product photo could be loaded, so the story would show the wrong piece.')
    concepts = story_concepts(p, n)
    return _render_in(cfg, Path(out_dir or PRODUCT_STORY) / slug, concepts, [b for b, _ in photos][:3], size, quality,
                      {'source': 'story', 'product': _txt(p.get('name'), 160)}, lambda c: story_prompt(p, c), keep=('shot',))


def list_story(slug, out_dir=None):
    return list_product_ads(slug, out_dir=out_dir or PRODUCT_STORY)


def story_path(slug, name, out_dir=None):
    return product_ad_path(slug, name, out_dir=out_dir or PRODUCT_STORY)
