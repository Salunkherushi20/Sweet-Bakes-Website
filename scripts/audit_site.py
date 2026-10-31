#!/usr/bin/env python3
"""Dependency-free static checks for the Sweet Bakes GitHub Pages site."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "treats.html", "our-story.html", "custom-cake.html", "404.html")
errors = []
warnings = []

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.images = []
        self.title_count = 0
        self.description_count = 0
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs)
            if "alt" not in attrs:
                errors.append(f"Image missing alt attribute in current page: {attrs.get('src', '(no src)')}")
        if tag == "title":
            self.title_count += 1
            self.in_title = True
        if tag == "meta" and attrs.get("name", "").lower() == "description":
            self.description_count += 1
            if not attrs.get("content", "").strip():
                errors.append("Empty meta description")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data

parsed = {}
for name in PAGES:
    path = ROOT / name
    if not path.is_file():
        errors.append(f"Required page missing: {name}")
        continue
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parsed[name] = parser
    if parser.title_count != 1 or not parser.title_text.strip():
        errors.append(f"{name}: expected exactly one non-empty <title>")
    if parser.description_count != 1:
        errors.append(f"{name}: expected exactly one meta description")
    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        errors.append(f"{name}: duplicate IDs: {', '.join(duplicates)}")

for name, parser in parsed.items():
    for href in parser.links:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or href.startswith("//"):
            continue
        target_name = unquote(parts.path)
        if not target_name:
            target = ROOT / name
        else:
            target = (ROOT / target_name).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{name}: link escapes site root: {href}")
            continue
        if not target.is_file():
            errors.append(f"{name}: broken local link: {href}")
            continue
        if parts.fragment:
            fragment = unquote(parts.fragment)
            target_page = target.name
            target_parser = parsed.get(target_page)
            if target_parser is None and target.suffix.lower() == ".html":
                target_parser = PageParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
            if target_parser and fragment not in target_parser.ids:
                errors.append(f"{name}: missing fragment target: {href}")

if "custom-cake.html" in parsed:
    content = (ROOT / "custom-cake.html").read_text(encoding="utf-8")
    for required in ('id="enquiryForm"', 'id="enquiryDraft"', 'id="formStatus"', 'id="copyEnquiry"'):
        if required not in content:
            errors.append(f"custom-cake.html: missing required enquiry control {required}")
    if "this site does not transmit it" not in content:
        warnings.append("Enquiry page should clearly state that the form does not send data.")

if errors:
    print("Static site audit FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"Static site audit passed: {len(parsed)} HTML pages checked; local links, fragments, titles, descriptions, IDs, and image alt attributes are valid.")
for warning in warnings:
    print(f"Warning: {warning}")
