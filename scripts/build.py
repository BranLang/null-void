#!/usr/bin/env python3
"""
NULL VOID — Book PDF Builder
Combines chapter markdown files into a single book-ready PDF.

Uses export-clean-drafts.py to strip comments, then merges chapters
into one markdown file and converts to PDF via md-to-pdf.
Cover page is generated separately with zero margins (full bleed)
and merged with the content PDF using PyPDF2.

Requirements:
  npm install -g md-to-pdf
  pip install PyPDF2

Usage:
  python scripts/build-book-pdf.py
  python scripts/build-book-pdf.py --book book-1-prach-nevriss
  python scripts/build-book-pdf.py --book book-1-prach-nevriss --no-pdf  (markdown only)
"""

import subprocess
import sys
import argparse
import re
import base64
import mimetypes
from pathlib import Path

import PyPDF2

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

# CSS for content pages (normal margins handled by @page)
CONTENT_CSS = """
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
"""

# CSS for cover page (full bleed, zero margins)
COVER_CSS = """
@page {
  size: A5;
  margin: 0;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.cover-page {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.cover-page img {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  object-position: center 15%;
  display: block;
  margin: 0;
  padding: 0;
}
"""

# md-to-pdf front-matter for content (normal margins + page numbers)
CONTENT_MD_CONFIG = """---
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

# md-to-pdf front-matter for cover (zero margins, no header/footer)
COVER_MD_CONFIG = """---
pdf_options:
  format: A5
  margin:
    top: 0mm
    bottom: 0mm
    left: 0mm
    right: 0mm
  displayHeaderFooter: false
---

"""


def img_to_base64_uri(img_path: Path) -> str:
    """Convert an image file to a base64 data URI string."""
    mime, _ = mimetypes.guess_type(str(img_path))
    if not mime:
        mime = 'image/png'
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{b64}'


def build_cover_markdown(books_dir: Path) -> str:
    """Build markdown for the cover page only."""
    cover_path = (books_dir / '..' / 'assets' / 'books' / 'book-1-cover-prach.jpeg').resolve()
    if not cover_path.exists():
        return ''
    cover_b64 = img_to_base64_uri(cover_path)
    print(f"  Cover: {cover_path.name}")
    return f'<div class="cover-page">\n<img src="{cover_b64}" />\n</div>\n'


def build_map_markdown(books_dir: Path) -> str:
    """Build markdown for the map page only (full bleed)."""
    map_path = (books_dir / '..' / 'assets' / 'maps' / 'map-achilles.jpeg').resolve()
    if not map_path.exists():
        return ''
    map_b64 = img_to_base64_uri(map_path)
    print(f"  Map: {map_path.name}")
    return f'<div class="cover-page">\n<img src="{map_b64}" />\n</div>\n'


def build_content_markdown(book_name: str, books_dir: Path) -> str:
    """Merge all chapter files into a single markdown string (no cover, no map)."""
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

    for i, chapter_file in enumerate(chapters):
        src = drafts_dir / chapter_file
        if not src.exists():
            print(f"  Warning: {chapter_file} not found, skipping")
            continue

        content = src.read_text(encoding='utf-8')

        # Strip comments
        clean = strip_comments(content)

        # Remove map image (rendered as separate full-bleed page)
        clean = re.sub(r'!\[.*?\]\([^)]*map-achilles[^)]*\)\n*', '', clean)

        # Convert image paths to base64 data URIs for Puppeteer compatibility
        def fix_img_path(match):
            alt = match.group(1)
            rel_path = match.group(2)
            abs_path = (src.parent / rel_path).resolve()
            if abs_path.exists():
                b64_uri = img_to_base64_uri(abs_path)
                return f'![{alt}]({b64_uri})\n'
            print(f"    Warning: image not found: {rel_path}")
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


def run_md_to_pdf(md_path: Path, css_path: Path) -> Path:
    """Run md-to-pdf and return the generated PDF path."""
    result = subprocess.run(
        ['md-to-pdf', str(md_path), '--stylesheet', str(css_path)],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"Error generating PDF:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return md_path.with_suffix('.pdf')


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

    # Build cover, map, and content markdown separately
    cover_md = build_cover_markdown(books_dir)
    map_md = build_map_markdown(books_dir)
    content_md = build_content_markdown(args.book, books_dir)

    # Write merged content markdown (for reference/--no-pdf)
    content_with_config = CONTENT_MD_CONFIG + content_md
    md_output = export_dir / f"{args.book}.md"
    md_output.write_text(content_with_config, encoding='utf-8')
    print(f"\nMerged markdown: {md_output}")

    # Write CSS files
    content_css_path = export_dir / 'book-style.css'
    content_css_path.write_text(CONTENT_CSS, encoding='utf-8')
    cover_css_path = export_dir / 'cover-style.css'
    cover_css_path.write_text(COVER_CSS, encoding='utf-8')

    if args.no_pdf:
        print("Skipping PDF generation (--no-pdf)")
        return

    pdf_output = Path(args.output) if args.output else export_dir / f"{args.book}.pdf"

    try:
        # Generate cover PDF (zero margins, full bleed)
        print("Generating cover PDF...")
        cover_md_path = export_dir / '_cover.md'
        cover_md_path.write_text(COVER_MD_CONFIG + cover_md, encoding='utf-8')
        cover_pdf = run_md_to_pdf(cover_md_path, cover_css_path)

        # Generate map PDF (zero margins, full bleed)
        print("Generating map PDF...")
        map_md_path = export_dir / '_map.md'
        map_md_path.write_text(COVER_MD_CONFIG + map_md, encoding='utf-8')
        map_pdf = run_md_to_pdf(map_md_path, cover_css_path)

        # Generate content PDF (normal margins + page numbers)
        print("Generating content PDF...")
        content_md_path = export_dir / '_content.md'
        content_md_path.write_text(content_with_config, encoding='utf-8')
        content_pdf = run_md_to_pdf(content_md_path, content_css_path)

        # Merge: cover + map + content
        print("Merging PDFs...")
        merger = PyPDF2.PdfMerger()
        merger.append(str(cover_pdf))
        merger.append(str(map_pdf))
        merger.append(str(content_pdf))
        merger.write(str(pdf_output))
        merger.close()

        # Clean up temp files
        for f in [cover_md_path, cover_pdf, map_md_path, map_pdf,
                   content_md_path, content_pdf, cover_css_path]:
            f.unlink(missing_ok=True)

        print(f"\nDone! PDF: {pdf_output}")

    except FileNotFoundError:
        print("Error: md-to-pdf not found. Install with: npm install -g md-to-pdf",
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
