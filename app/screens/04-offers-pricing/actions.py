"""Rank for screen 04 (depth.md section 5): every audit finding becomes an action a person can approve today.

`rank(brand, window)` runs audit.run, starts each action from app/rank.py's default (rubric, owner, capability),
then a builder per rule writes the real title, owner, steps with who, the artefact with its drafted text, the
size, the win and stop rules and the check date. Unavailable findings keep rank.py's connect action. No model call;
same tables, brain and window give the same actions in the same order.
"""
import importlib.util
import math
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '04-offers-pricing'


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


audit = _load('offers_pricing_audit_mod', HERE / 'audit.py')
model = _load('offers_pricing_model', HERE / 'model.py')
RANK = _load('ecomos_rank', APP / 'rank.py')


def money(v, digits=None):
    if v is None:
        return 'unavailable'
    if digits is None:
        digits = 0 if abs(v) >= 1000 else 2
    return f'${v:,.{digits}f}'


def pct(v, digits=1):
    return 'unavailable' if v is None else f'{v * 100:.{digits}f} percent'


def step(n, who, text):
    return {'n': n, 'who': who, 'text': text}


def steps(*rows):
    return [step(i + 1, who, text) for i, (who, text) in enumerate(rows)]


# ---------------------------------------------------------------- context shared by the builders

class Ctx:
    """Numbers several builders need, computed once per rank call."""

    def __init__(self, rd):
        self.rd = rd
        self.end = rd.ends_on
        self.threshold, _ = audit.threshold_usd(rd)
        self.be = audit.break_even(rd, self.end)
        self.contribution = model.contribution_28d(rd)
        self.totals = model.window_totals(rd)
        self.po = model.per_order(self.totals)

    def check_on(self, days):
        return (self.end + timedelta(days=days)).isoformat()


# ---------------------------------------------------------------- builders, one per rule

def threshold_action(f, a, ctx):
    t, be = ctx.threshold, ctx.be
    new = math.ceil(be['value'] / 5) * 5
    stake = f.get('money_at_stake')
    size = (f'{money(stake["usd"])} of labels in 28 days on orders from ${t:,.0f} to ${be["value"]:,.2f}' if stake else
            f'Label cost on orders from ${t:,.0f} to ${be["value"]:,.2f} is unavailable until order rows connect')
    brief = '\n'.join([
        f'Test brief: free shipping at ${new} against ${t:,.0f}',
        f'Why: break-even is ${be["value"]:,.2f} (AOV {money(be["aov"])} plus the {money(be["label"])} label over a '
        f'{be["gross_margin"] * 100:.0f} percent margin). Every free order under it ships at a loss on the label.',
        f'Arms: A keeps ${t:,.0f}. B moves the line to ${new}. Same cart bar, same copy, only the number changes.',
        'Split: 50/50 by visitor, new and returning, all devices, 28 days.',
        'Primary metric: contribution per visitor (net minus landed cost, label, pick and pack, fees).',
        'Guard: conversion rate by arm, AOV by arm, share of orders in the $10 under each line.',
        'Win: contribution per visitor up in B with conversion down less than 3 percent relative.',
        'Stop: conversion in B down more than 5 percent relative for 7 days in a row.',
    ])
    a.update({
        'title': f'Test free shipping at ${new} against ${t:,.0f}',
        'why': f['sentence'] + f' Break-even is AOV {money(be["aov"])} plus the {money(be["label"])} label over a '
               f'{be["gross_margin"] * 100:.0f} percent margin.',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'test_brief', 'label': f'Test brief: free shipping at ${new} against ${t:,.0f}', 'draft': brief},
        'steps': steps(
            ('agent', f'Count orders from ${t:,.0f} to ${new} in the last 28 days and the label they cost.'),
            ('agent', 'Draft the test brief and the cart bar line for both arms.'),
            ('person', 'Approve the brief. Set arm B in the shipping rates app. Nothing changes before that.'),
            ('agent', 'Read conversion, AOV and contribution per visitor by arm every 7 days.'),
            ('agent', f'Call the test on {ctx.check_on(35)} with the win and stop rules.')),
        'size': {'text': size, 'usd': stake['usd'] if stake else None},
        'win_rule': 'Contribution per visitor up in B, conversion down less than 3 percent relative.',
        'stop_rule': 'Conversion in B down more than 5 percent relative for 7 days in a row.',
        'check_on': ctx.check_on(35), 'time_to_ship_hours': 4,
    })
    return a


def rung_action(f, a, ctx):
    doubt = f['entity']['label'].split(': ', 1)[-1]
    theme = f['entity']['id'].split('.')[0].replace('_', ' ')
    a.update({
        'title': f'Answer "{doubt}" with an offer and proof',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'offer', 'label': f'Offer spec for the {theme} deal-breaker', 'draft': None,
                     'draft_note': 'The agent drafts the offer spec from the ladder, the guarantee and the returns once approved.'},
        'steps': steps(
            ('agent', f'Pull the one-star quotes and the returns behind "{doubt}".'),
            ('agent', 'Draft an offer that removes the risk, priced from finance inputs.'),
            ('person', 'Approve the offer and its margin cost.'),
            ('agent', 'Add the offer line to the product page and the ads that meet this doubt.')),
        'check_on': ctx.check_on(28), 'time_to_ship_hours': 6,
    })
    return a


BUILDERS = {'OFFER-R01': threshold_action, 'OFFER-R04': rung_action}


def build(f, rd, ctx, nr):
    a = RANK.action_from_finding(f, nr)
    a['screen'] = SCREEN
    if f.get('status') == 'unavailable':
        return a
    fn = BUILDERS.get(f['rule_id'])
    return fn(f, a, ctx) if fn else a


def ends_on(brand, window):
    last = audit.last_full_day(None, brand)
    want = (window or {}).get('ends_on')
    if want:
        want = date.fromisoformat(str(want)[:10])
        return min(want, last)
    return last


def rank(brand='bombas', window=None):
    end = ends_on(brand, window)
    w = {'ends_on': end.isoformat(), 'days': audit.WINDOW}
    findings = audit.run(brand, w)
    rd = audit.Reader(None, brand, end)
    ctx = Ctx(rd)
    nr = RANK.net_revenue_28d(brand, w)
    actions = [build(f, rd, ctx, nr) for f in findings if f.get('status') in ('open', 'unavailable', None)]
    actions = [a for a in actions if not RANK.validate_action(a)]
    actions.sort(key=RANK.sort_key)
    return {'screen': SCREEN, 'brand': brand, 'window': w, 'simulated': True, 'net_revenue_28d': nr,
            'actions': actions, 'findings': findings}
