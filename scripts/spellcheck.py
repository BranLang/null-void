#!/usr/bin/env python3
"""
NULL VOID — Slovak Spell & Grammar Check
Uses the free LanguageTool public API to check Slovak prose in draft files.

Strips inline comments and markdown formatting before checking.
Supports a local whitelist of world-specific proper nouns.

Usage:
  python scripts/spellcheck.py                          # all heist-arc drafts
  python scripts/spellcheck.py --arc yera               # different arc
  python scripts/spellcheck.py path/to/file.md          # single file
  python scripts/spellcheck.py --ignore-types TYPOS     # skip typo-only errors
  python scripts/spellcheck.py --only-types GRAMMAR     # only grammar errors
"""

import re
import sys
import io
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── LanguageTool config ──────────────────────────────────────────────────────
LT_API_URL = "https://api.languagetool.org/v2/check"
LT_LANGUAGE = "sk"
LT_MAX_CHARS = 18000   # public API limit is ~20k, leave buffer
LT_RATE_LIMIT_SLEEP = 3  # seconds between requests (20 req/min limit)

# ─── Inline comment pattern (same as export-clean-drafts.py) ─────────────────
COMMENT_PATTERN = re.compile(
    r'\s*\['
    r'(?:'
    r'→[^\]]*'           # [→ ...]
    r'|NOTE:\s*[^\]]*'   # [NOTE: ...]
    r'|TODO:\s*[^\]]*'   # [TODO: ...]
    r'|FIXME:\s*[^\]]*'  # [FIXME: ...]
    r')'
    r'\]\s*'
)

# ─── Markdown stripping ───────────────────────────────────────────────────────
MARKDOWN_PATTERNS = [
    re.compile(r'^#{1,6}\s+', re.MULTILINE),   # headers
    re.compile(r'\*{1,3}([^*]+)\*{1,3}'),      # bold/italic → keep text
    re.compile(r'_{1,3}([^_]+)_{1,3}'),        # underline variants
    re.compile(r'`[^`]+`'),                     # inline code → remove
    re.compile(r'^```.*?^```', re.MULTILINE | re.DOTALL),  # code blocks
    re.compile(r'^\s*[-*+]\s+', re.MULTILINE), # list items
    re.compile(r'^\s*>\s+', re.MULTILINE),     # blockquotes
    re.compile(r'\[([^\]]+)\]\([^)]+\)'),      # links → keep label
]

# ─── Whitelist: world-specific words that are NOT errors ─────────────────────
# Add more here as needed. Case-insensitive matching.
WHITELIST = {
    # Characters
    "maks", "kaito", "elania", "yera", "tami", "otami",
    "spira", "varietas", "archanjel", "archanjeli",
    "wraith", "wraithy",
    # Places
    "nevriss", "nyau", "karakuri", "airen",
    "šoraven", "atra",
    # Factions / groups
    "grawská", "grawský", "grawskej", "graw",
    # Tech / magic
    "nanoboty", "nanobot", "nanobotov", "nanobotmi",
    "gen", "exorcizmus", "korditu", "korditom", "kordit",
    # Religion / culture
    "vševedúcej", "vševedúca", "kňažiek", "kňažien",
    # Japanese elements
    "kaze", "mizu", "teru", "tsuchi",
    # Other world terms
    "dieselpunk", "grimdark", "kotvísk",
    # Slovak variants the API doesn't know
    "etanolovým", "zahryzú", "nakládači", "kotviacimi",
}

# Error type → friendly label
TYPE_LABELS = {
    "misspelling": "PRAVOPIS",
    "grammar":     "GRAMATIKA",
    "style":       "ŠTÝL",
    "other":       "INÉ",
    "hint":        "TIP",
    "typographical": "TYPOGRAFIA",
    "uncategorized": "INÉ",
}


def strip_comments(text: str) -> str:
    """Remove inline author comments."""
    def _replace(match):
        s = match.string
        start, end = match.start(), match.end()
        if start > 0 and end < len(s) and s[start-1] not in ' \t\n' and s[end] not in ' \t\n':
            return ' '
        return ''
    return COMMENT_PATTERN.sub(_replace, text)


def strip_markdown(text: str) -> str:
    """Simplify markdown so LanguageTool sees clean prose."""
    for pat in MARKDOWN_PATTERNS:
        if pat.groups:
            text = pat.sub(r'\1', text)
        else:
            text = pat.sub('', text)
    # Collapse multiple spaces / clean up
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text


def prepare_text(raw: str) -> str:
    text = strip_comments(raw)
    text = strip_markdown(text)
    return text


def chunk_text(text: str, max_chars: int = LT_MAX_CHARS) -> list[str]:
    """Split text on paragraph boundaries to stay under API limit."""
    paragraphs = text.split('\n\n')
    chunks, current = [], []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) + 2 > max_chars and current:
            chunks.append('\n\n'.join(current))
            current, current_len = [], 0
        current.append(para)
        current_len += len(para) + 2

    if current:
        chunks.append('\n\n'.join(current))
    return chunks


def is_whitelisted(word: str) -> bool:
    return word.lower().strip('.,!?;:"\'-()') in WHITELIST


