import subprocess
import sys
import os
from pathlib import Path

md_path = Path('test.md').resolve()
css_path = Path('test.css').resolve()

print(f"MD Path: {md_path}")
print(f"CSS Path: {css_path}")

cmd = ['md-to-pdf', str(md_path), '--stylesheet', str(css_path)]
if sys.platform == 'win32':
    cmd[0] = 'md-to-pdf.cmd'

print(f"Running: {cmd}")
try:
    subprocess.run(cmd, check=True, shell=True)
    print("Success with backslashes!")
except subprocess.CalledProcessError:
    print("Failed with backslashes!")

# Try with forward slashes
css_path_fwd = str(css_path).replace(os.sep, '/')
print(f"CSS Path Fwd: {css_path_fwd}")
cmd[3] = css_path_fwd

print(f"Running Fwd: {cmd}")
try:
    subprocess.run(cmd, check=True, shell=True)
    print("Success with forward slashes!")
except subprocess.CalledProcessError:
    print("Failed with forward slashes!")
