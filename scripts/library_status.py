"""Generate a concise local progress and spending report without provider calls."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    directory=ROOT/'data/library-v3'
    progress=json.loads((directory/'progress.json').read_text(encoding='utf-8'))
    db=sqlite3.connect(ROOT/'data/spend.sqlite')
    actual,pending=db.execute('SELECT COALESCE(SUM(actual),0),COALESCE(SUM(CASE WHEN actual IS NULL THEN reserved ELSE 0 END),0) FROM spend').fetchone()
    db.close()
    lines=['# Ecommerce intelligence progress','', 'Snapshot: '+datetime.now(timezone.utc).isoformat(),'',
           f"Generated cards: **{progress['cards']}**.",
           f'Conservatively estimated settled API usage: **${actual/1e6:.3f}**. Pending/uncertain reservations: **${pending/1e6:.3f}**.',
           'These are pipeline ledger estimates, not provider invoices. The overall USD 200 ceiling includes earlier work; the current working stop remains USD 160.','',
           '| Folder | Sections completed | Cards |','|---|---:|---:|']
    for row in progress['folders']:
        lines.append(f"| {row['folder'].strip('/')} | {row['completed']}/{row['sections']} | {row['cards']} |")
    lines += ['', '## What is available','',
              '- Text-only cards in `data/library-v3/cards.json` and per-folder Markdown in `data/library-v3/markdown/`.',
              '- Keyword plus semantic search, with complete cards packed to a measured token budget.',
              '- Folder completion is listed above. The next stage after ingestion is task-based retrieval and agent integration.',
              '- Three same-model CRO comparisons completed. They demonstrate retrieval and context use, not proven superiority or business uplift.',
              '- Sample corrections clarified lead-generation applicability and source-specific testing thresholds. The revised low-traffic answer retained the heuristic caveat.',
              '- Hosting, a production agent service and GitHub push are not completed.',
              '', 'Use `python scripts/library_status.py` to refresh this report. A folder is fully searchable semantically after its vector refresh finishes.']
    (ROOT/'LIBRARY_PROGRESS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'cards':progress['cards'],'settled_estimate_usd':actual/1e6,'reserved_usd':pending/1e6}))


if __name__=='__main__':main()
