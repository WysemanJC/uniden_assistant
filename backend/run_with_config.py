#!/usr/bin/env python
"""
Wrapper to ensure config.env is loaded before Django starts.
This ensures all environment variables from config.env are available to Django settings.
"""

import os
import sys
from pathlib import Path

def load_config_env():
    """Load config.env from workspace root into environment."""
    # Get the workspace root (parent of backend directory)
    script_path = Path(__file__).resolve()
    backend_dir = script_path.parent
    workspace_root = backend_dir.parent
    config_file = workspace_root / 'config.env'
    
    if not config_file.exists():
        print(f"WARNING: config.env not found at {config_file}", file=sys.stderr)
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Parse KEY=VALUE pairs
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Set in environment (only if not already set)
                if key not in os.environ:
                    os.environ[key] = value
    
if __name__ == '__main__':
    # Load config.env before importing Django
    load_config_env()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
    
    # Now run Django's manage.py
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
