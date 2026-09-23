"""Deterministic extraction, preserving block locators and raw source identity."""
import hashlib
import io
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_document(raw: bytes, name: str):
    """Supports DOCX and UTF-8 plain text/Markdown. Unsupported formats fail closed.

    Does not infer original-vs-generated origin or repair legacy YAML. Both require
    a separate review stage. DOCX media inventory is surfaced, not discarded.
    """
    lower = name.lower()
    if lower.endswith((".txt", ".md")):
        text = raw.decode("utf-8-sig")
        return [{"locator": f"paragraph:{i}", "text": p, "origin": "unknown"}
                for i, p in enumerate(re.split(r"\n\s*\n", text), 1) if p.strip()], []
    if not lower.endswith(".docx"):
        raise ValueError("Unsupported format; route to a dedicated parser")
    with ZipFile(io.BytesIO(raw)) as z:
        if sum(i.file_size for i in z.infolist()) > 100_000_000:
            raise ValueError("Expanded DOCX exceeds the 100 MB local parser limit")
        xml = z.read("word/document.xml")
        if b"<!DOCTYPE" in xml or b"<!ENTITY" in xml:
            raise ValueError("Document type/entity declarations are not accepted")
        root = ET.fromstring(xml)
        body = root.find("w:body", NS)
        if body is None:
            raise ValueError("DOCX body missing")
        blocks = []
        for i, node in enumerate(body, 1):
            if node.tag == f"{{{NS['w']}}}p":
                text = "".join(node.itertext()) if not node.findall(".//w:t", NS) else "".join(
                    n.text or "" for n in node.findall(".//w:t", NS))
                if text.strip():
                    blocks.append({"locator": f"body:{i}/paragraph", "text": text, "origin": "unknown"})
            elif node.tag == f"{{{NS['w']}}}tbl":
                rows = [["".join(t.text or "" for t in cell.findall(".//w:t", NS))
                         for cell in row.findall("w:tc", NS)] for row in node.findall("w:tr", NS)]
                blocks.append({"locator": f"body:{i}/table", "text": "\n".join(" | ".join(r) for r in rows),
                               "rows": rows, "origin": "unknown"})
        media = [i.filename for i in z.infolist() if i.filename.startswith("word/media/")]
        return blocks, media

