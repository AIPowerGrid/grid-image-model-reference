#!/usr/bin/env python3
"""
Validate all download URLs in stable_diffusion.json
Standardize the structure and test URLs for accessibility
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import sys

def get_download_url(model_config: Dict[str, Any]) -> Optional[str]:
    """Extract download URL from model config (same logic as catalog_sync.py)"""
    if 'config' not in model_config:
        return None
    
    config = model_config['config']
    download_url = None
    filename = None
    
    # Try config['download'] first (for standard format)
    if 'download' in config and isinstance(config['download'], list) and len(config['download']) > 0:
        download_url = config['download'][0].get('file_url')
        filename = config['download'][0].get('file_name')
    
    # Try config['download_url'] or config['file_url'] (for alternate format)
    if not download_url:
        download_url = config.get('download_url') or config.get('file_url')
    
    # Fallback to top-level URL fields
    if not download_url:
        download_url = model_config.get('download_url') or model_config.get('url')
    
    return download_url

def validate_url(url: str, timeout: int = 10) -> tuple[bool, str, int]:
    """
    Validate URL by checking if it's accessible
    Returns: (is_valid, error_message, status_code)
    """
    try:
        # Use HEAD request first to check if file exists (faster)
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        status_code = response.status_code
        
        # Some servers don't support HEAD, so try GET if HEAD fails
        if status_code == 405 or status_code == 403:
            response = requests.get(url, stream=True, timeout=timeout)
            status_code = response.status_code
        
        if status_code == 200:
            return True, "OK", status_code
        elif status_code == 401:
            return False, "Requires authentication", status_code
        elif status_code == 403:
            return False, "Forbidden - may require authentication", status_code
        elif status_code == 404:
            return False, "Not found", status_code
        else:
            return False, f"HTTP {status_code}", status_code
            
    except requests.exceptions.Timeout:
        return False, "Request timeout", 0
    except requests.exceptions.ConnectionError:
        return False, "Connection error", 0
    except requests.exceptions.TooManyRedirects:
        return False, "Too many redirects", 0
    except Exception as e:
        return False, f"Error: {str(e)}", 0

def validate_all_models(json_file: str = "stable_diffusion.json") -> Dict[str, Any]:
    """Validate all models in the JSON file"""
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"Error: {json_file} not found")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        models = json.load(f)
    
    results = {
        'total': len(models),
        'valid': 0,
        'invalid': 0,
        'missing_url': 0,
        'errors': [],
        'warnings': []
    }
    
    print(f"Validating {results['total']} models...\n")
    
    for model_name, model_config in models.items():
        print(f"Checking: {model_name}")
        
        # Extract URL
        url = get_download_url(model_config)
        
        if not url:
            results['missing_url'] += 1
            results['warnings'].append({
                'model': model_name,
                'issue': 'No download URL found',
                'details': 'Missing config.download[].file_url or config.download_url'
            })
            print(f"  [X] No download URL found")
            continue
        
        print(f"  URL: {url}")
        
        # Validate URL
        is_valid, error_msg, status_code = validate_url(url)
        
        if is_valid:
            results['valid'] += 1
            print(f"  [OK] Valid ({status_code})")
        else:
            results['invalid'] += 1
            results['errors'].append({
                'model': model_name,
                'url': url,
                'error': error_msg,
                'status_code': status_code
            })
            print(f"  [X] Invalid: {error_msg} ({status_code})")
        
        print()
    
    return results

def standardize_structure(json_file: str = "stable_diffusion.json", dry_run: bool = True) -> None:
    """Standardize all model entries to use config.download[] format"""
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"Error: {json_file} not found")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        models = json.load(f)
    
    changes = []
    
    for model_name, model_config in models.items():
        if 'config' not in model_config:
            continue
        
        config = model_config['config']
        needs_update = False
        
        # Check if using alternate format (download_url or file_url at config level)
        if 'download_url' in config or 'file_url' in config:
            download_url = config.get('download_url') or config.get('file_url')
            file_name = config.get('file_name')
            file_path = config.get('file_path')
            
            if download_url:
                needs_update = True
                
                # Create standard download array
                if 'download' not in config:
                    config['download'] = []
                
                # Check if we already have a download entry with this URL
                existing = False
                for entry in config['download']:
                    if entry.get('file_url') == download_url:
                        existing = True
                        break
                
                if not existing:
                    download_entry = {
                        "file_name": file_name or download_url.split('/')[-1].split('?')[0],
                        "file_path": file_path or "",
                        "file_url": download_url
                    }
                    config['download'].append(download_entry)
                
                # Remove old format fields
                if 'download_url' in config:
                    del config['download_url']
                if 'file_url' in config and 'download' in config:
                    del config['file_url']
                if 'file_name' in config and 'download' in config:
                    del config['file_name']
                if 'file_path' in config and 'download' in config:
                    del config['file_path']
                
                changes.append(model_name)
        
        # Also check for files that need download entries
        if 'files' in config and 'download' not in config:
            # Create download array from files
            config['download'] = []
            for file_entry in config['files']:
                if 'path' in file_entry:
                    # This is a file entry, but we need URL - skip for now
                    pass
        
        if needs_update:
            model_config['config'] = config
    
    if changes:
        print(f"\nFound {len(changes)} models that need standardization:")
        for name in changes:
            print(f"  - {name}")
        
        if not dry_run:
            # Backup original file
            backup_path = json_path.with_suffix('.json.backup')
            print(f"\nCreating backup: {backup_path}")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(models, f, indent=4)
            
            # Write updated file
            print(f"Writing updated file: {json_path}")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(models, f, indent=4)
            
            print("\n[OK] Standardization complete!")
        else:
            print("\n[!] DRY RUN - No changes made. Run with --apply to make changes.")
    else:
        print("\n[OK] All models already use standard format!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate and standardize stable_diffusion.json')
    parser.add_argument('--validate', action='store_true', help='Validate all URLs')
    parser.add_argument('--standardize', action='store_true', help='Standardize structure')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')
    parser.add_argument('--file', default='stable_diffusion.json', help='JSON file to process')
    
    args = parser.parse_args()
    
    if not args.validate and not args.standardize:
        # Default: do both
        args.validate = True
        args.standardize = True
    
    if args.validate:
        print("=" * 60)
        print("VALIDATING URLs")
        print("=" * 60)
        results = validate_all_models(args.file)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total models: {results['total']}")
        print(f"[OK] Valid URLs: {results['valid']}")
        print(f"[X] Invalid URLs: {results['invalid']}")
        print(f"[!] Missing URLs: {results['missing_url']}")
        
        if results['errors']:
            print(f"\n[X] ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"  - {error['model']}: {error['error']} ({error['status_code']})")
                print(f"    URL: {error['url']}")
        
        if results['warnings']:
            print(f"\n[!] WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"  - {warning['model']}: {warning['issue']}")
    
    if args.standardize:
        print("\n" + "=" * 60)
        print("STANDARDIZING STRUCTURE")
        print("=" * 60)
        standardize_structure(args.file, dry_run=not args.apply)

if __name__ == '__main__':
    main()

