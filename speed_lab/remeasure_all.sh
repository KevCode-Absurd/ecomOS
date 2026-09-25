#!/bin/bash
# Re-measure the baseline and every variant on the current replay server, 3 runs each, sequentially.
cd /home/user/ecomOS
python3 speed_lab/measure.py baseline --runs 3 | tail -1
for v in $(ls speed_lab/variants | sort); do
  python3 speed_lab/measure.py "$v" --variant "$v" --runs 3 | tail -1
done
