import os
import re
import asyncio
import edge_tts

# Absolute paths
REPO_DIR = '/Users/branislavlang/Documents/GitHub/null-void'
SOURCE_FILE = os.path.join(REPO_DIR, 'export/book-1-prach-nevriss.md')
OUTPUT_DIR = os.path.join(REPO_DIR, 'export/audio')
TEMP_DIR = os.path.join(OUTPUT_DIR, 'temp')
VOICE = 'sk-SK-LukasNeural'

def clean_markdown_general(text):
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
            
    text = re.sub(r'<div class="image-wrapper">.*?</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'^---\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    return text.strip()

async def generate_audio():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = clean_markdown_general(content)
    chapters = re.split(r'\n(?=#\s+)', '\n' + content)
    
    chapter_num = 0
    for chapter_text in chapters:
        chapter_text = chapter_text.strip()
        if not chapter_text:
            continue
            
        lines = chapter_text.split('\n')
        heading = lines[0].strip()
        
        if not heading.startswith('# '):
            continue
            
        heading_clean = heading.lstrip('# ').strip()
        body = '\n'.join(lines[1:]).strip()
        body = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
        
        if not body:
            continue
            
        title_for_file = re.sub(r'[^a-zA-Z0-9ščťžýáíéäôúňľĺ]', '_', heading_clean)
        title_for_file = re.sub(r'_+', '_', title_for_file).lower().strip('_')
        
        filename = f"{chapter_num:02d}-{title_for_file}.mp3"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(output_path):
            print(f"[{chapter_num:02d}] Skipping (already exists): {filename}")
            chapter_num += 1
            continue
            
        print(f"\n=======================")
        print(f"[{chapter_num:02d}] Generating Chapter: {heading_clean}")
        
        paragraphs = [heading_clean] + [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
        
        # We will append the MP3 chunks into the output_path directly as binary data.
        with open(output_path, 'wb') as outfile:
            for idx, paragraph in enumerate(paragraphs):
                if len(paragraph) < 2:
                    continue
                    
                temp_file = os.path.join(TEMP_DIR, f"{chapter_num:02d}_temp_{idx}.mp3")
                communicate = edge_tts.Communicate(paragraph, VOICE)
                try:
                    await communicate.save(temp_file)
                    
                    with open(temp_file, 'rb') as infile:
                        outfile.write(infile.read())
                        
                    os.remove(temp_file)
                    print(f"  -> Generated paragraph {idx+1}/{len(paragraphs)}", end='\r')
                except Exception as e:
                    print(f"\n  -> Error on paragraph {idx+1}: {e}")
            
        print(f"\n -> Saved full chapter to {filename}")
        chapter_num += 1
        
    try:
        os.rmdir(TEMP_DIR)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(generate_audio())
