"""Validate inspiration references against app/inspiration/reference.schema.json.

A small validator for the subset of JSON Schema the file uses (type, required, enum,
properties, additionalProperties, items, pattern, minLength, maxLength, minimum, maximum),
so the check runs with no extra package.

CLI: python3 -m app.inspiration.validate app/inspiration/bombas/creative.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "reference.schema.json"
_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def _is(value, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[name])


def _check(value, schema: dict, path: str, errors: list[str]) -> None:
    types = schema.get("type")
    if types is not None:
        types = [types] if isinstance(types, str) else types
        if not any(_is(value, t) for t in types):
            errors.append(f"{path}: expected {'/'.join(types)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: {len(value)} characters, max {schema['maxLength']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
    if _is(value, "number"):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} above {schema['maximum']}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        for key, sub in value.items():
            if key in props:
                _check(sub, props[key], f"{path}.{key}", errors)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected key {key}")
    if isinstance(value, list) and "items" in schema:
        for i, sub in enumerate(value):
            _check(sub, schema["items"], f"{path}[{i}]", errors)


def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def errors(reference: dict, sch: dict | None = None) -> list[str]:
    out: list[str] = []
    _check(reference, sch or schema(), reference.get("id", "$") if isinstance(reference, dict) else "$", out)
    if isinstance(reference, dict):
        media, origin = reference.get("media") or {}, reference.get("origin") or {}
        if origin.get("role") == "own" and media.get("rights") != "own_brand":
            out.append(f"{reference.get('id')}: own reference must carry rights own_brand")
        if origin.get("role") in ("competitor", "leader") and media.get("rights") != "reference_only":
            out.append(f"{reference.get('id')}: {origin.get('role')} reference must carry rights reference_only")
    return out


def validate_file(path: Path | str) -> list[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    sch = schema()
    out: list[str] = []
    for ref in data:
        out += errors(ref, sch)
    return out


def main(argv: list[str] | None = None) -> int:
    paths = argv if argv is not None else sys.argv[1:]
    bad = 0
    for p in paths:
        errs = validate_file(p)
        bad += len(errs)
        print(f"{p}: {'ok' if not errs else f'{len(errs)} errors'}")
        for e in errs[:20]:
            print("  " + e)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
