#!/usr/bin/env python3
"""
Audiobook Adaptation Script for NULL VOID
==========================================
Transforms book-version markdown chapters into audiobook-optimized versions.

Key transformations:
1. Strip all inline comments [→ ...], [NOTE: ...], [TODO: ...], [FIXME: ...]
2. Strip markdown images ![...](...) and HTML image blocks
3. Strip HTML blocks (epigraph divs, etc.)
4. Strip markdown formatting (bold, italic markers) — TTS doesn't render them
5. Insert SSML-style pauses at scene breaks (---) and chapter headings
6. Clean up excessive whitespace

NOTE: This script handles MECHANICAL transformations only.
      Manual audiobook adaptations (dialogue attribution, inner monologue
      markers, pacing cuts) should be done in the audiobook/ chapter files
      BEFORE running this script for final TTS preparation.

Usage:
    python scripts/adapt_for_audiobook.py
    python scripts/adapt_for_audiobook.py --source audiobook  # use audiobook/ adapted versions
    python scripts/adapt_for_audiobook.py --source drafts     # use original drafts (default: audiobook if exists)
"""

import os
import re
import argparse

REPO_DIR = '/Users/branislavlang/Documents/GitHub/null-void'
DRAFTS_DIR = os.path.join(REPO_DIR, 'World-Bible/books/book-1-prach-nevriss/drafts/heist-arc')
AUDIOBOOK_DIR = os.path.join(DRAFTS_DIR, 'audiobook')
OUTPUT_FILE = os.path.join(REPO_DIR, 'export/book-1-prach-nevriss-audiobook.md')

# Chapter order (same as build.py)
CHAPTERS = [
    '00-prologue.md',
    '01-karakuri.md',
    '02-dead-bells.md',
    '03-prelude-south.md',
    '03-tunnels.md',
    '04-elanias-blade.md',
    '04.1-interlude-glass-city.md',
]

PAUSE_SHORT = '\n\n'        # ~0.5s natural paragraph pause
PAUSE_MEDIUM = '\n\n...\n\n'  # ~1.5s scene break pause
PAUSE_LONG = '\n\n......\n\n'  # ~3s chapter break pause


def strip_inline_comments(text):
    """Remove all inline comments: [→ ...], [NOTE: ...], [TODO: ...], [FIXME: ...]"""
    # Multi-pattern removal
    text = re.sub(r'\[→[^\]]*\]', '', text)
    text = re.sub(r'\[NOTE:[^\]]*\]', '', text)
    text = re.sub(r'\[TODO:[^\]]*\]', '', text)
    text = re.sub(r'\[FIXME:[^\]]*\]', '', text)
    return text


def strip_images_and_html(text):
    """Remove markdown images and HTML blocks"""
    # HTML blocks (div, img, etc.)
    text = re.sub(r'<div[^>]*>.*?</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Markdown images
    text = re.sub(r'!\[[^\]]*\]\([^\)]*\)', '', text)
    return text


def strip_markdown_formatting(text):
    """Remove bold/italic markers but keep the text"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Italic — but preserve inner monologue markers that were manually converted
    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', text)
    # Underscores
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', text)
    return text


def strip_frontmatter(text):
    """Remove YAML frontmatter"""
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    return text


def convert_scene_breaks(text):
    """Convert --- scene breaks to audio pauses"""
    # Scene break (---) → medium pause
    text = re.sub(r'^\s*[-*]{3,}\s*$', PAUSE_MEDIUM, text, flags=re.MULTILINE)
    return text


def convert_blockquotes(text):
    """Convert blockquotes (epigraphs) to narrator text"""
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    return text


def clean_whitespace(text):
    """Clean up excessive blank lines"""
    # Max 2 consecutive newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Strip trailing whitespace on lines
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    # Remove lines that are just whitespace after comment removal
    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text.strip()


def process_chapter(text):
    """Apply all transformations to a chapter"""
    text = strip_frontmatter(text)
    text = strip_inline_comments(text)
    text = strip_images_and_html(text)
    text = convert_blockquotes(text)
    text = strip_markdown_formatting(text)
    text = convert_scene_breaks(text)
    text = clean_whitespace(text)
    return text


def build_audiobook(source='auto'):
    """Build merged audiobook markdown from chapters"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    parts = []

    for chapter_file in CHAPTERS:
        # Determine source: prefer audiobook/ adapted versions if they exist
        audiobook_path = os.path.join(AUDIOBOOK_DIR, chapter_file)
        drafts_path = os.path.join(DRAFTS_DIR, chapter_file)

        if source == 'audiobook' or (source == 'auto' and os.path.exists(audiobook_path)):
            src_path = audiobook_path
            src_label = 'audiobook'
        else:
            src_path = drafts_path
            src_label = 'draft'

        if not os.path.exists(src_path):
            print(f"  [WARN] Missing: {chapter_file}")
            continue

        with open(src_path, 'r', encoding='utf-8') as f:
            text = f.read()

        processed = process_chapter(text)
        parts.append(processed)
        print(f"  [{src_label}] {chapter_file} -> {len(processed)} chars")

    # Join chapters with long pauses between them
    merged = (PAUSE_LONG).join(parts)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(merged)

    print(f"\n  Output: {OUTPUT_FILE}")
    print(f"  Total: {len(merged)} chars")
    return OUTPUT_FILE


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build audiobook-optimized markdown')
    parser.add_argument('--source', choices=['auto', 'audiobook', 'drafts'], default='auto',
                       help='Source: auto (prefer audiobook/), audiobook, or drafts')
    args = parser.parse_args()

    print("NULL VOID Audiobook Adapter")
    print("=" * 40)
    build_audiobook(source=args.source)
    print("\nDone!")
