#!/usr/bin/env python3
"""
NULL VOID — Book PDF Builder
Combines chapter markdown files into a single book-ready PDF.

Uses export-clean-drafts.py to strip comments, then merges chapters
into one markdown file and converts to PDF via md-to-pdf.

Requirements:
  npm install -g md-to-pdf

Usage:
  python scripts/build-book-pdf.py
  python scripts/build-book-pdf.py --book book-1-prach-nevriss
  python scripts/build-book-pdf.py --book book-1-prach-nevriss --no-pdf  (markdown only)
"""

import subprocess
import sys
import argparse
import re
from pathlib import Path

# Import strip_comments from sibling script
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
clean_module = import_module('export-clean-drafts')
strip_comments = clean_module.strip_comments

# Chapter order for each book
BOOK_CHAPTERS = {
    'book-1-prach-nevriss': [
        'main-arc/00-prologue.md',
        'main-arc/01.1-interlude-far-from-snow.md',
        'main-arc/01-karakuri.md',
        'main-arc/02-dead-bells.md',
        'main-arc/03-tunnels.md',
        'main-arc/04-elanias-blade.md',
        'main-arc/04.1-interlude-glass-city.md',
        'links-arc/01-golden-cage.md',
        'links-arc/02-frozen-bridge.md',
        'links-arc/03-antiquarian.md',
        'links-arc/03-desolation.md',
        'main-arc/05-blood-ritual.md',
        'main-arc/06-sky-hammer.md',
        'main-arc/07-awakening.md',
        'main-arc/08-epilogue-blockade-run.md',
    ],
}

# PDF styling
BOOK_CSS = """
@page {
  size: A5;
  margin: 20mm 18mm 25mm 18mm;
}

body {
  font-family: 'Garamond', 'Georgia', serif;
  font-size: 9.5pt;
  line-height: 1.5;
  color: #1a1a1a;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
}

h1 {
  font-size: 18pt;
  font-weight: normal;
  text-align: center;
  margin-top: 60mm;
  margin-bottom: 10mm;
  page-break-before: always;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* First h1 (title/cover) should not break before */
h1:first-of-type {
  page-break-before: avoid;
  margin-top: 0;
  font-size: 24pt;
}

h2 {
  font-size: 11pt;
  font-weight: normal;
  text-align: center;
  margin-top: 15mm;
  margin-bottom: 8mm;
  font-style: italic;
  letter-spacing: 1px;
}

h3 {
  font-size: 10pt;
  font-weight: normal;
  text-align: center;
  font-style: italic;
  letter-spacing: 1px;
  margin-top: 5mm;
  margin-bottom: 0;
}

p {
  margin: 0;
  text-indent: 1.5em;
  orphans: 3;
  widows: 3;
}

/* No indent after headings, breaks, or blockquotes */
h1 + p, h2 + p, h3 + p, hr + p, blockquote + p {
  text-indent: 0;
}

blockquote {
  font-style: italic;
  margin: 1.5em 2em;
  border-left: none;
  text-align: center;
  text-indent: 0;
}

blockquote p {
  text-indent: 0;
}

em {
  font-style: italic;
}

strong {
  font-weight: bold;
  letter-spacing: 0.5px;
}

hr {
  border: none;
  text-align: center;
  margin: 2em 0;
}

hr::after {
  content: '* * *';
  letter-spacing: 8px;
  color: #888;
  font-size: 9pt;
}

/* Scene break styling */
p + hr {
  margin-top: 1.5em;
}

/* Images */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1.5em auto;
  page-break-inside: avoid;
}

/* Title page styling */
.title-page {
  text-align: center;
  page-break-after: always;
}
"""

# md-to-pdf front-matter config
MD_TO_PDF_CONFIG = """---
pdf_options:
  format: A5
  margin:
    top: 20mm
    bottom: 25mm
    left: 18mm
    right: 18mm
  displayHeaderFooter: true
  headerTemplate: '<span></span>'
  footerTemplate: '<div style="width:100%;text-align:center;font-size:9pt;color:#555;font-family:Georgia,serif;"><span class="pageNumber"></span></div>'
---

"""


