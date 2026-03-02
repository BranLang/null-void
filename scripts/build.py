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
  python scripts/build.py heist-arc
  python scripts/build.py nyau-arc
  python scripts/build.py nyau-arc --no-pdf  (markdown only)
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

# ──────────────────────────────────────────────────────────
# Arc configurations
# ──────────────────────────────────────────────────────────

ARC_CONFIGS = {
    'heist-arc': {
        'book': 'book-1-prach-nevriss',
        'chapters': [
            'heist-arc/00-prologue.md',
            'heist-arc/01-karakuri.md',
            'heist-arc/02-dead-bells.md',
            'heist-arc/03-tunnels.md',
            'heist-arc/04-elanias-blade.md',
            'heist-arc/04.1-interlude-glass-city.md',
            # 'links-arc/01-golden-cage.md',
            # 'links-arc/02-frozen-bridge.md',
            # 'links-arc/03-antiquarian.md',
            # 'links-arc/03-desolation.md',
            # 'maks-arc/05-blood-ritual.md',
            # 'maks-arc/06-sky-hammer.md',
            # 'maks-arc/07-dust-of-achilles.md',
        ],
        'cover': 'books/book-1-cover-prach.jpeg',
        'cover_fit': 'cover',           # object-fit for cover image
        'cover_position': 'center 15%',
        'epigraph': None,               # extract from content
        'output': 'heist-arc.pdf',
    },
    'nyau-arc': {
        'book': 'book-1-prach-nevriss',
        'chapters': [
            'nyau-arc/01-lantern-festival.md',
            'nyau-arc/02-first-light-cast-1.md',
            'nyau-arc/03-first-light-cast-2.md',
            'nyau-arc/04-itaka.md',
            'nyau-arc/04.5-interlude-temple.md',
            'nyau-arc/05-black-book.md',
            'nyau-arc/06-within-temptation.md',
            'nyau-arc/06.5-interlude-breakup.md',
            'nyau-arc/07-farewell.md',
        ],
        'cover': 'books/book-1/covers/book-nyau-arc-cover.png',
        'cover_fit': 'contain',
        'cover_position': 'center center',
        'epigraph': {
            'html': """<div class="epigraph">
<p>„A El povedala: Pusť svetlo. Nech stúpa. Nech sa dotkne hviezd a nech sa vráti ako dážď — lebo každé svetlo, čo vypustíš, sa k tebe vráti stonásobne."</p>
<p class="epigraph-author">Kniha El, 1:7</p>
</div>
""",
            'strip_first_chapter': True,  # remove blockquote epigraph from ch1
        },
        'output': 'nyau-arc.pdf',
    },
}

# ──────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────

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

