"""Builds REVIEW.md and review.html for the Bombas simulated data (session S2.5).
Reads only aggregates/*.json, manifest.json and finance_inputs.json. No paid calls.
Run: python3 app/data/brands/bombas/review/build_review.py [artifact_url]"""
from __future__ import annotations
import json, sys, os, collections, statistics as st, datetime as dt, html as H
sys.path.insert(0, os.path.dirname(__file__))
import charts as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "aggregates")
L = lambda n: json.load(open(os.path.join(A, n)))["rows"]
mo, ch, co, pr, wh, dy = (L(n) for n in ("monthly.json", "channels_monthly.json", "cohorts.json", "products_monthly.json", "wholesale_monthly.json", "daily.json"))
man = json.load(open(os.path.join(ROOT, "manifest.json")))
fin = json.load(open(os.path.join(ROOT, "finance_inputs.json")))["rows"]
ph = man["placeholders"]
ART_URL = sys.argv[1] if len(sys.argv) > 1 else None
OUT = os.path.join(ROOT, "review", "charts")
os.makedirs(OUT, exist_ok=True)

MN = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
IDX = {v: man["fields"]["seasonality"]["value"][k] for k, v in MN.items()}
full = [m for m in mo if m["days"] >= 28]                      # 23 full months
W12 = [m for m in mo if "2025-09" <= m["month"] <= "2026-08"]   # last 12 full months
inw = lambda s: "2025-09" <= s <= "2026-08"
T = lambda k, rows=W12: sum(m[k] for m in rows)
mlab = lambda s: dt.date(int(s[:4]), int(s[5:]), 1).strftime("%b %y")
labels = [mlab(m["month"]) for m in full]
pct = lambda v, d=1: f"{v * 100:.{d}f}%"
usd = lambda v: f"${v / 1e6:,.1f}M" if abs(v) >= 1e6 else f"${v:,.0f}"
num = lambda v: f"{v:,.0f}"

SVG = {}
def chart(name, svg):
    SVG[name] = svg
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)

# ---------- 1 revenue and seasonality ----------
chart("revenue", C.columns("Net sales by month (orders only, USD)", labels, [[m["net_sales"] for m in full]], unit="$", subtitle="23 full months, Oct 2024 to Aug 2026", label_every=2))
g = 1 + man["fields"]["revenue_band"]["value"]["growth_per_year"]
detr = [m["net_sales"] / m["days"] / (g ** ((i - 11) / 12)) for i, m in enumerate(W12)]
avg = st.mean(detr)
gen_idx = [v / avg for v in detr]
tgt_idx = [IDX[int(m["month"][5:])] for m in W12]
chart("seasonality", C.columns("Seasonality index: generated vs brain", [mlab(m["month"]) for m in W12], [gen_idx, tgt_idx], subtitle="detrended at 29.1% a year, mean = 1", legend_names=["generated", "brain index"]))
yoy = []
d = {m["month"]: m for m in mo}
for m in full:
    y = str(int(m["month"][:4]) - 1) + m["month"][4:]
    if y in d and d[y]["days"] >= 28:
        yoy.append((m["month"], m["net_sales"] / d[y]["net_sales"] - 1))
seas_rows = [(mlab(m["month"]), f"{gi:.3f}", f"{ti:.3f}", f"{gi - ti:+.3f}") for m, gi, ti in zip(W12, gen_idx, tgt_idx)]

# ---------- 2 AOV and pack mix ----------
chart("aov", C.lines("AOV by month (net merchandise per order)", labels, [[m["aov"] for m in full]], unit="$", ylo=68, yhi=78, ref=(73.0, "brain estimate $73"), label_every=2))
sk = collections.defaultdict(lambda: [0, 0, ""])
for r in pr:
    if inw(r["month"]):
        sk[r["sku"]][0] += r["units"]; sk[r["sku"]][1] += r["net_sales"]; sk[r["sku"]][2] = r["category"]
tu = sum(v[0] for v in sk.values()); ts = sum(v[1] for v in sk.values())
packs = collections.defaultdict(lambda: [0, 0])
for k, v in sk.items():
    n = int(k.split("-")[-1]); packs[n][0] += v[0]; packs[n][1] += v[1]
pk = sorted(packs)
chart("packmix", C.hbars("Share of net sales by pack size (last 12 months)", [f"{n}-pack" if n > 1 else "single" for n in pk], [packs[n][1] / ts for n in pk], unit="%", subtitle="units share in the table"))
cat = collections.defaultdict(float)
for k, v in sk.items():
    cat[v[2]] += v[1]
pack_rows = [(f"{n}-pack" if n > 1 else "single", pct(packs[n][0] / tu), pct(packs[n][1] / ts), f"${packs[n][1] / packs[n][0]:.2f}") for n in pk]
top_skus = sorted(sk.items(), key=lambda x: -x[1][1])[:5]

# ---------- 3 new vs repeat, cohorts ----------
chart("newrepeat", C.columns("Orders by month: new vs returning customers", labels, [[m["new_customer_orders"] for m in full], [m["returning_customer_orders"] for m in full]], stacked=True, legend_names=["new customer", "returning"], label_every=2))
cs = {c["cohort"]: c for c in co}
def curve(name, k=12):
    c = cs[name]; return [x / c["customers"] for x in c["active_by_month"][1:k + 1]]
chart("cohorts", C.lines("Repeat curve: share of cohort ordering in month k after first order", [str(i) for i in range(1, 24)], [curve("2024-10", 23), curve("2024-12", 21), curve("2025-06", 15)], unit="%", ylo=0, yhi=0.10, legend_names=["Oct 2024 cohort", "Dec 2024 cohort", "Jun 2025 cohort"], end_labels=False))
coh_rows = []
for name in ("2024-10", "2024-12", "2025-03", "2025-06", "2025-09"):
    c = cs[name]; a = c["active_by_month"]; n = c["customers"]
    y1 = sum(a[1:13]) / n; y2 = sum(a[13:25]) / n if len(a) > 13 else None
    coh_rows.append((name, num(n), pct(a[1] / n), pct(a[2] / n), pct(a[6] / n), pct(a[12] / n) if len(a) > 12 else "n/a", f"{y1:.2f}", f"{y2:.2f}" if y2 else "n/a"))
