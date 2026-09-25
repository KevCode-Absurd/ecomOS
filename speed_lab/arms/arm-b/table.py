"""Build the results table for arm B from speed_lab/results/*.json (medians of 3 runs) and both fidelity checks."""
import json, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LABELS = ["baseline"] + [f"arm-b-f{i:02d}" for i in range(1, 9)]


def fid(label):
    p = os.path.join(ROOT, "results", label + ".json")
    off = subprocess.run([sys.executable, os.path.join(ROOT, "check_fidelity.py"), p], capture_output=True, text=True).stdout
    nrm = subprocess.run([sys.executable, os.path.join(ROOT, "arms", "arm-b", "check_norm.py"), p], capture_output=True, text=True).stdout
    off_lines = [l for l in off.splitlines()[1:]]
    # official failures other than the 501 beacon-payload artifact
    other = [l for l in off_lines if "Unsupported method" not in l]
    return ("PASS" if off.startswith("PASS") else "FAIL"), other, nrm.strip().splitlines()[-1].split()[-1]


rows = []
for L in LABELS:
    m = json.load(open(os.path.join(ROOT, "results", L + ".json")))["median"]
    o, other, n = fid(L)
    rows.append((L, m, o, other, n))
print("| Variant | LCP ms | FCP ms | DCL ms | Load ms | TBT ms | Wire KB | 1st-party KB | 3rd-party KB | Requests | Official check | Other official failures | Normalized check (3 runs) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for L, m, o, other, n in rows:
    print(f"| {L} | {m['lcp_ms']:.0f} | {m['fcp_ms']:.0f} | {m['dcl_ms']:.0f} | {m['load_ms']:.0f} | {m['tbt_est_ms']:.0f} | {m['wire_bytes']/1024:.0f} | {m['first_party_bytes']/1024:.0f} | {m['third_party_bytes']/1024:.0f} | {m['requests_served']:.0f} | {o} | {'; '.join(other) or 'none'} | {n} |")
b = rows[0][1]; f = rows[-1][1]
print()
for k in ["lcp_ms", "fcp_ms", "dcl_ms", "load_ms", "tbt_est_ms", "wire_bytes", "first_party_bytes", "third_party_bytes", "requests_served"]:
    print(f"{k}: {b[k]:.0f} -> {f[k]:.0f}  change {f[k]-b[k]:+.0f} ({(f[k]-b[k])/b[k]*100:+.1f}%)")
print()
prev = rows[0][1]
for L, m, *_ in rows[1:]:
    print(L, {k: round(m[k] - prev[k]) for k in ["lcp_ms", "fcp_ms", "dcl_ms", "load_ms", "tbt_est_ms", "wire_bytes", "third_party_bytes"]})
    prev = m