def call_languagetool(text: str) -> list[dict]:
    """POST text to LanguageTool API, return list of matches."""
    data = urllib.parse.urlencode({
        "text": text,
        "language": LT_LANGUAGE,
        "enabledOnly": "false",
        "disabledCategories": "PUNCTUATION",  # Slovak punctuation rules are often wrong for creative prose
    }).encode("utf-8")

    req = urllib.request.Request(
        LT_API_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read())
            return result.get("matches", [])
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [HTTP {e.code}] {e.reason}: {body[:200]}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  [Chyba API] {e}", file=sys.stderr)
        return []


def check_file(path: Path, filter_types: set | None = None, only_types: set | None = None) -> int:
    """Check one file. Returns number of issues found."""
    raw = path.read_text(encoding="utf-8")
    clean = prepare_text(raw)
    chunks = chunk_text(clean)

    all_matches = []
    offset = 0

    for i, chunk in enumerate(chunks):
        if i > 0:
            time.sleep(LT_RATE_LIMIT_SLEEP)
        matches = call_languagetool(chunk)
        # Adjust character offset for multi-chunk files
        for m in matches:
            m["_offset_adj"] = offset
        all_matches.extend(matches)
        offset += len(chunk) + 2  # +2 for '\n\n' separator

    # Filter by type
    def passes_filter(m) -> bool:
        issue_type = m.get("rule", {}).get("issueType", "other").lower()
        word = m.get("context", {}).get("text", "")[
            m.get("context", {}).get("offset", 0):
            m.get("context", {}).get("offset", 0) + m.get("context", {}).get("length", 0)
        ]
        if is_whitelisted(word):
            return False
        if filter_types and issue_type in filter_types:
            return False
        if only_types and issue_type not in only_types:
            return False
        return True

    filtered = [m for m in all_matches if passes_filter(m)]

    if not filtered:
        return 0

    print(f"\n{'-' * 70}")
    print(f"  {path.name}  ({len(filtered)} problemov)")
    print(f"{'-' * 70}")

    for m in filtered:
        ctx = m.get("context", {})
        ctx_text = ctx.get("text", "")
        ctx_off = ctx.get("offset", 0)
        ctx_len = ctx.get("length", 1)

        # Highlight the problematic word in context
        before = ctx_text[:ctx_off]
        problem = ctx_text[ctx_off:ctx_off + ctx_len]
        after = ctx_text[ctx_off + ctx_len:]
        context_display = f"{before}>>>{problem}<<<{after}".strip()

        rule = m.get("rule", {})
        issue_type = rule.get("issueType", "other").lower()
        label = TYPE_LABELS.get(issue_type, "INÉ")
        message = m.get("message", "")
        replacements = [r["value"] for r in m.get("replacements", [])[:3]]

        print(f"\n  [{label}] {message}")
        print(f"  Kontext: {context_display[:100]}")
        if replacements:
            print(f"  Návrhy:  {' / '.join(replacements)}")

    return len(filtered)


def find_arc_files(arc_name: str) -> list[Path]:
    repo_root = Path(__file__).parent.parent
    pattern = f"World-Bible/books/**/drafts/{arc_name}-arc/*.md"
    files = sorted(repo_root.glob(pattern))
    if not files:
        # Try without -arc suffix
        pattern = f"World-Bible/books/**/drafts/{arc_name}/*.md"
        files = sorted(repo_root.glob(pattern))
    return files


def main():
    parser = argparse.ArgumentParser(description="Slovak spell/grammar check for NULL VOID drafts")
    parser.add_argument("files", nargs="*", help="Specific .md files to check")
    parser.add_argument("--arc", default="heist", help="Arc name (default: heist)")
    parser.add_argument("--ignore-types", nargs="+",
                        metavar="TYPE",
                        help="Issue types to skip: misspelling grammar style typographical")
    parser.add_argument("--only-types", nargs="+",
                        metavar="TYPE",
                        help="Only show these issue types")
    parser.add_argument("--add-whitelist", nargs="+", metavar="WORD",
                        help="Extra words to whitelist for this run")
    args = parser.parse_args()

    if args.add_whitelist:
        WHITELIST.update(w.lower() for w in args.add_whitelist)

    filter_types = set(t.lower() for t in args.ignore_types) if args.ignore_types else None
    only_types = set(t.lower() for t in args.only_types) if args.only_types else None

    # Determine files to check
    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = find_arc_files(args.arc)
        if not paths:
            print(f"Nenašli sa žiadne súbory pre arc '{args.arc}'.", file=sys.stderr)
            sys.exit(1)
        print(f"Kontrolujem {len(paths)} súborov v '{args.arc}-arc'...")

    total_issues = 0
    for i, path in enumerate(paths):
        if not path.exists():
            print(f"Súbor neexistuje: {path}", file=sys.stderr)
            continue
        print(f"  [{i+1}/{len(paths)}] {path.name}", end="", flush=True)
        count = check_file(path, filter_types=filter_types, only_types=only_types)
        if count == 0:
            print(f"  OK - bez chyb")
        total_issues += count
        if i < len(paths) - 1:
            time.sleep(LT_RATE_LIMIT_SLEEP)

    print(f"\n{'=' * 70}")
    print(f"  Celkom: {total_issues} problemov v {len(paths)} suboroch")
    print(f"{'=' * 70}")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
