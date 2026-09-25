# Gehna speed lab: verdict, 25 Sep 2026

Two agents, same offline mirror of the Gehna homepage, same harness, same web budget. Arm A: general knowledge. Arm B: plus the idea bank and card library. Each ranked the top 10 limiters and applied fixes one at a time, 3 measured runs per step, fidelity-checked. Page: reviews/speed-lab/gehna-speed-lab.html. Data and code: speed_lab/.

| | Baseline | Arm A final (f09) | Arm B final (f08) |
|---|---|---|---|
| Load | 15.4 s | 5.2 s (-66%) | 5.8 s (-62%) |
| LCP | 1.70 s | 1.22 s (-28%) | 1.30 s (-24%) |
| First paint | 740 ms | 528 ms (-29%) | 744 ms (0%) |
| Blocking time | 2.36 s | 2.47 s | 2.49 s |
| Wire bytes | 4.34 MB | 1.98 MB (-54%) | 2.09 MB (-52%) |
| Third-party bytes | 1.06 MB | 0.93 MB | 0.93 MB |
| Fidelity | | PASS all 8 steps | PASS 7 of 8; f01 alone fails, ships with f02 |

Result: Arm A slightly ahead. Both found the same 7 core fixes; Arm A added inlining the render-blocking CSS and ordered Rocket Loader before the fonts. The idea bank matched 4 of Arm B's 8 fixes, all of which its own audit had also found; Arm B challenged 6 bank ideas as not applicable here. On this page the bank was confirmation, not discovery.

Harness notes: absolute numbers are kinder than the live site (localhost, HTTP/1.1, no server time); deltas are fair. The replay server initially did not read POST bodies, which produced random console errors; it was fixed and every variant was re-measured on the corrected server. First-pass numbers are archived in speed_lab/results/first-pass/.