new_share_12 = T("new_customer_orders") / T("orders")
ns_by_m = {m["month"]: m["new_customer_orders"] / m["orders"] for m in mo}

# ---------- 4 channel shares ----------
wp = collections.defaultdict(float); wm = collections.defaultdict(float)
for r in wh:
    wm[r["month"]] += r["net_sales"]
    if inw(r["month"]): wp[r["partner"]] += r["net_sales"]
byM = collections.defaultdict(dict)
for r in ch: byM[r["month"]][r["channel"]] = r
pos_net = sum(byM[m["month"]].get("pos", {}).get("net_sales", 0) for m in W12)
site_net = T("net_sales") - pos_net
whol = sum(wp.values())
tot_rev = site_net + pos_net + whol
sales_lab = ["DTC site", "Wholesale (fixture)", "Owned retail (POS)", "Marketplaces"]
sales_val = [site_net / tot_rev, whol / tot_rev, pos_net / tot_rev, 0]
sales_ref = [0.90, 0.09, 0.01, 0]
chart("saleschannels", C.hbars("Revenue by sales channel (last 12 months)", sales_lab, sales_val, unit="%", value_labels=[pct(sales_val[0]), pct(sales_val[1]), pct(sales_val[2]), "unavailable (brain: null)"], ref_values=sales_ref))
w_share_by_m = [wm[m["month"]] / (wm[m["month"]] + m["net_sales"]) for m in full]
partner_rows = sorted(((k, v) for k, v in wp.items()), key=lambda x: -x[1])
CH = ["paid_social", "paid_search", "organic_search", "direct", "email_sms", "other"]
CHN = ["paid social", "paid search", "organic search", "direct", "email + SMS", "other"]
def cshare(m, c):
    d = byM[m["month"]]; tot = sum(r["orders"] for k, r in d.items() if k != "pos")
    if c == "email_sms": return (d["email"]["orders"] + d["sms"]["orders"]) / tot
    return d[c]["orders"] / tot
chart("acq", C.columns("Web orders by acquisition channel (share of month)", labels, [[cshare(m, c) for m in full] for c in CH], unit="%", stacked=True, legend_names=CHN, label_every=2, ymax=1.0, h=320))
ca = collections.defaultdict(lambda: [0, 0, 0])
for r in ch:
    if inw(r["month"]): ca[r["channel"]][0] += r["orders"]; ca[r["channel"]][1] += r["net_sales"]; ca[r["channel"]][2] += r["new_customer_orders"]
web_o = sum(v[0] for k, v in ca.items() if k != "pos")
fb = man["fields"]["channel_mix"]["value"]
acq_rows = []
for c, nm in zip(CH, CHN):
    if c == "email_sms":
        o = ca["email"][0] + ca["sms"][0]; n = ca["email"][1] + ca["sms"][1]; nw = ca["email"][2] + ca["sms"][2]
    else:
        o, n, nw = ca[c]
    acq_rows.append((nm, pct(o / web_o), pct(fb[c] / 100, 0), f"${n / o:.2f}", pct(nw / o, 0)))

# ---------- 5 funnel ----------
cvr = [m["ga4_transactions"] / m["sessions"] for m in full]
chart("cvr", C.lines("Site conversion rate by month (GA4 transactions / sessions)", labels, [cvr], unit="%", ylo=0, yhi=0.025, label_every=2))
sess12 = T("sessions"); tx12 = T("ga4_transactions")
dev = ph["device_share"]; dm = ph["cvr_device_mult"]
blend = sum(dev[k] * dm[k] for k in dev)
base_cvr = tx12 / sess12 / blend
dev_rows = [(k, pct(dev[k], 0), f"{dm[k]:.2f}x", pct(base_cvr * dm[k], 2)) for k in ("mobile", "desktop", "tablet")]
src_rows = [(k, pct(v, 1)) for k, v in ph["cvr_by_channel"].items()]

# ---------- 6 paid ----------
chart("spend", C.columns("Ad spend by month", labels, [[m["meta_spend"] for m in full], [m["google_spend"] for m in full]], unit="$", stacked=True, legend_names=["Meta", "Google"], label_every=2))
meta_cpa = [m["meta_spend"] / m["meta_purchases"] for m in full]
goog_cpa = [m["google_spend"] / m["google_conversions"] for m in full]
chart("cpa", C.lines("Platform CPA by month (spend / platform-reported purchases)", labels, [meta_cpa, goog_cpa], unit="$", ylo=0, yhi=60, legend_names=["Meta CPA", "Google CPA"], label_every=2))
meta_roas = [m["meta_purchases"] * m["aov"] / m["meta_spend"] for m in full]
goog_roas = [m["google_conversions"] * m["aov"] / m["google_spend"] for m in full]
chart("roas", C.lines("Platform ROAS by month (purchases x AOV / spend, a proxy)", labels, [meta_roas, goog_roas], unit="x", ylo=0, yhi=3.5, legend_names=["Meta", "Google"], label_every=2))
att = [[m["meta_purchases"] / m["orders"] for m in full], [m["google_conversions"] / m["orders"] for m in full], [m["klaviyo_attributed_orders"] / m["orders"] for m in full]]
chart("attribution", C.columns("Platform-attributed purchases as a share of Shopify orders", labels, att, unit="%", stacked=True, legend_names=["Meta", "Google", "Klaviyo"], ymax=1.0, ref=(1.0, "all orders"), label_every=2))
paid_rows = []
for m in [x for x in mo if x["month"] in ("2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-05", "2026-08")]:
    paid_rows.append((mlab(m["month"]), usd(m["meta_spend"]), f"${m['meta_spend'] / m['meta_purchases']:.1f}", f"{m['meta_purchases'] * m['aov'] / m['meta_spend']:.2f}x", usd(m["google_spend"]), f"${m['google_spend'] / m['google_conversions']:.1f}", f"{m['google_conversions'] * m['aov'] / m['google_spend']:.2f}x", pct((m["meta_purchases"] + m["google_conversions"] + m["klaviyo_attributed_orders"]) / m["orders"], 0)))
meta12, goog12 = T("meta_spend"), T("google_spend")
mer = T("net_sales") / (meta12 + goog12)

