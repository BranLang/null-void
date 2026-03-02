#!/usr/bin/env python3
"""
NULL VOID — Google Drive Asset Uploader
Uploads all files from World-Bible/assets/ to Google Drive,
preserving folder structure, and generates assets/gdrive-manifest.json.

Requirements:
  pip install google-auth google-auth-oauthlib google-api-python-client

Setup (one-time):
  1. Go to https://console.cloud.google.com
  2. Create a project → Enable Google Drive API
  3. Create OAuth 2.0 credentials (Desktop App) → Download as credentials.json
  4. Place credentials.json next to this script (scripts/credentials.json)
     OR set GDRIVE_CREDENTIALS env var to the path

Usage:
  python scripts/upload-assets.py               # upload all assets
  python scripts/upload-assets.py --dry-run     # preview without uploading
  python scripts/upload-assets.py --folder-id X # upload into existing folder
"""

import json
import os
import sys
import argparse
import mimetypes
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("Missing dependencies. Run:")
    print("  pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

# ──────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────

SCOPES = ['https://www.googleapis.com/auth/drive']
GDRIVE_FOLDER_NAME = 'NULL-VOID-Assets'

REPO_ROOT   = Path(__file__).parent.parent
ASSETS_DIR  = REPO_ROOT / 'World-Bible' / 'assets'
MANIFEST    = REPO_ROOT / 'World-Bible' / 'assets' / 'gdrive-manifest.json'
TOKEN_FILE  = Path(__file__).parent / 'gdrive-token.json'
CREDS_FILE  = Path(os.environ.get('GDRIVE_CREDENTIALS',
                   Path(__file__).parent / 'credentials.json'))


# ──────────────────────────────────────────────────────────
# Auth
# ──────────────────────────────────────────────────────────

def authenticate() -> object:
    """Authenticate with Google Drive via OAuth2. Opens browser on first run."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_FILE.exists():
                print(f"Error: credentials.json not found at {CREDS_FILE}")
                print("Download it from Google Cloud Console → APIs & Services → Credentials")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        print(f"Token saved to {TOKEN_FILE}")

    return build('drive', 'v3', credentials=creds)


# ──────────────────────────────────────────────────────────
# Drive helpers
# ──────────────────────────────────────────────────────────

def get_or_create_folder(service, name: str, parent_id: str = None) -> str:
    """Get existing folder by name (under parent) or create it. Returns folder ID."""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields='files(id, name)').execute()
    files = results.get('files', [])

    if files:
        return files[0]['id']

    metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        metadata['parents'] = [parent_id]

    folder = service.files().create(body=metadata, fields='id').execute()
    return folder['id']


def upload_file(service, local_path: Path, parent_id: str) -> str:
    """Upload a file to Drive under parent_id. Returns file ID."""
    mime, _ = mimetypes.guess_type(str(local_path))
    if not mime:
        mime = 'application/octet-stream'

    metadata = {'name': local_path.name, 'parents': [parent_id]}
    media = MediaFileUpload(str(local_path), mimetype=mime, resumable=True)

    file = service.files().create(
        body=metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file['id']


def make_public(service, file_id: str):
    """Make a file publicly readable (anyone with link)."""
    service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'},
    ).execute()


# ──────────────────────────────────────────────────────────
# Main upload logic
# ──────────────────────────────────────────────────────────

def upload_assets(service, root_folder_id: str, dry_run: bool) -> dict:
    """
    Walk assets/ and upload everything to Drive, mirroring folder structure.
    Returns mapping of relative_path → file_id.
    """
    manifest = {}
    folder_cache = {'': root_folder_id}  # relative_dir → drive_folder_id

    all_files = sorted(ASSETS_DIR.rglob('*'))
    asset_files = [f for f in all_files if f.is_file() and f.name != 'gdrive-manifest.json']

    print(f"\nFound {len(asset_files)} assets to upload\n")

    for i, local_path in enumerate(asset_files, 1):
        rel_path = local_path.relative_to(ASSETS_DIR)
        rel_dir  = str(rel_path.parent) if str(rel_path.parent) != '.' else ''
        rel_str  = str(rel_path).replace('\\', '/')

        print(f"[{i:3}/{len(asset_files)}] {rel_str}", end=' ')

        if dry_run:
            print("(dry run)")
            manifest[rel_str] = 'DRY_RUN'
            continue

        # Ensure parent folder exists on Drive
        if rel_dir not in folder_cache:
            parts = rel_dir.split('/')
            parent = root_folder_id
            built = ''
            for part in parts:
                built = f"{built}/{part}".lstrip('/')
                if built not in folder_cache:
                    fid = get_or_create_folder(service, part, parent)
                    folder_cache[built] = fid
                parent = folder_cache[built]
            folder_cache[rel_dir] = folder_cache[built]

        parent_id = folder_cache[rel_dir]

        try:
            file_id = upload_file(service, local_path, parent_id)
            make_public(service, file_id)
            manifest[rel_str] = file_id
            print(f"→ {file_id}")
        except Exception as e:
            print(f"ERROR: {e}")
            manifest[rel_str] = None

    return manifest


# ──────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Upload NULL VOID assets to Google Drive')
    parser.add_argument('--dry-run',   action='store_true', help='Preview without uploading')
    parser.add_argument('--folder-id', default=None,        help='Use existing Drive folder ID')
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN — no files will be uploaded\n")

    # Load existing manifest if present (to skip already-uploaded files)
    existing = {}
    if MANIFEST.exists():
        existing = json.loads(MANIFEST.read_text()).get('files', {})
        print(f"Loaded existing manifest with {len(existing)} entries")

    service = authenticate()
    print("Authenticated with Google Drive")

    # Get or create root folder
    if args.folder_id:
        root_id = args.folder_id
        print(f"Using existing folder: {root_id}")
    else:
        root_id = get_or_create_folder(service, GDRIVE_FOLDER_NAME)
        print(f"Drive folder '{GDRIVE_FOLDER_NAME}': {root_id}")
        print(f"  https://drive.google.com/drive/folders/{root_id}")

    # Upload
    new_manifest = upload_assets(service, root_id, args.dry_run)

    # Merge with existing (keep old entries for files not re-uploaded)
    merged = {**existing, **{k: v for k, v in new_manifest.items() if v}}

    # Write manifest
    output = {
        'version': 1,
        'folder_id': root_id,
        'folder_url': f'https://drive.google.com/drive/folders/{root_id}',
        'files': merged
    }

    if not args.dry_run:
        MANIFEST.write_text(json.dumps(output, indent=2, ensure_ascii=False))
        print(f"\nManifest written → {MANIFEST}")
        print(f"Total files in manifest: {len(merged)}")
    else:
        print(f"\n[DRY RUN] Would write manifest with {len(new_manifest)} entries")


if __name__ == '__main__':
    main()
