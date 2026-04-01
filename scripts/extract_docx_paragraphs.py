#!/usr/bin/env python3
"""Extract non-empty paragraphs from a DOCX file for rule review."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", help="Path to the .docx file")
    parser.add_argument("--grep", help="Only print paragraphs matching this regex")
    parser.add_argument("--limit", type=int, help="Stop after N matched paragraphs")
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Print only paragraph text without numeric indices",
    )
    return parser.parse_args()


def extract_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        with zf.open("word/document.xml") as fh:
            tree = ET.parse(fh)
    paragraphs: list[str] = []
    for para in tree.findall(f".//{W_NS}body/{W_NS}p"):
        texts = [node.text or "" for node in para.iterfind(f".//{W_NS}t")]
        text = "".join(texts).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def main() -> int:
    args = parse_args()
    docx_path = Path(args.docx).expanduser()
    if not docx_path.is_file():
        print(f"[ERROR] File not found: {docx_path}", file=sys.stderr)
        return 1
    if docx_path.suffix.lower() != ".docx":
        print(f"[ERROR] Expected a .docx file: {docx_path}", file=sys.stderr)
        return 1

    pattern = re.compile(args.grep) if args.grep else None
    matched = 0
    for index, paragraph in enumerate(extract_paragraphs(docx_path)):
        if pattern and not pattern.search(paragraph):
            continue
        matched += 1
        if args.no_index:
            print(paragraph)
        else:
            print(f"[{index}] {paragraph}")
        if args.limit is not None and matched >= args.limit:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
