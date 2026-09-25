"""4-week test budget and thresholds, computed from baselines.json and account_totals.json.
Run from the repo root: python3 reviews/copy-test/blind/raw-2/test_budget.py
"""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
b = json.load(open(os.path.join(ROOT, "baselines.json")))
t = json.load(open(os.path.join(ROOT, "account_totals.json")))

monthly = t["current_monthly_spend"]["mean_of_last_3_full_months"]      # 1,111,950.87
last30 = t["current_monthly_spend"]["last_30_days_spend"]                # 1,152,746.61
base = round(monthly, -3)                                                 # rounded base for the plan
TEST_SHARE = 0.25                                                         # share of monthly spend the test takes
test_total = base * TEST_SHARE
split = {"new_buyers": 0.60, "site_visitors_and_cart": 0.25, "past_customers": 0.15}
out = {
    "monthly_spend_base_inr": base,
    "monthly_base_source": "mean of Jun, Jul, Aug 2026 spend (%.2f), rounded to the nearest 1,000; last 30 days = %.2f" % (monthly, last30),
    "test_share_of_monthly_spend": TEST_SHARE,
    "test_budget_4_weeks_inr": test_total,
    "test_budget_per_day_inr": round(test_total / 28, 2),
    "objectives": {},
}
for k, s in split.items():
    amt = test_total * s
    out["objectives"][k] = {
        "share_of_test": s,
        "share_of_monthly_spend": round(TEST_SHARE * s, 4),
        "budget_4_weeks_inr": round(amt, 2),
        "per_ad_set_4_weeks_inr": round(amt / 4, 2),
        "per_ad_set_per_day_inr": round(amt / 4 / 28, 2),
    }
# past-customer cap from the 24-DEP frequency formula: customers x (CPM / 1000) x frequency
cpm_warm = b["bof_mof_12m"]["cpm"]
for customers in (10000, 20000, 30000):
    out.setdefault("past_customer_cap_by_customer_count", {})[str(customers)] = {
        "cpm_used": cpm_warm,
        "frequency_per_month": 6,
        "monthly_budget_inr": round(customers * cpm_warm / 1000 * 6, 2),
    }
# thresholds
cold_cpa = b["tof_evergreen_90d"]["cpa"]
cold_roas = b["tof_evergreen_90d"]["roas"]
cold_roas_12m = b["tof_evergreen_12m"]["roas"]
warm_cpa = b["bof_mof_90d"]["cpa"]
warm_roas = b["bof_mof_90d"]["roas"]
acct_cpa = b["account_90d"]["cpa"]
acct_roas = b["account_90d"]["roas"]
out["thresholds"] = {
    "cold_new_buyers": {
        "baseline": "TOF evergreen ads, last 90 days: CPA %.0f, ROAS %.2f (12 months: ROAS %.2f)" % (cold_cpa, cold_roas, cold_roas_12m),
        "read_spend_per_ad_set_inr": round(3 * cold_cpa, -3),
        "keep_purchases_at_read": "3 or more",
        "yellow_purchases_at_read": "2 (extend by 1 more CPA of spend, about %.0f)" % cold_cpa,
        "kill_purchases_at_read": "0 or 1",
        "scale_roas": round(cold_roas, 2),
        "keep_roas": round(cold_roas_12m, 2),
    },
    "warm_site_visitors": {
        "baseline": "BOF and MOF ad sets, last 90 days: CPA %.0f, ROAS %.2f" % (warm_cpa, warm_roas),
        "read_spend_per_ad_set_inr": round(3 * warm_cpa, -3),
        "keep_purchases_at_read": "3 or more",
        "yellow_purchases_at_read": "2",
        "kill_purchases_at_read": "0 or 1",
        "scale_roas": round(warm_roas, 2),
    },
    "past_customers": {
        "baseline": "no dedicated past-customer campaign exists; placeholder is the account 90-day CPA %.0f and ROAS %.2f, to be replaced by store-side repeat orders" % (acct_cpa, acct_roas),
        "read_spend_per_ad_set_inr": 10000,
        "frequency_cap_per_30_days": 7,
    },
}
json.dump(out, open(os.path.join(ROOT, "budget_split.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
