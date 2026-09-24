"""Package only allowlisted handoff/report/playbook artifacts; no credentials or raw data."""
import json,zipfile,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 files=set(ROOT.glob('*.md'))
 files.add(ROOT/'HANDOFF_PROJECT_SNAPSHOT.json')
 for name in ('AD_COPY_PLAYBOOK_COMPARISON.html','AD_COPY_OPTIMISATION_COMPARISON.html','AD_COPY_BRIDGE_COMPARISON.html','AD_COPY_TASK_FIRST_COMPARISON.html','OWNER_BENCHMARK_COMPARISON.html'):
  files.add(ROOT/name)
 for name in ('README.md','VALIDATION.md','OPERATING_CONTRACT.md','feedback-template.json','v1/INDEX.md','v1/BUILD_REPORT.json','v1/catalog.json'):
  p=ROOT/'playbooks'/name
  if p.exists():files.add(p)
 for version in ('ad-copy-v1.1','ad-copy-v1.2','ad-copy-v1.3','ad-copy-v1.4'):
  base=ROOT/'playbooks'/version
  files.update(base.glob('*.md'))
  for name in ('catalog.json','ad-copy-deployment/playbook.json'):
   if (base/name).exists():files.add(base/name)
 files.update((ROOT/'playbooks/v1').glob('*/README.md'))
 index=['# Handoff bundle contents','',
  'Read CLAUDE_START_HERE.md, then CLAUDE_HANDOFF.md. The snapshot is a dated local audit; historical reports can be superseded. This package contains documentation, selected self-contained comparisons and the ad-copy playbook definitions. It is not a runnable checkout or a full library backup.',
  '', 'Excluded: .env, secrets, service-account files, raw source documents, the 7,611-card database, vectors/index databases, complete provider payload archives, local runtimes, Meta captures/customer datasets and image assets. Some reports contain business facts needed to explain the tests; share this bundle privately.',
  '', 'All other paths in the handoff refer to the actual project; not every linked report/image/script is included in this documentation package.','', '| File | Bytes |','|---|---:|']
 for p in sorted(files):
  if p.name in ('HANDOFF_FILE_INDEX.md',):continue
  rel=p.relative_to(ROOT).as_posix();index.append(f'| [{rel}]({rel}) | {p.stat().st_size:,} |')
 idx=ROOT/'HANDOFF_FILE_INDEX.md';idx.write_text('\n'.join(index)+'\n',encoding='utf-8');files.add(idx)
 # Stop on recognizable credential material; print only filenames, never matched strings.
 pattern=re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----|\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}|\bAIza[A-Za-z0-9_-]{30,}')
 bad=[]
 for p in files:
  rel=p.relative_to(ROOT)
  if rel.parts[0] in ('data','secrets','.git') or p.name.startswith('.env'):raise ValueError('Disallowed archive path')
  if pattern.search(p.read_text(encoding='utf-8')):bad.append(rel.as_posix())
 if bad:raise ValueError('Credential-pattern review needed for files: '+', '.join(bad))
 dest=ROOT/'CLAUDE_HANDOFF_BUNDLE.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  assert {'CLAUDE_START_HERE.md','CLAUDE_HANDOFF.md','HANDOFF_PROJECT_SNAPSHOT.json'}.issubset(z.namelist())
 print(json.dumps({'archive':dest.name,'files':len(files),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'credential_pattern_scan':'passed (heuristic; allowlist is primary exclusion control)','handoff_words':len((ROOT/'CLAUDE_HANDOFF.md').read_text(encoding='utf-8').split())}))

if __name__=='__main__':main()
