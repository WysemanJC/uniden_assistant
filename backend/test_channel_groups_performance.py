#!/usr/bin/env python3
"""
Test performance of channel-groups endpoint with hierarchy filters
"""
import json
import urllib.request
from urllib.error import HTTPError
import time

API_BASE_URL = 'http://localhost:8001/api'

def make_request(endpoint, params=None):
    """Make HTTP request to API"""
    url = f"{API_BASE_URL}{endpoint}"
    if params:
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        url = f"{url}?{query_string}"
    
    start = time.time()
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            elapsed = time.time() - start
            return elapsed, response.status, data
    except HTTPError as e:
        elapsed = time.time() - start
        content = e.read().decode('utf-8')
        return elapsed, e.code, {'error': content}

print("=" * 80)
print("Testing Channel Groups Endpoint Performance")
print("=" * 80)

# First, get agencies for Juneau
print("\n[Step 1] Get agencies for Juneau County...")
elapsed, status, data = make_request('/hpdb/tree/agencies/', {'county': 'county-76'})
print(f"Status: {status}, Time: {elapsed*1000:.2f}ms")
agencies = data if isinstance(data, list) else []
print(f"Found {len(agencies)} agencies")

# For each agency, test channel-groups fetch with and without hierarchy filters
for agency in agencies[:3]:
    agency_id = agency['id']
    agency_name = agency['name_tag']
    
    print(f"\n[Agency: {agency_name}]")
    
    # Test 1: Without hierarchy filters (just agency)
    print(f"  1. With just agency parameter:")
    elapsed, status, data = make_request('/hpdb/channel-groups/', {'agency': agency_id})
    groups_simple = data if isinstance(data, list) else data.get('results', [])
    print(f"     Status: {status}, Time: {elapsed*1000:.2f}ms, Groups: {len(groups_simple)}")
    
    # Test 2: With hierarchy filters (agency + county + state)
    print(f"  2. With hierarchy filters (agency + county + state):")
    params = {
        'agency': agency_id,
        'county': 'county-76',
        'state': 'state-2'
    }
    elapsed, status, data = make_request('/hpdb/channel-groups/', params)
    groups_filtered = data if isinstance(data, list) else data.get('results', [])
    print(f"     Status: {status}, Time: {elapsed*1000:.2f}ms, Groups: {len(groups_filtered)}")
    
    # Test 3: Measure again to check if there's caching
    print(f"  3. Second call with same parameters (check cache):")
    elapsed, status, data = make_request('/hpdb/channel-groups/', params)
    groups_cached = data if isinstance(data, list) else data.get('results', [])
    print(f"     Status: {status}, Time: {elapsed*1000:.2f}ms, Groups: {len(groups_cached)}")

print("\n" + "=" * 80)
print("Performance Analysis Complete")
print("=" * 80)
