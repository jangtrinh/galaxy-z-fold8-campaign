#!/usr/bin/env python3
"""Deterministic, stdlib-only checks for the campaign artifact."""
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
REQUIRED_ASSETS = [
    "assets/hero-layers/hero-background-layer.png",
    "assets/hero-layers/hero-product-cutout.png",
]
TRANSPARENT_ASSETS = [
    "assets/hero-layers/hero-product-cutout.png",
    *[
        f"assets/section-cutouts/{name}-cutout.png"
        for name in (
            "02-folded-cover-wide", "03-hinge-transition-wide",
            "04-dynamic-angle-wide", "05-static-rest-wide",
            "06-commerce-open-wide", "07-system-exploded-wide",
            "08-finale-macro-wide", "09-content-shape-wide",
        )
    ],
]

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.refs = []
        self.viewport = False
        self.images_without_alt = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = bool(attrs.get("content"))
        if tag in {"img", "script"} and attrs.get("src"):
            self.refs.append(attrs["src"])
        if tag == "link" and attrs.get("href"):
            self.refs.append(attrs["href"])
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src", "<inline>"))

def main():
    errors = []
    for relative in ["index.html", *REQUIRED_ASSETS]:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in TRANSPARENT_ASSETS:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing transparent asset: {relative}")
            continue
        header = path.read_bytes()[:26]
        if len(header) < 26 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
            errors.append(f"invalid PNG: {relative}")
            continue
        width, height = struct.unpack(">II", header[16:24])
        color_type = header[25]
        if (width, height) != (1672, 941):
            errors.append(f"wrong transparent asset size: {relative} ({width}x{height})")
        if color_type != 6:
            errors.append(f"transparent asset is not RGBA PNG: {relative}")
    if not PAGE.is_file():
        return report(errors)
    source = PAGE.read_text(encoding="utf-8")
    parser = AuditParser()
    parser.feed(source)
    if parser.tags.count("h1") != 1:
        errors.append(f"expected one h1, found {parser.tags.count('h1')}")
    for tag in ("main", "nav", "footer"):
        if tag not in parser.tags:
            errors.append(f"missing semantic <{tag}>")
    if not parser.viewport:
        errors.append("missing viewport meta")
    if "prefers-reduced-motion" not in source:
        errors.append("missing reduced-motion CSS")
    if source.count("data-depth") < 7:
        errors.append("depth layering is not applied across the required sections")
    for token in ("--depth-fg-scroll", "--depth-bg-scroll", "pointerleave"):
        if token not in source:
            errors.append(f"missing depth behavior: {token}")
    if parser.images_without_alt:
        errors.append("images without alt: " + ", ".join(parser.images_without_alt))
    if re.search(r"(?:src|href)=[\"'](?:file:|/(?!/)|[A-Za-z]:\\)", source):
        errors.append("absolute local path found")
    for ref in parser.refs:
        parsed = urlparse(ref)
        if parsed.scheme or ref.startswith("//") or ref.startswith("#"):
            continue
        target = (ROOT / parsed.path).resolve()
        if ROOT not in target.parents and target != ROOT:
            errors.append(f"relative reference escapes project: {ref}")
        elif not target.is_file():
            errors.append(f"missing relative reference: {ref}")
    placeholders = ("lorem ipsum", "todo", "tbd", "replace me", "placeholder")
    lowered = source.lower()
    for token in placeholders:
        if token in lowered:
            errors.append(f"placeholder text found: {token}")
    report(errors)

def report(errors):
    if errors:
        print("VERIFY FAILED")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("VERIFY PASSED: structure, assets, paths, semantics, viewport, motion, and content")

if __name__ == "__main__":
    main()
