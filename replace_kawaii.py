import os
import re

directories = [
    r'c:\Users\brani\Documents\GitHub\null-void\World-Bible'
]

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return
    
    orig_content = content
    
    # "Kawaii nálepky" -> "Roztomilé nálepky"
    content = re.sub(r'\bKawaii nálepk', 'Roztomilé nálepk', content)
    content = re.sub(r'\bkawaii nálepk', 'roztomilé nálepk', content)
    
    # "Kawaii hlas" -> "Sladký hlas"
    content = re.sub(r'\bKawaii hlas', 'Sladký hlas', content)
    content = re.sub(r'\bkawaii hlas', 'sladký hlas', content)
    
    # "kawaii aesthetics" -> "roztomilá aesthetics"
    content = re.sub(r'"Kawaii" aesthetics', '"Roztomilá" estetika', content)
    
    # "kawaii ruka" -> "roztomilá ruka"
    content = re.sub(r'\bkawaii ruka', 'roztomilá ruka', content)
    
    # "kawaii úsmev" -> "sladký úsmev"
    content = re.sub(r'\bkawaii úsmev', 'sladký úsmev', content)
    
    # Specific fragments
    content = content.replace('Takmer *kawaii*', 'Takmer *rozkošné*')
    content = content.replace('[Kawaii. Testuje', '[Sladko. Testuje')
    content = content.replace('Nie kawaii. Nie business.', 'Nie sladký. Nie business.')
    content = content.replace('Nie kawaii.', 'Nie sladko.')
    content = content.replace('business ↔ kawaii', 'business ↔ sladký')
    content = content.replace('not business, not kawaii', 'nie obchodný, nie sladký')
    content = content.replace('hlboký/kawaii/pravda', 'hlboký/sladký/pravda')
    
    # Fallback for remaining (case-insensitive)
    content = re.sub(r'\bKawaii\b', 'Sladký', content)
    content = re.sub(r'\bkawaii\b', 'sladký', content)

    if orig_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

for d in directories:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.md'):
                replace_in_file(os.path.join(root, file))