# ---------- 7 email ----------
kl = [m["klaviyo_attributed_orders"] / m["orders"] for m in full]
em = [(byM[m["month"]]["email"]["orders"] + byM[m["month"]]["sms"]["orders"]) / m["orders"] for m in full]
chart("email", C.lines("Email and SMS: Klaviyo-attributed share vs last-click share of orders", labels, [kl, em], unit="%", ylo=0, yhi=0.25, legend_names=["Klaviyo attributed", "email + SMS last click"], label_every=2))
kl12 = T("klaviyo_attributed_orders") / T("orders")
em12 = sum(byM[m["month"]]["email"]["orders"] + byM[m["month"]]["sms"]["orders"] for m in W12) / T("orders")

# ---------- 8 ops ----------
tk = [1000 * m["tickets"] / m["orders"] for m in full]
chart("tickets", C.columns("Support tickets per 1,000 orders", labels, [tk], ref=(1000 * ph["ticket_rate"], "manifest placeholder 35"), label_every=2, ymax=150))
rf = [m["refunds_on_orders"] / m["net_sales"] for m in full] + [mo[-1]["refunds_on_orders"] / mo[-1]["net_sales"]]
chart("refunds", C.lines("Refunds as a share of net sales, by order month", labels + ["Sep 26*"], [rf], unit="%", ylo=0, yhi=0.05, label_every=2))
tk12 = 1000 * T("tickets") / T("orders"); rf12 = T("refunds_on_orders") / T("net_sales")
ops_rows = [("Tickets per 1,000 orders", f"{tk12:.0f}", "35 (manifest ticket_rate 0.035)", "40 to 80 for DTC apparel; 100+ reads as a support problem"),
            ("Tickets per 1,000 orders, December", f"{1000 * d['2025-12']['tickets'] / d['2025-12']['orders']:.0f}", "60 (ticket_rate_dec 0.06)", "1.5x to 2x the base month"),
            ("Return rate (orders)", "not in aggregates", "6.0% (return_rate)", "3% to 8% for socks; fine"),
            ("Refunds / net sales", pct(rf12, 1), "implied by 6% returns on one line", "2% to 5%; fine"),
            ("Chargebacks / orders", "not in aggregates", "0.40% (chargeback_rate)", "0.10% to 0.25%; 0.4% is near card-network warning levels"),
            ("Checkout abandonment", "not in aggregates", "0.75 abandoned per order = 43%", "65% to 75%; low")]

# ---------- 9 margin by channel ----------
cogs_share_net = ph["cogs_share_of_price"] / (1 - T("discounts") / T("gross_sales"))
upo = T("units") / T("orders")
orders12 = T("orders"); net12 = T("net_sales"); ship12 = T("shipping"); ref12 = T("refunds_on_orders")
def contrib(c):
    o, n, _ = ca[c]
    pos = c == "pos"
    cogs = cogs_share_net * n
    fulfil = (2.85 + 0.62 + 0.35 * upo + (0 if pos else 5.3)) * o
    fees = (0.026 * n + 0.10 * o) if pos else (0.024 * n + 0.30 * o)
    ret = 4.25 * ph["return_rate"] * o + ref12 / net12 * n
    shiprev = 0 if pos else ship12 / orders12 * o
    gm = n + shiprev - cogs - fulfil - fees - ret
    ads = meta12 if c == "paid_social" else goog12 if c == "paid_search" else 0
    return o, n, gm / n, (gm - ads) / n, ads / o
MCH = ["paid_social", "paid_search", "organic_search", "direct", "email", "sms", "other", "pos"]
MCHN = ["paid social", "paid search", "organic search", "direct", "email", "SMS", "other", "owned retail (POS)"]
mrows = [contrib(c) for c in MCH]
chart("margin", C.hbars("Contribution margin by channel after its own ad spend (last 12 months)", MCHN, [r[3] for r in mrows], unit="%", ref=(0.22, "target 22%")))
margin_rows = [(nm, num(r[0]), f"${r[1] / r[0]:.2f}", pct(r[2], 1), f"${r[4]:.2f}" if r[4] else "none", pct(r[3], 1)) for nm, r in zip(MCHN, mrows)]
gm_all = sum(r[2] * r[1] for r in mrows) / net12; cm_all = sum(r[3] * r[1] for r in mrows) / net12
fixed = (4100000 * 6 + 3900000 * 6) + 950000 * 12 + 160000 * 12 + (40000 + 42000 + 9000 + 6500 + 7000 + 12000) * 12 + 185000 * 12
fk = set(r["scope_key"] for r in fin if r["field"] == "cogs_landed"); pkeys = set(sk)
cg = {r["scope_key"]: r["value"] for r in fin if r["field"] == "cogs_landed" and r["effective_to"] is None}
price = {k: v[1] / v[0] for k, v in sk.items()}
cogs_pairs = [("BMB-SK-M-ANK-4", "BB-ANK-4"), ("BMB-SK-M-ANK-1", "BB-ANK-1"), ("BMB-SK-MER-3", "BB-MER-3"), ("BMB-SK-CMP-3", "BB-CMP-3"), ("BMB-UW-M-BRF-3", "BB-BXB-3")]
cogs_rows = [(a, b, f"${cg[a]:.2f}", f"${price[b]:.2f}", pct(cg[a] / price[b], 0)) for a, b in cogs_pairs]

# ---------- 10 zero vs unavailable ----------
pos_zero = sum(1 for r in ch if r["channel"] == "pos" and r["orders"] == 0)
zero_rows = [("channels_monthly, channel = pos, 14 months before the store opened (Nov 2025)", "0 orders, $0", "no row, or null: the store did not exist"),
             ("monthly.pos_orders before Nov 2025", "0", "acceptable as 0 (orders table truly has none), but screens should say 'no stores yet'"),
             ("marketplace_listings", "0 rows, brain share null", "correct: reads unavailable"),
             ("finance_inputs before 2025-01-01 (data starts 2024-09-28)", "no rows", "margin for Oct to Dec 2024 must read unavailable, not $0 cost"),
             ("refunds for the latest order month (Sep 2026)", pct(rf[-1], 1) + " vs 3.5% mature", "real lag; label the last 30 to 60 days as maturing, not low"),
             ("daily.refunds_on_orders", "8 days at 0", "fine (partial days at the window edges)")]

