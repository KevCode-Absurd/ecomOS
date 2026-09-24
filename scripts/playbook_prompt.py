"""Print the pass 1 agent prompt for one source. Usage: python3 scripts/playbook_prompt.py FOLDER NN"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
man=json.load(open(ROOT/'playbooks/v2/_source_manifest.json'))
folder,nn=sys.argv[1],sys.argv[2]
s=[x for x in man[folder] if x['nn']==nn][0]
fdir=folder.strip('/')
print(f"""You write playbook source distillations for ecomOS in /home/user/ecomOS. Read `playbooks/v2/TEMPLATE.md` first and follow the Pass 1 format and writing rules exactly.

Task: write 1 mini playbook for this source in folder {folder}:
- source_id {s['id']}  "{s['name']}" ({s['words']:,} words, {s['cards']} cards)

How: run `python3 scripts/export_source.py {s['id']}` to get the full source text and all its cards. Read the whole text. Write the mini playbook to `playbooks/v2/{fdir}/sources/{s['nn']}-{s['slug']}.md` (create directories as needed). Be exhaustive: every principle, procedure, number, tool and check the source gives. The folder playbook will be built only from these mini playbooks, so anything left out is lost. Cite card ids (first 12 characters). Tag platform steps `[verify UI]`, brand-dependent numbers `[needs brand data: what]`, and claims to re-check `[web check: what]`. Do not invent anything the source does not say. Do not edit any other file. No paid or external calls. Final report under 120 words: file path, word count, 2 lines on what the source is strongest and weakest at, and any conflict you noticed with common ecommerce advice.""")