def build_merged_markdown(book_name: str, books_dir: Path) -> str:
    """Merge all chapter files into a single markdown string."""
    chapters = BOOK_CHAPTERS.get(book_name)
    if not chapters:
        print(f"Error: Unknown book '{book_name}'", file=sys.stderr)
        print(f"Available: {', '.join(BOOK_CHAPTERS.keys())}", file=sys.stderr)
        sys.exit(1)

    drafts_dir = books_dir / book_name / 'drafts'
    if not drafts_dir.exists():
        print(f"Error: Drafts directory not found: {drafts_dir}", file=sys.stderr)
        sys.exit(1)

    parts = []

    # Title page with cover
    cover_path = (books_dir / '..' / 'assets' / 'books' / 'book-1-cover-inetis.png').resolve()
    if cover_path.exists():
        parts.append(f'<div style="text-align:center; margin-top:0; padding:0;">\n')
        parts.append(f'<img src="file://{cover_path}" style="max-width:100%; max-height:85%; margin:0 auto;" />\n')
        parts.append(f'</div>\n\n')

    for i, chapter_file in enumerate(chapters):
        src = drafts_dir / chapter_file
        if not src.exists():
            print(f"  Warning: {chapter_file} not found, skipping")
            continue

        content = src.read_text(encoding='utf-8')

        # Strip comments
        clean = strip_comments(content)

        # Fix image paths to absolute so PDF renderer can find them
        def fix_img_path(match):
            alt = match.group(1)
            rel_path = match.group(2)
            abs_path = (src.parent / rel_path).resolve()
            if abs_path.exists():
                return f'![{alt}](file://{abs_path})\n'
            return ''  # Remove if image not found
        clean = re.sub(r'!\[(.*?)\]\((.*?)\)\n*', fix_img_path, clean)

        # Remove trailing "— koniec interlúdia —" markers (we use page breaks)
        clean = re.sub(r'\n*\*— koniec interlúdia —\*\n*', '\n', clean)

        # Add page break between chapters (except first)
        if i > 0:
            parts.append('\n\n<div style="page-break-before: always;"></div>\n\n')

        parts.append(clean.strip())
        parts.append('\n\n')
        print(f"  + {chapter_file}")

    return ''.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Build book PDF from markdown chapters')
    parser.add_argument('--book', default='book-1-prach-nevriss',
                        help='Book directory name (default: book-1-prach-nevriss)')
    parser.add_argument('--no-pdf', action='store_true',
                        help='Only generate merged markdown, skip PDF conversion')
    parser.add_argument('--output', default=None,
                        help='Output filename (default: export/<book-name>.pdf)')
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    books_dir = repo_root / 'World-Bible' / 'books'
    export_dir = repo_root / 'export'
    export_dir.mkdir(parents=True, exist_ok=True)

    print(f"Building book: {args.book}\n")

    # Merge chapters
    merged = build_merged_markdown(args.book, books_dir)

    # Add md-to-pdf config
    final_md = MD_TO_PDF_CONFIG + merged

    # Write merged markdown
    md_output = export_dir / f"{args.book}.md"
    md_output.write_text(final_md, encoding='utf-8')
    print(f"\nMerged markdown: {md_output}")

    # Write CSS
    css_output = export_dir / 'book-style.css'
    css_output.write_text(BOOK_CSS, encoding='utf-8')

    if args.no_pdf:
        print("Skipping PDF generation (--no-pdf)")
        return

    # Generate PDF
    pdf_output = args.output or str(export_dir / f"{args.book}.pdf")
    print(f"Generating PDF: {pdf_output}")

    try:
        result = subprocess.run(
            ['md-to-pdf', str(md_output),
             '--stylesheet', str(css_output)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"Error generating PDF:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        # md-to-pdf outputs to same dir with .pdf extension
        generated = md_output.with_suffix('.pdf')
        if generated.exists() and str(generated) != pdf_output:
            generated.rename(pdf_output)

        print(f"\nDone! PDF: {pdf_output}")

    except FileNotFoundError:
        print("Error: md-to-pdf not found. Install with: npm install -g md-to-pdf",
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
