"""Speed lab: an offline mirror of one page, a replay server, a measurement harness, and variants.

record.py  captures every response of a page load into store/.
serve.py   replays the store over HTTPS on 443 for any host (Chromium maps all hosts to 127.0.0.1).
measure.py loads the page through the replay server on a throttled mobile profile and writes metrics.
lab.py     helpers for building a variant: read a stored response, write an override.
"""