# ---------- 11 daily shape ----------
wd = collections.defaultdict(list)
for x in dy: wd[dt.date.fromisoformat(x["date"]).weekday()].append(x["orders"])
avg_o = st.mean(x["orders"] for x in dy)
wd_idx = [st.mean(wd[i]) / avg_o for i in range(7)]
chart("weekday", C.columns("Orders by weekday, index to the average day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], [wd_idx], ref=(1.0, "average day"), ymax=1.3, h=240))
q = [x["orders"] for x in dy if x["date"].startswith("2026-06")]
june_cv = st.pstdev(q) / st.mean(q)
bf = {x["date"]: x for x in dy}
bfcm = [(k, num(bf[k]["orders"]), f"{bf[k]['orders'] / st.mean([bf[j]['orders'] for j in ('2025-11-17','2025-11-18','2025-11-19','2025-11-20')]):.1f}x", pct(bf[k]["discounts"] / bf[k]["gross_sales"], 1), f"${bf[k]['net_sales'] / bf[k]['orders']:.2f}", pct(bf[k]["new_customer_orders"] / bf[k]["orders"], 0)) for k in ("2025-11-27", "2025-11-28", "2025-11-29", "2025-11-30", "2025-12-01", "2025-12-02")]
dec = [(k, num(bf[k]["orders"])) for k in ("2025-12-18", "2025-12-19", "2025-12-20", "2025-12-22", "2025-12-24")]

# ================= sections =================
def table(head, rows, align=None):
    align = align or ["l"] + ["r"] * (len(head) - 1)
    md = "| " + " | ".join(head) + " |\n|" + "|".join("---:" if a == "r" else "---" for a in align) + "|\n"
    md += "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in rows) + "\n"
    ht = "<table><thead><tr>" + "".join(f'<th class="{a}">{H.escape(h)}</th>' for h, a in zip(head, align)) + "</tr></thead><tbody>"
    ht += "".join("<tr>" + "".join(f'<td class="{a}">{H.escape(str(c))}</td>' for c, a in zip(r, align)) + "</tr>" for r in rows) + "</tbody></table>"
    return md, ht

S = []  # (id, title, status, paragraphs[list of str], tables[list of (md,html)], charts[list of names], extra)
def sec(id, title, status, paras, tables=(), charts=()):
    S.append(dict(id=id, title=title, status=status, paras=paras, tables=list(tables), charts=list(charts)))

top5 = ", ".join(f"{k} {pct(v[1] / ts, 0)}" for k, v in top_skus)
sec("revenue", "1. Revenue by month against the brain's seasonality index", "pass",
    [f"Net sales on orders for the last 12 full months are {usd(net12)}, plus {usd(whol)} wholesale fixture, so {usd(tot_rev)} against the brain's $450M to $550M band. The month shape follows the brain index once the 29.1% growth trend is removed: the largest gap is {max(abs(a - b) for a, b in zip(gen_idx, tgt_idx)):.3f} (December, generated a little flatter than the index).",
     f"Year on year growth is {min(v for _, v in yoy) * 100:.1f}% to {max(v for _, v in yoy) * 100:.1f}% in every month. That is the assumption applied backward, not a brand's history: a real 2 year series wobbles by 5 to 10 points from month to month around its trend. Screens that show growth will look synthetic until the generator adds month level noise.",
     f"Daily shape is good: Cyber Monday 2025 is {bf['2025-12-01']['orders'] / st.mean([bf[j]['orders'] for j in ('2025-11-17','2025-11-18','2025-11-19','2025-11-20')]):.1f}x a normal November day, Black Friday {bf['2025-11-28']['orders'] / st.mean([bf[j]['orders'] for j in ('2025-11-17','2025-11-18','2025-11-19','2025-11-20')]):.1f}x, and orders halve after the December 19 shipping cutoff. The weekday curve (Sunday high, Thursday low) is right for a sock brand. Day to day noise inside a quiet month is small (June 2026 coefficient of variation {june_cv * 100:.1f}%); real daily order counts move 8 to 12%."],
    [table(["Month", "Generated index", "Brain index", "Gap"], seas_rows), table(["Day", "Orders", "x normal Nov day", "Discount % of gross", "AOV", "New share"], bfcm)],
    ["revenue", "seasonality", "weekday"])

sec("aov", "2. AOV and pack mix", "pass",
    [f"AOV is ${net12 / orders12:.2f} on the year against the brain's $73 estimate, with {upo:.2f} units per order (about 1.42 lines: multi packs count as 1 unit each). Multi packs carry {pct(sum(packs[n][1] for n in pk if n > 1) / ts, 0)} of revenue and {pct(sum(packs[n][0] for n in pk if n > 1) / tu, 0)} of units, which fits a brand whose whole page pushes 4 and 6 packs. Category split is socks {pct(cat['socks'], 1)}, slippers {pct(cat['slippers'], 1)}, underwear {pct(cat['underwear'], 1)}, tees {pct(cat['tshirts'], 1)}: 93 / 7 as the brain says. Top SKUs by revenue: {top5}.",
     f"One shape is wrong: AOV falls in November and December (${d['2025-12']['aov']:.2f}) and peaks in January and February (${d['2026-02']['aov']:.2f}). The generator drives this with the discount rate (8.7% of gross in Q4, 5.3% in February). A gifting brand usually sees the opposite: gift packs, bulk gifting and the free shipping line lift Q4 baskets even after deeper discounts. The Q4 AOV should be flat to up 3 to 5%, and BFCM discounts should be deeper than {bfcm[1][3]} of gross (Bombas runs 20% or more sitewide on those days)."],
    [table(["Pack", "Units share", "Revenue share", "Avg net price"], pack_rows)],
    ["aov", "packmix"])

c1012 = cs["2024-10"]["active_by_month"]
sec("repeat", "3. New versus repeat share and the repeat curve by cohort", "flag",
    [f"New customers place {pct(new_share_12, 1)} of orders on the year and the 12 month repeat rate is {man['fields']['repeat_rate']['value']:.0%} as calibrated. The direction by channel is right (paid social {acq_rows[0][4]} new, email {acq_rows[4][4]} new). Two things do not look like a 13 year old sock brand.",
     f"First, the month swing. New share runs from {pct(ns_by_m['2026-02'], 0)} in February to {pct(ns_by_m['2025-12'], 0)} in December, and on Cyber Monday {bfcm[4][5]}. Seasonality is applied to new orders almost alone: returning orders rise only {d['2025-12']['returning_customer_orders'] / d['2025-08']['returning_customer_orders'] - 1:.0%} from August to December while new orders rise {d['2025-12']['new_customer_orders'] / d['2025-08']['new_customer_orders'] - 1:.0%}. Loyal customers gift too, so returning orders should carry most of the same peak. A returning share of about 36% on the year is also at the low end for a mature replenishment brand; 40 to 50% is more typical.",
     f"Second, the curve. Every cohort has the same shape, which is fine for a simulation, but it decays too fast: the October 2024 cohort places {sum(c1012[1:13]) / cs['2024-10']['customers']:.2f} repeat orders per customer in year 1 and only {sum(c1012[13:25]) / cs['2024-10']['customers']:.2f} in year 2 ({sum(c1012[13:25]) / sum(c1012[1:13]):.0%} of year 1). For socks, year 2 is usually 40 to 60% of year 1 because a customer who has bought twice keeps buying. The fixed repeat_continue of 0.45 after every order is the cause. Holiday cohorts (gift buyers) should also repeat a little less than spring cohorts; here Nov and Dec 2024 match June 2025 exactly."],
    [table(["Cohort", "Customers", "Month 1", "Month 2", "Month 6", "Month 12", "Orders / cust yr 1", "Orders / cust yr 2"], coh_rows)],
    ["newrepeat", "cohorts"])

sec("channels", "4. Channel shares against the brain's channel mix", "flag",
    [f"Sales channels land on the brain: site {pct(sales_val[0], 1)}, wholesale {pct(sales_val[1], 1)}, owned retail {pct(sales_val[2], 1)} (from November 2025), marketplaces unavailable as the brain's share is null. The wholesale fixture is exactly 9.0% of orders revenue in every one of the 25 months. Sell in to Nordstrom, Target and DSW does not track site orders day for day: it peaks in August to October as retailers stock for holiday and drops in January. The fixture needs its own month curve. Partner split also reads odd: DSW takes {pct(wp['DSW'] / whol, 0)} of wholesale in its first year, above Athleta ({pct(wp['Athleta'] / whol, 0)}) which has 190 doors since 2020. A first year rollout should ramp.",
     f"Acquisition mix matches the generic fallback (the brain has no acquisition split): paid social {acq_rows[0][1]}, paid search {acq_rows[1][1]}, organic {acq_rows[2][1]}, direct {acq_rows[3][1]}, email and SMS {acq_rows[4][1]}. The Q4 tilt toward paid (paid social 38% of orders in December, 30% in February) is the right direction. AOV by channel is flat within $5, which is plausible; email and direct a little higher is correct."],
    [table(["Sales channel", "Share of revenue", "Brain"], [(a, pct(b, 1) if a != "Marketplaces" else "unavailable", pct(c, 0) if a != "Marketplaces" else "null") for a, b, c in zip(sales_lab, sales_val, sales_ref)]),
     table(["Partner", "Wholesale net sales (12m)", "Share"], [(k, usd(v), pct(v / whol, 0)) for k, v in partner_rows]),
     table(["Acquisition channel", "Share of web orders", "Fallback", "AOV", "New share"], acq_rows)],
    ["saleschannels", "acq"])

sec("funnel", "5. Funnel rates by device and source", "flag",
    [f"Blended conversion is {pct(tx12 / sess12, 2)} of sessions (GA4 captures a fixed 93% of web orders, so {pct(T('web_orders') / sess12, 2)} on orders). The seasonal shape is right: conversion is lowest in November and December when traffic is cold and highest in January and February when the visitors are returning buyers. The device and source split are not in the aggregates and data.sqlite is not in this checkout, so the table below shows what the placeholders imply. Mobile at 70% of sessions converting near 1.5% and desktop near 2.5% is a normal DTC apparel shape.",
     f"The level is the problem: {num(sess12)} sessions in 12 months is {num(sess12 / 12)} a month. Public traffic estimators put bombas.com in the single digit millions of visits a month, so the simulated site has 3 to 5 times the traffic a reader will expect, because the revenue is sourced and the conversion rate is a placeholder. Either the brain needs a traffic anchor or the channel conversion rates need to roughly double (blended near 3%). This matters for every screen that shows sessions or cost per session."],
    [table(["Device", "Share of sessions", "CVR multiplier", "Implied CVR"], dev_rows), table(["Source (placeholder CVR)", "CVR"], src_rows)],
    ["cvr"])

sec("paid", "6. Meta and Google spend, ROAS, CPA and attribution overlap", "flag",
    [f"Paid is {usd(meta12 + goog12)} on the year ({pct((meta12 + goog12) / net12, 0)} of net sales, MER {mer:.1f}x against the finance target of 4.0x). Meta is {pct(meta12 / (meta12 + goog12), 0)} of it. Meta CPA is ${meta12 / T('meta_purchases'):.0f} on the year and Google ${goog12 / T('google_conversions'):.0f}, and the platforms credit themselves with {pct((T('meta_purchases') + T('google_conversions') + T('klaviyo_attributed_orders')) / orders12, 0)} of Shopify orders between Meta, Google and Klaviyo. That is a good, reconcilable gap for the measurement screen: no platform matches orders, the three overlap, and the total stays under 100%.",
     f"The Q4 shape is wrong. Meta spend rises 2.6x from September to December while its CPA jumps from $38 to $49 and the proxy ROAS falls from 1.9x to 1.5x. No brand scales into a falling ROAS for two months; in Q4 a gifting brand's CPM rises but conversion rises more, so CPA holds or improves. The 1.25 Q4 CPA multiplier should be near 1.05 to 1.10, and the Q4 AOV should rise (section 2) so ROAS holds around 2x. Outside Q4 the level is plausible for a brand buying mostly new customers at a $71 first order: paid social is roughly break even on the first order and earns on the repeat (section 9)."],
    [table(["Month", "Meta spend", "Meta CPA", "Meta ROAS", "Google spend", "Google CPA", "Google ROAS", "Attributed / orders"], paid_rows)],
    ["spend", "cpa", "roas", "attribution"])

sec("email", "7. Email flow revenue as a share of orders", "pass",
    [f"Klaviyo claims {pct(kl12, 1)} of orders on the year (flows plus campaigns, with the overlap on direct, organic and paid orders the README describes); email and SMS last click is {pct(em12, 1)}. The gap between the two (Klaviyo claims about 1.7x what last click gives it) is the usual real world gap. The share peaks at 21% in January and February and dips to 14% in December when paid new customers flood in: correct. The aggregates do not split flows from campaigns, so flow share alone was not checked; the flows table has 6,570 rows and campaign_sends 1,736, which is a sane ratio for 9 flows over 2 years and about 2 campaigns a day."],
    [], ["email"])

sec("ops", "8. Returns, chargebacks and tickets per 1,000 orders", "flag",
    [f"Tickets run at {tk12:.0f} per 1,000 orders on the year and {1000 * d['2025-12']['tickets'] / d['2025-12']['orders']:.0f} in December, against a manifest placeholder of 35 (60 in December). The fixture writes about 3x the placeholder; the README's 1,131,568 tickets on 11,061,240 orders is 10.2%. At 10% contact rate the support screen will read as a brand in trouble. Either the placeholder is not what the fixture applies or messages are being counted as tickets.",
     f"Refunds are {pct(rf12, 1)} of net sales, consistent with a 6% return rate refunding one line, which is right for socks. The latest month shows {pct(rf[-1], 1)} because returns lag the order: realistic, but the screen must label it. Chargebacks at 0.4% of orders is high: DTC apparel sits at 0.1 to 0.25%, and 0.4% approaches the level where the card networks start a monitoring program. Checkout abandonment at 0.75 abandoned checkouts per order is 43%, when 65 to 75% is the norm."],
    [table(["Measure", "Generated", "Placeholder", "Real brand range"], ops_rows)],
    ["tickets", "refunds"])

sec("margin", "9. Margin by channel once finance inputs apply", "fail",
    [f"finance_inputs.json cannot be joined to the data. Its 25 landed cost rows use keys like BMB-SK-M-ANK-4; the products table and products_monthly use BB-ANK-4. Overlap is 0 of 21 SKUs, so any margin screen that looks up cost by SKU reads unavailable for every line. The costs themselves are sane where a pair can be matched by eye: core packs at 26% of net price, merino and underwear at 33%, against the generator's 30% of list placeholder.",
     f"Using the placeholder cost share and the per order inputs (pick and pack $2.85 plus $0.35 a unit, packaging $0.62, USPS label about $5.30, 2.4% plus $0.30 payment fee, $4.25 a return), gross margin after fulfilment is {pct(gm_all, 0)} on every online channel (gross margin before fulfilment {pct(1 - cogs_share_net, 0)} versus the 62% target). After charging Meta to paid social and Google to paid search, paid social contributes {pct(mrows[0][3], 1)} on the first order, paid search {pct(mrows[1][3], 1)}, and owned channels around 53%. Blended contribution after all ad spend is {pct(cm_all, 0)}, above the 22% target, and about {pct((cm_all * net12 - fixed) / net12, 0)} after the {usd(fixed)} a year fixed stack (headcount, fixed costs, agency, apps, storage). This is the shape a real DTC sock brand shows: paid social near break even on first order, the business earning on repeat and owned channels. The finance rows start 2025-01-01 while the data starts 2024-09-28, so the first 3 months must read unavailable."],
    [table(["Finance key", "Product SKU", "Landed cost", "Net price", "Cost share"], cogs_rows), table(["Channel", "Orders", "AOV", "GM after fulfilment", "Ad cost / order", "Contribution"], margin_rows)],
    ["margin"])

sec("zero", "10. Zero where it should be unavailable", "flag",
    ["The rule is that a missing or unsupported value reads unavailable, not 0. The aggregates get marketplaces right and get POS wrong."],
    [table(["Place", "Reads", "Should read"], zero_rows, ["l", "l", "l"])], [])

sec("implausible", "11. Anything implausible", "flag",
    ["Rates outside what a brand of this size shows, collected from the sections above, ranked by how much a screen would mislead a reader:",
     f"Sessions of {num(sess12 / 12)} a month (section 5). Tickets at {tk12:.0f} per 1,000 orders (section 8). Chargebacks at 0.4% (section 8). Year on year growth pinned at 29% in every month and daily noise of {june_cv * 100:.1f}% (section 1). Meta scaling 2.6x into a 1.5x ROAS (section 6). AOV falling in Q4 and a 10% BFCM discount (section 2). Returning orders barely lifting in Q4 (section 3). Year 2 repeat at {sum(c1012[13:25]) / sum(c1012[1:13]):.0%} of year 1 (section 3). Wholesale pinned at 9.0% of monthly orders with DSW half of it in year 1 (section 4). Checkout abandonment of 43% (section 8).",
     "Things that looked odd but are fine: GA4 capture at a fixed 93% (a real tag drifts 90 to 95%, add a little noise later); giving units at 31.5M versus the brain's 33.3M a year (wholesale and retail units also donate); shipping revenue at 5.1% of net (half of orders sit under the $75 free shipping line); discounts at 7.3% of gross with 55% of first orders using the 20% code."],
    [], [])

FIXES = [
    ("Join finance inputs to products", "Use one SKU key scheme. Either the generator's `products` list adopts the finance keys (BMB-SK-M-ANK-4 and the 25 SKU list in finance_inputs.json) or finance_inputs is rewritten to the 21 BB- keys. The first is better: the finance list already splits men's and women's, which the product screen will want."),
    ("Ticket rate", "`ticket_rate` 0.035 and `ticket_rate_dec` 0.06 are not what the fixture writes (it lands near 0.10 and 0.13). Find the multiplier in the tickets fixture (messages per ticket, or tickets written per order line) and make the written rate equal the placeholder. Then raise the placeholder to 0.05 base, 0.08 December, which is where a $500M apparel brand sits."),
    ("Traffic level", "Add a brain field `site_sessions_monthly` (assumed, with the open question flagged) and solve `cvr_by_channel` from it, or scale all seven `cvr_by_channel` values by about 1.8 so blended conversion lands near 3% and sessions near 15M a month. Keep `cvr_device_mult` as is."),
    ("Seasonality on returning orders", "Apply the month index to returning orders with a weight (new `returning_seasonality_weight` = 0.7) so December new share lands near 65 to 70% instead of 78%, and Cyber Monday near 80% instead of 93%."),
    ("Repeat curve", "Replace the flat `repeat_continue` 0.45 with a schedule by order number, for example 0.45 after the 1st, 0.60 after the 2nd, 0.70 after the 3rd and later, and recalibrate `repeat_q` so the 12 month repeat stays 0.35. Year 2 orders per customer should reach 40 to 60% of year 1. Add a cohort multiplier of 0.85 on `repeat_q` for November and December first orders."),
    ("Q4 paid efficiency", "`meta_q4_cpa_mult` 1.25 to 1.08. Add a Q4 AOV lift (new `q4_aov_mult` = 1.04, applied to basket size, not price) so proxy ROAS holds near 2x while spend scales."),
    ("BFCM discount depth", "Add `bfcm_discount_pct` = 20 and `bfcm_code_use` = 0.85 for the 5 days from Black Friday to Cyber Monday, so discounts read 18 to 20% of gross on those days instead of 10%."),
    ("Growth and daily noise", "Add `growth_noise_sigma` = 0.04 (a random walk on the monthly growth factor) and `daily_noise_cv` = 0.09 so YoY growth wobbles between about 22 and 36% and daily orders vary 8 to 10% within a month."),
    ("Wholesale fixture shape", "Give `wholesale_sell_in` its own month index (Aug 1.3, Sep 1.4, Oct 1.3, Nov 0.9, Dec 0.6, Jan 0.5, rest near 0.9), keep the year total at 9% of orders revenue, and ramp new partners: DSW and Target at 25% of their run rate in the first quarter, 50% in the second, full from the third. Cap DSW at about 25% of wholesale in year 1."),
    ("POS before the store opened", "Do not write `channels_monthly` rows for `pos` before `owned_retail_open` (2025-11-01), and write `monthly.pos_orders` as null before that date so the screen says no stores yet rather than 0."),
    ("Chargebacks", "`chargeback_rate` 0.004 to 0.0015."),
    ("Checkout abandonment", "`abandoned_per_web_order` 0.75 to 2.0, which gives a 67% abandonment rate."),
    ("Finance inputs start date", "Not a generator change: either set `effective_from` on the 2025-01-01 rows to 2024-09-28 or make the margin screen read unavailable for months with no cost rows. The second is the right behaviour for a real brand, so build that and leave the data alone."),
    ("GA4 capture noise", "Low priority: replace the fixed `ga4_capture` 0.93 with a daily draw between 0.91 and 0.95."),
]

# ================= verdict =================
VERDICT = [
    "Verdict: the levels are right, the shapes are too clean, and one join is broken. The simulated 24 months look like a $500M sock brand in revenue, AOV, pack mix, category split, seasonality, sales channel split, acquisition mix, paid share of sales, attribution overlap, email share and refund rate. They do not look like one in five places: site traffic is 3 to 5x too high for the revenue; support tickets are 3x the placeholder; Q4 is shaped by new customers and discounts alone, so AOV falls and Meta ROAS drops while spend triples; the repeat curve dies in year 2; and growth, daily noise and the wholesale share are pinned to one number. finance_inputs.json cannot be joined to the products at all (0 of 21 SKU keys match), so margin by SKU reads unavailable everywhere until one side changes its keys.",
    "Screens can be built on this data now. The five shape fixes and the key fix are listed at the end as 14 numbered generator changes with the parameter to touch. None needs a paid call.",
]
SUMMARY = [("1. Revenue and seasonality", "pass", "in band, index within 0.03; growth and daily noise too smooth"),
           ("2. AOV and pack mix", "pass", "$73, 85% of revenue from multi packs; Q4 AOV should rise, not fall"),
           ("3. New vs repeat, cohorts", "flag", "36% returning is low; Q4 peak sits on new orders; year 2 repeat at 18% of year 1"),
           ("4. Channel shares", "flag", "site 90 / wholesale 9 / retail 1 as the brain; wholesale pinned at 9.0% monthly, DSW oversize"),
           ("5. Funnel", "flag", "CVR 1.7% is a normal rate, but 27M sessions a month is 3 to 5x real traffic"),
           ("6. Paid and attribution", "flag", "MER 4.1x, 67% of orders claimed by platforms; Q4 ROAS falls to 1.5x while spend scales"),
           ("7. Email", "pass", "Klaviyo claims 17% of orders, last click 10%; right gap and right seasonality"),
           ("8. Returns, chargebacks, tickets", "flag", "refunds 3.5% fine; tickets 103 per 1,000 (placeholder 35); chargebacks 0.4% high"),
           ("9. Margin by channel", "fail", "finance SKU keys do not join; shape by channel is right once a placeholder cost is used"),
           ("10. Zero vs unavailable", "flag", "POS reads 0 for 14 months before the store opened; marketplaces correct"),
           ("11. Implausible rates", "flag", "10 items listed, ranked")]

# ================= REVIEW.md =================
md = ["# Bombas simulated data: review (S2.5)", ""]
md.append(f"Artifact: {ART_URL}" if ART_URL else "Artifact: (published after this file is written; see the line the build adds)")
md += ["", "Simulated data, generator v2, seed 7, scale 1.0, 2024-09-28 to 2026-09-27. Every number here is from `aggregates/*.json`, `manifest.json` and `finance_inputs.json`; nothing is a Bombas result. `data.sqlite` was not in this checkout, so checks that need a row level query (returns, chargebacks, device and source funnels) use the manifest placeholders and say so. Chart sources are in `review/` (`build_review.py`, `charts.py`); the SVGs render in light and dark.", ""]
md += ["## Verdict", ""] + [p + "\n" for p in VERDICT]
tm, th = table(["Check", "Result", "One line"], SUMMARY, ["l", "l", "l"])
md += [tm, ""]
for s in S:
    md += [f"## {s['title']}", "", f"Result: {s['status']}", ""]
    for p in s["paras"]:
        md += [p, ""]
    for name in s["charts"]:
        md += [f"![{name}](review/charts/{name}.svg)", ""]
    for tmd, _ in s["tables"]:
        md += [tmd, ""]
md += ["## Fixes for the generator", "", "Numbered, with the parameter to change. Ordered by how much each one changes what a screen shows.", ""]
for i, (t, body) in enumerate(FIXES, 1):
    md.append(f"{i}. **{t}.** {body}")
md += ["", "## What was not checked", "", "- Return rate, carrier returns and chargebacks by row (need `reversed_orders`).", "- Funnel by device and source by row (need `sessions`).", "- Flow versus campaign split inside the Klaviyo share (need `flows` and `campaign_sends`).", "- Inventory cover and payouts (out of scope for this card).", ""]
open(os.path.join(ROOT, "REVIEW.md"), "w").write("\n".join(md))

# ================= review.html =================
def paras(ps): return "".join(f"<p>{H.escape(p)}</p>" for p in ps)
def chart_html(name): return f'<figure class="chart">{SVG[name]}</figure>'
badge = lambda s: f'<span class="badge {s}">{ {"pass": "looks right", "flag": "needs a fix", "fail": "broken"}[s]}</span>'
sections_html = ""
for s in S:
    body = paras(s["paras"]) + "".join(chart_html(n) for n in s["charts"]) + "".join(f'<div class="tbl">{t[1]}</div>' for t in s["tables"])
    sections_html += f'<section id="{s["id"]}"><h2>{H.escape(s["title"])} {badge(s["status"])}</h2>{body}</section>'
fix_html = "<ol class=\"fixes\">" + "".join(f"<li><strong>{H.escape(t)}.</strong> {H.escape(b)}</li>" for t, b in FIXES) + "</ol>"
sum_html = "<div class=\"tbl\"><table><thead><tr><th>Check</th><th>Result</th><th>One line</th></tr></thead><tbody>" + "".join(f'<tr><td><a href="#{s["id"]}">{H.escape(r[0])}</a></td><td>{badge(r[1])}</td><td>{H.escape(r[2])}</td></tr>' for r, s in zip(SUMMARY, S)) + "</tbody></table></div>"
page = f"""<title>Bombas Data Review</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#f7f6f2;--surface:#fcfcfb;--ink:#161614;--sec:#52514e;--mut:#898781;--line:#e1e0d9;--accent:#1c5cab;--accent-ink:#1c5cab;
--pass:#0ca30c;--flag:#b8790a;--fail:#c53434;--pass-bg:#e6f6e6;--flag-bg:#fbf1dc;--fail-bg:#fbe3e3;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{color-scheme:dark;--bg:#0f0f0e;--surface:#1a1a19;--ink:#f4f3ee;--sec:#c3c2b7;--mut:#898781;--line:#2c2c2a;--accent:#5598e7;--accent-ink:#86b6ef;--pass-bg:#10301a;--flag-bg:#3a2c10;--fail-bg:#3d1a1a;--pass:#3fc94a;--flag:#e0a63b;--fail:#f07070}}}}
:root[data-theme="dark"]{{color-scheme:dark;--bg:#0f0f0e;--surface:#1a1a19;--ink:#f4f3ee;--sec:#c3c2b7;--mut:#898781;--line:#2c2c2a;--accent:#5598e7;--accent-ink:#86b6ef;--pass-bg:#10301a;--flag-bg:#3a2c10;--fail-bg:#3d1a1a;--pass:#3fc94a;--flag:#e0a63b;--fail:#f07070}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55;margin:0;padding-block:32px 64px;padding-inline:16px}}
.wrap{{max-width:860px;margin:0 auto}}
header{{border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:28px}}
.eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}}
h1{{font-size:30px;font-weight:600;letter-spacing:-.01em;margin:6px 0 10px;text-wrap:balance}}
h2{{font-size:19px;font-weight:600;margin:40px 0 12px;text-wrap:balance;display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
p{{max-width:68ch;margin:0 0 12px;color:var(--ink)}}
.meta{{color:var(--sec);font-size:14px;max-width:68ch}}
.verdict{{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);padding:18px 20px;border-radius:6px;margin:0 0 24px}}
.verdict p:last-child{{margin-bottom:0}}
.badge{{font-family:var(--mono);font-size:11px;letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1px solid transparent}}
.badge.pass{{background:var(--pass-bg);color:var(--pass)}}.badge.flag{{background:var(--flag-bg);color:var(--flag)}}.badge.fail{{background:var(--fail-bg);color:var(--fail)}}
.badge::before{{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:currentColor;margin-right:6px;vertical-align:1px}}
.tbl{{overflow-x:auto;margin:12px 0 18px;border:1px solid var(--line);border-radius:6px;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{padding:7px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-weight:500;color:var(--sec);font-size:12px}}
td.r,th.r{{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}}
tr:last-child td{{border-bottom:0}}
figure.chart{{margin:14px 0 18px;background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:6px;overflow-x:auto}}
figure.chart svg{{display:block;width:100%;height:auto;max-width:720px}}
ol.fixes{{padding-left:22px;max-width:72ch}}ol.fixes li{{margin:0 0 12px}}
a{{color:var(--accent-ink)}}
code{{font-family:var(--mono);font-size:.92em}}
.sim{{font-family:var(--mono);font-size:12px;color:var(--mut);margin-top:14px}}
</style>
<div class="wrap">
<header>
<div class="eyebrow">ecomOS · session S2.5 · simulated data</div>
<h1>Bombas Data Review</h1>
<p class="meta">Sanity check of the simulated 24 months (generator v2, seed 7, scale 1.0, 28 Sep 2024 to 27 Sep 2026) against the brain's public profile of Bombas. Every number is simulated; nothing here is a Bombas result. Source: aggregates, manifest and finance inputs only.</p>
</header>
<div class="verdict">{paras(VERDICT)}</div>
{sum_html}
{sections_html}
<section id="fixes"><h2>Fixes for the generator</h2><p>Numbered, with the parameter to change. Ordered by how much each one changes what a screen shows.</p>{fix_html}</section>
<section id="notchecked"><h2>What was not checked</h2><p>Row level checks need data.sqlite, which was not in this checkout: return and chargeback rates, funnel by device and source, and the flow versus campaign split inside the Klaviyo share. Inventory cover and payouts are outside this card.</p></section>
<p class="sim">simulated = 1 on every row · built by review/build_review.py</p>
</div>"""
open(os.path.join(ROOT, "review", "review.html"), "w").write(page)
print("wrote REVIEW.md, review/review.html and", len(SVG), "charts")
