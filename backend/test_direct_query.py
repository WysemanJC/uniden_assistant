#!/usr/bin/env python
"""
Direct Django test of channel-groups query performance
"""
import os
import sys
import django
import time
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.db import connection
from django.test.utils import CaptureQueriesContext
from uniden_assistant.hpdb.models import HPDBAgency, HPDBChannelGroup

print("=" * 80)
print("Direct Django Query Performance Test")
print("=" * 80)

# Find agencies in Juneau
juneau_agencies = HPDBAgency.objects.using('hpdb').filter(counties__county_id=76).distinct()[:3]

for agency in juneau_agencies:
    print(f"\n[Agency: {agency.name_tag}]")
    
    # Test 1: Direct query
    print(f"  1. Direct query by agency_id:")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        groups = list(HPDBChannelGroup.objects.using('hpdb').filter(agency_id=agency.id))
    elapsed = time.time() - start
    print(f"     Time: {elapsed*1000:.2f}ms, Groups: {len(groups)}, Queries: {len(ctx)}")
    if len(ctx) > 0:
        print(f"     Query: {str(ctx[0]['sql'])[:100]}...")
    
    # Test 2: Using FK lookup
    print(f"  2. Using FK lookup (agency=):")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        groups = list(HPDBChannelGroup.objects.using('hpdb').filter(agency=agency))
    elapsed = time.time() - start
    print(f"     Time: {elapsed*1000:.2f}ms, Groups: {len(groups)}, Queries: {len(ctx)}")
    if len(ctx) > 0:
        print(f"     Query: {str(ctx[0]['sql'])[:100]}...")
    
    # Test 3: Using agency__agency_id
    print(f"  3. Using agency__agency_id:")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        groups = list(HPDBChannelGroup.objects.using('hpdb').filter(agency__agency_id=agency.agency_id))
    elapsed = time.time() - start
    print(f"     Time: {elapsed*1000:.2f}ms, Groups: {len(groups)}, Queries: {len(ctx)}")
    if len(ctx) > 0:
        print(f"     Query: {str(ctx[0]['sql'])[:100]}...")

print("\n" + "=" * 80)
