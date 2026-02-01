#!/usr/bin/env python
"""
Performance test with detailed query logging.
"""
import os
import sys
import django
import time
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
sys.path.insert(0, os.path.dirname(__file__))

# Enable SQL query logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

django.setup()

from uniden_assistant.hpdb.models import Country, State, County, HPDBAgency
from django.db import connection
import json

def measure_retrieval():
    """Measure time and queries"""
    
    print("\n" + "="*80)
    print("Performance Test with Query Logging")
    print("="*80)
    
    # Step 1: Get Juneau
    print("\n[Step 1] Getting Juneau county...")
    juneau = County.objects.using('hpdb').get(name='Juneau', state__name='Alaska')
    print(f"Found: {juneau} (ID: {juneau.id}, county_id: {juneau.county_id})")
    
    # Step 2: Get agencies
    print("\n[Step 2] Getting agencies for Juneau...")
    print(f"Using filter: HPDBAgency.objects.using('hpdb').filter(counties={juneau})")
    
    start = time.time()
    print("\n--- Starting query execution ---")
    # Reset query log
    connection.queries_log.clear()
    
    qs = HPDBAgency.objects.using('hpdb').filter(counties=juneau)
    print(f"QuerySet created: {qs.query}")
    
    print("\n--- Executing list() to materialize queryset ---")
    agencies = list(qs)
    
    elapsed = time.time() - start
    print(f"--- Query completed ---\n")
    
    print(f"Time elapsed: {elapsed*1000:.2f}ms")
    print(f"Agencies found: {len(agencies)}")
    for agency in agencies:
        print(f"  - {agency.name}")
    
    print(f"\nQueries executed ({len(connection.queries)}):")
    for i, query in enumerate(connection.queries):
        print(f"\n[Query {i+1}]")
        print(f"  SQL: {query['sql'][:200]}...")
        print(f"  Time: {query['time']}s")

if __name__ == '__main__':
    measure_retrieval()
