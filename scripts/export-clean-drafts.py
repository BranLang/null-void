#!/usr/bin/env python3
"""
NULL VOID — Clean Draft Export
Strips inline comments from draft .md files and exports clean versions.

Comment conventions:
  [→ path/to/file.md]              Lore reference (source citation)
  [→ path/to/file.md: section]     Lore reference with section
  [NOTE: text]                     Author's note
  [TODO: text]                     Open task / unresolved question
  [FIXME: text]                    Known issue to fix

All text matching [→ ...], [NOTE: ...], [TODO: ...], [FIXME: ...] is stripped.
Entire lines that contain ONLY a comment (after stripping whitespace) are removed.
Empty lines left behind by removed comment-only lines are collapsed.

Usage:
  python scripts/export-clean-drafts.py
  python scripts/export-clean-drafts.py --source "World-Bible/books" --output "export/clean"
"""

import re
import sys
import argparse
from pathlib import Path

# Pattern matches: [→ anything], [NOTE: anything], [TODO: anything], [FIXME: anything]
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


def _replace_comment(match: re.Match) -> str:
    """Replace comment with a single space if it's between text, otherwise empty."""
    s = match.string
    start, end = match.start(), match.end()
    # If there's text before AND after the comment, keep a space
    if start > 0 and end < len(s) and s[start - 1] not in ' \t\n' and s[end] not in ' \t\n':
        return ' '
    return ''


def strip_comments(text: str) -> str:
    """Remove all inline comments from text and clean up empty lines."""
    lines = text.split('\n')
    cleaned = []
    prev_empty = False

    for line in lines:
        # Strip comments from line, preserving spacing between surrounding text
        stripped = COMMENT_PATTERN.sub(_replace_comment, line)

        # If the line is now empty (was comment-only), skip it
        # but preserve intentional empty lines (markdown formatting)
        if stripped.strip() == '' and line.strip() != '':
            # Line had content but it was all comments — skip
            continue

        # Collapse multiple empty lines into max 2
        is_empty = stripped.strip() == ''
        if is_empty and prev_empty:
            continue

        cleaned.append(stripped.rstrip())
        prev_empty = is_empty

    return '\n'.join(cleaned)


def export_clean(source_dir: Path, output_dir: Path, verbose: bool = True):
    """Export clean versions of all draft .md files."""
    # Find all draft markdown files
    draft_dirs = list(source_dir.glob('**/drafts/**/*.md'))

    if not draft_dirs:
        if verbose:
            print(f"No draft files found in {source_dir}")
        return 0

    exported = 0
    for src_file in draft_dirs:
        # Skip archive directory
        if 'archive' in src_file.parts:
            continue

        # Calculate relative path from source
        rel_path = src_file.relative_to(source_dir)

        # Build output path
        dst_file = output_dir / rel_path

        # Read source
        content = src_file.read_text(encoding='utf-8')

        # Check if file has any comments
        has_comments = bool(COMMENT_PATTERN.search(content))

        # Strip comments
        clean = strip_comments(content)

        # Write clean version
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        dst_file.write_text(clean, encoding='utf-8')
        exported += 1

        if verbose:
            status = "  (has comments)" if has_comments else ""
            print(f"  {rel_path}{status}")

    if verbose:
        print(f"\nExported {exported} files to {output_dir}")

    return exported


def main():
    parser = argparse.ArgumentParser(description='Export clean drafts without comments')
    parser.add_argument('--source', default='World-Bible/books',
                        help='Source directory containing drafts (default: World-Bible/books)')
    parser.add_argument('--output', default='export/clean',
                        help='Output directory for clean files (default: export/clean)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress output')
    args = parser.parse_args()

    # Resolve paths relative to repo root
    repo_root = Path(__file__).parent.parent
    source = repo_root / args.source
    output = repo_root / args.output

    if not source.exists():
        print(f"Error: Source directory not found: {source}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"Exporting clean drafts...")
        print(f"  Source: {source}")
        print(f"  Output: {output}")
        print()

    count = export_clean(source, output, verbose=not args.quiet)

    if count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
