#!/usr/bin/env python
"""
Compatibility wrapper that runs Django management commands using environment variables.
"""

import os
import sys
    
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
