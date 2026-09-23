import argparse
import json
from pathlib import Path
from .costs import estimate
from .store import Store
from .context import pack


def main():
    parser = argparse.ArgumentParser(description="Offline ecommerce intelligence foundations")
    sub = parser.add_subparsers(dest="command", required=True)
    costs = sub.add_parser("estimate")
    costs.add_argument("--sources", type=int, default=350)
    costs.add_argument("--raw-tokens", type=int, default=30000)
    costs.add_argument("--batch", action="store_true")
    costs.add_argument("--extraction-model", default="claude-sonnet-5")
    costs.add_argument("--output-scale", type=float, default=1)
    costs.add_argument("--verification-scale", type=float, default=1)
    ingest = sub.add_parser("ingest-local")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--source-id", required=True)
    ingest.add_argument("--scope", required=True)
    ingest.add_argument("--data-dir", default="data")
    inventory = sub.add_parser("manifest")
    inventory.add_argument("path", type=Path)
    context = sub.add_parser("context")
    context.add_argument("query")
    context.add_argument("--scopes", nargs="+", required=True)
    context.add_argument("--facts", type=Path, required=True)
    context.add_argument("--budget", type=int, default=6000)
    context.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    if args.command == "estimate":
        result = estimate(args.sources, args.raw_tokens, args.batch, args.extraction_model,
                          output_scale=args.output_scale, verification_scale=args.verification_scale)
    elif args.command == "manifest":
        rows = json.loads(args.path.read_text(encoding="utf-8"))
        result = {"folders":len(rows), "sources":sum(len(x["sources"]) for x in rows),
                  "counts":{x["folder"]:len(x["sources"]) for x in rows}}
    else:
        store = Store(args.data_dir)
        try:
            if args.command == "ingest-local":
                result = store.ingest(args.source_id, args.scope, args.path.read_bytes(), args.path.name)
            else:
                result = pack(store.eligible_cards(set(args.scopes)), args.query,
                              json.loads(args.facts.read_text(encoding="utf-8")), args.budget)
        finally:
            store.close()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