/* Chapter epigraph: own page, vertically centered */
.chapter-epigraph {
  page-break-before: always;
  page-break-after: always;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chapter-epigraph blockquote {
  font-style: italic;
  text-align: center;
  border-left: none;
  text-indent: 0;
  margin: 0 2em;
  max-width: 80%;
}

.chapter-epigraph blockquote p {
  text-indent: 0;
  font-size: 9pt;
  line-height: 1.6;
}

.chapter-epigraph .epigraph-source {
  display: block;
  margin-top: 0.8em;
  font-style: normal;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 7.5pt;
}

h2 {
  font-size: 11pt;
  font-weight: normal;
  text-align: center;
  margin-top: 15mm;
  margin-bottom: 8mm;
  font-style: italic;
  letter-spacing: 1px;
  page-break-after: avoid;
}

h3 {
  font-size: 10pt;
  font-weight: normal;
  text-align: center;
  font-style: italic;
  letter-spacing: 1px;
  margin-top: 5mm;
  margin-bottom: 0;
  page-break-after: avoid;
}

p {
  margin: 0;
  text-indent: 1.5em;
  orphans: 3;
  widows: 3;
  break-inside: avoid;
  page-break-inside: avoid;
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

EPIGRAPH_CSS = """
@page {
  size: A5;
  margin: 25mm 22mm;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.epigraph {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  font-family: 'Garamond', 'Georgia', serif;
}

.epigraph p {
  font-style: italic;
  font-size: 10pt;
  line-height: 1.9;
  max-width: 28em;
  color: #1a1a1a;
}

.epigraph .epigraph-author {
  margin-top: 1.5em;
  font-style: normal;
  letter-spacing: 3px;
  font-size: 8.5pt;
  text-transform: uppercase;
  color: #555;
}
"""

TERRA_MAP_CSS = """
@page {
  size: A5 landscape;
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
  object-position: center center;
  display: block;
  margin: 0;
  padding: 0;
}
"""

def make_cover_css(arc_config):
    """Generate cover CSS based on arc config."""
    return f"""
@page {{
  size: A5;
  margin: 0;
}}

html, body {{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}}

.cover-page {{
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #000;
}}

.cover-page img {{
  width: 100vw;
  height: 100vh;
  object-fit: {arc_config['cover_fit']};
  object-position: {arc_config['cover_position']};
  display: block;
  margin: 0;
  padding: 0;
}}
"""

# md-to-pdf front-matter configs
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

EPIGRAPH_MD_CONFIG = """---
pdf_options:
  format: A5
  margin:
    top: 25mm
    bottom: 25mm
    left: 22mm
    right: 22mm
  displayHeaderFooter: false
---

"""

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


# ──────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────

def img_to_base64_uri(img_path: Path) -> str:
    """Convert an image file to a base64 data URI string."""
    mime, _ = mimetypes.guess_type(str(img_path))
    if not mime:
        mime = 'image/png'
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{b64}'


def build_cover_markdown(assets_dir: Path, arc_config: dict) -> str:
    """Build markdown for the cover page only."""
    cover_path = (assets_dir / arc_config['cover']).resolve()
    if not cover_path.exists():
        print(f"  Warning: cover not found: {cover_path}")
        return ''
    cover_b64 = img_to_base64_uri(cover_path)
    print(f"  Cover: {cover_path.name}")
    return f'<div class="cover-page">\n<img src="{cover_b64}" />\n</div>\n'


def build_map_markdown(assets_dir: Path, map_file: str) -> str:
    """Build markdown for a map page (full bleed)."""
    map_path = (assets_dir / 'maps' / map_file).resolve()
    if not map_path.exists():
        print(f"  Warning: {map_file} not found, skipping")
        return ''
    map_b64 = img_to_base64_uri(map_path)
    print(f"  Map: {map_path.name}")
    return f'<div class="cover-page">\n<img src="{map_b64}" />\n</div>\n'


def extract_epigraph_markdown(content: str) -> tuple[str, str]:
    """Extract epigraph div from content. Returns (epigraph_html, content_without_epigraph)."""
    match = re.search(r'<div class="epigraph">.*?</div>\s*', content, re.DOTALL)
    if match:
        epigraph = match.group(0)
        content_clean = content[:match.start()] + content[match.end():]
        return epigraph, content_clean
    return '', content


def build_content_markdown(arc_config: dict, books_dir: Path) -> str:
    """Merge all chapter files into a single markdown string (no cover, no map)."""
    book_name = arc_config['book']
    chapters = arc_config['chapters']

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

        # Remove metadata lines (POV, Lokácia, Čas, Nálada, etc.)
        clean = re.sub(r'\*\*(?:POV|Lokácia|Čas|Nálada|Postavy|Cieľ)\*\*:[^\n]*\n*', '', clean)

        # Convert image paths to base64 or copy to export/_assets
        def fix_img_path(match):
            import shutil
            alt = match.group(1)
            rel_path = match.group(2)
            abs_path = (src.parent / rel_path).resolve()
            if abs_path.exists():
                export_assets_dir = books_dir.parent.parent / 'export' / '_assets'
                export_assets_dir.mkdir(parents=True, exist_ok=True)
                dest_name = f"{src.stem}_{abs_path.name}"
                dest_path = export_assets_dir / dest_name
                shutil.copy2(abs_path, dest_path)
                return f'\n<div class="image-wrapper"><img src="_assets/{dest_name}" alt="{alt}" /></div>\n\n'
            print(f"    Warning: image not found: {rel_path}")
            return ''
        clean = re.sub(r'!\[(.*?)\]\((.*?)\)\n*', fix_img_path, clean)

        # Remove trailing "— koniec interlúdia —" markers (we use page breaks)
        clean = re.sub(r'\n*\*— koniec interlúdia —\*\n*', '\n', clean)

        # First chapter: remove its blockquote epigraph if arc uses hardcoded epigraph
        epigraph_cfg = arc_config.get('epigraph')
        if i == 0 and epigraph_cfg and epigraph_cfg.get('strip_first_chapter'):
            clean = clean.lstrip('\n')
            clean = re.sub(r'^(>.*\n)+\s*\n*', '', clean)

        # Add a few newlines between chapters
        if i > 0:
            parts.append('\n\n')

        # Strip "## Časť" headings if the part is shorter than ~4000 characters
        def remove_short_parts(match):
            heading = match.group(1)
            content = match.group(2)
            if len(content.strip()) < 4000:
                return content.lstrip()
            return heading + content

        clean = re.sub(r'(## Časť[^\n]*\n+)(.*?(?=\n## |\n# |\Z))', remove_short_parts, clean, flags=re.DOTALL)

        parts.append(clean.strip())
        parts.append('\n\n')
        print(f"  + {chapter_file}")

    merged = ''.join(parts)

    # Put chapter epigraphs on their own centered page, heading on next page
    def wrap_chapter_epigraph(match):
        blockquote = match.group(1)
        heading = match.group(2)
        quote_lines = []
        source_line = None
        for line in blockquote.strip().split('\n'):
            line = line.lstrip('> ').strip()
            if not line:
                continue
            line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
            if line.startswith('—') or line.startswith('–'):
                source_line = f'<span class="epigraph-source">{line}</span>'
            else:
                quote_lines.append(line)
        quote_html = '<br>\n'.join(quote_lines)
        if source_line:
            bq_html = f'<blockquote>\n<p>{quote_html}</p>\n<p>{source_line}</p>\n</blockquote>'
        else:
            bq_html = f'<blockquote>\n<p>{quote_html}</p>\n</blockquote>'
        return f'\n<div class="chapter-epigraph">\n{bq_html}\n</div>\n\n{heading}\n'

    merged = re.sub(
        r'((?:^>.*\n)+)\s*\n*(# [^\n]+)',
        wrap_chapter_epigraph,
        merged,
        flags=re.MULTILINE
    )

    # Remove --- that immediately follow </div> (chapter-epigraph)
    merged = re.sub(r'(</div>)\s*\n+---\n*', r'\1\n\n', merged)

    return merged


def run_md_to_pdf(md_path: Path, css_path: Path) -> Path:
    """Run md-to-pdf and return the generated PDF path."""
    use_shell = (sys.platform == 'win32')
    md_path_str = str(md_path.resolve()).replace('\\', '/')
    css_path_str = str(css_path.resolve()).replace('\\', '/')

    print(f"Running md-to-pdf on {md_path_str} with css {css_path_str}...")
    try:
        result = subprocess.run(
            ['md-to-pdf', md_path_str, '--stylesheet', css_path_str],
            capture_output=False, text=True, timeout=120, shell=use_shell
        )
    except subprocess.TimeoutExpired:
        print(f"Error: md-to-pdf timed out after 120s on {md_path}", file=sys.stderr)
        sys.exit(1)
    if result.returncode != 0:
        print(f"Error generating PDF:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return md_path.with_suffix('.pdf')


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Build book PDF from markdown chapters')
    parser.add_argument('arc', choices=list(ARC_CONFIGS.keys()),
                        help='Which arc to build')
    parser.add_argument('--no-pdf', action='store_true',
                        help='Only generate merged markdown, skip PDF conversion')
    parser.add_argument('--output', default=None,
                        help='Output filename (default: export/<arc>.pdf)')
    args = parser.parse_args()

    arc_config = ARC_CONFIGS[args.arc]
    repo_root = Path(__file__).parent.parent
    books_dir = repo_root / 'World-Bible' / 'books'
    assets_dir = repo_root / 'World-Bible' / 'assets'
    export_dir = repo_root / 'export'
    export_dir.mkdir(parents=True, exist_ok=True)

    print(f"Building: {args.arc}\n")

    # Build cover, maps, and content markdown
    cover_md = build_cover_markdown(assets_dir, arc_config)
    map_md = build_map_markdown(assets_dir, 'map-achilles.jpeg')
    terra_map_md = build_map_markdown(assets_dir, 'map-terra.png')
    content_md = build_content_markdown(arc_config, books_dir)

    # Epigraph: use hardcoded or extract from content
    epigraph_cfg = arc_config.get('epigraph')
    if epigraph_cfg:
        epigraph_md = epigraph_cfg['html']
        _, content_md = extract_epigraph_markdown(content_md)
        print("  Epigraph: hardcoded")
    else:
        epigraph_md, content_md = extract_epigraph_markdown(content_md)
        if epigraph_md:
            print("  Epigraph: extracted from content")

    # Write merged content markdown
    content_with_config = CONTENT_MD_CONFIG + content_md
    md_output = export_dir / f"{args.arc}.md"
    md_output.write_text(content_with_config, encoding='utf-8')
    print(f"\nMerged markdown: {md_output}")

    # Write CSS files
    content_css_path = export_dir / 'book-style.css'
    content_css_path.write_text(CONTENT_CSS, encoding='utf-8')
    cover_css = make_cover_css(arc_config)
    cover_css_path = export_dir / 'cover-style.css'
    cover_css_path.write_text(cover_css, encoding='utf-8')
    terra_map_css_path = export_dir / 'terra-map-style.css'
    terra_map_css_path.write_text(TERRA_MAP_CSS, encoding='utf-8')
    epigraph_css_path = export_dir / 'epigraph-style.css'
    epigraph_css_path.write_text(EPIGRAPH_CSS, encoding='utf-8')

    if args.no_pdf:
        print("Skipping PDF generation (--no-pdf)")
        return

    pdf_output = Path(args.output) if args.output else export_dir / arc_config['output']

    try:
        # Generate cover PDF
        print("Generating cover PDF...")
        cover_md_path = export_dir / '_cover.md'
        cover_md_path.write_text(COVER_MD_CONFIG + cover_md, encoding='utf-8')
        cover_pdf = run_md_to_pdf(cover_md_path, cover_css_path)

        # Generate Achilles map PDF
        print("Generating Achilles map PDF...")
        map_md_path = export_dir / '_map.md'
        map_md_path.write_text(COVER_MD_CONFIG + map_md, encoding='utf-8')
        map_pdf = run_md_to_pdf(map_md_path, cover_css_path)

        # Generate Terra map PDF (landscape)
        print("Generating Terra map PDF (landscape)...")
        terra_map_md_path = export_dir / '_terra-map.md'
        terra_map_md_path.write_text(COVER_MD_CONFIG + terra_map_md, encoding='utf-8')
        terra_map_pdf = run_md_to_pdf(terra_map_md_path, terra_map_css_path)

        # Generate epigraph PDF
        epigraph_pdf = None
        if epigraph_md:
            print("Generating epigraph PDF...")
            epigraph_md_path = export_dir / '_epigraph.md'
            epigraph_md_path.write_text(EPIGRAPH_MD_CONFIG + epigraph_md, encoding='utf-8')
            epigraph_pdf = run_md_to_pdf(epigraph_md_path, epigraph_css_path)

        # Generate content PDF
        print("Generating content PDF...")
        content_md_path = export_dir / '_content.md'
        content_md_path.write_text(content_with_config, encoding='utf-8')
        content_pdf = run_md_to_pdf(content_md_path, content_css_path)

        # Merge: cover + achilles map + terra map + [epigraph] + content
        print("Merging PDFs...")
        merger = PyPDF2.PdfMerger()
        merger.append(str(cover_pdf))
        merger.append(str(map_pdf))
        merger.append(str(terra_map_pdf))
        if epigraph_pdf:
            merger.append(str(epigraph_pdf))
        merger.append(str(content_pdf))
        merger.write(str(pdf_output))
        merger.close()

        # Clean up temp files
        temp_files = [cover_md_path, cover_pdf, map_md_path, map_pdf,
                      terra_map_md_path, terra_map_pdf,
                      content_md_path, content_pdf,
                      cover_css_path, terra_map_css_path, epigraph_css_path]
        if epigraph_pdf:
            temp_files.extend([epigraph_md_path, epigraph_pdf])
        for f in temp_files:
            f.unlink(missing_ok=True)

        print(f"\nDone! PDF: {pdf_output}")

    except FileNotFoundError:
        print("Error: md-to-pdf not found. Install with: npm install -g md-to-pdf",
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
