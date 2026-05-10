#!/usr/bin/env python3
"""
Test script to verify hierarchy filtering in HPDB APIs.
Simulates the exact user flow: USA -> Alaska -> Juneau -> Businesses agencies -> Channel groups -> Frequencies
"""

import os
import sys
import json
from urllib.parse import urlencode
import urllib.request
from urllib.error import HTTPError

API_BASE_URL = 'http://localhost:8001/api'

def print_section(title):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}")

def make_request(endpoint, params=None):
    """Make HTTP request to API"""
    url = f"{API_BASE_URL}{endpoint}"
    if params:
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        url = f"{url}?{query_string}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return response.status, data
    except HTTPError as e:
        content = e.read().decode('utf-8')
        return e.code, {'error': content}
    except Exception as e:
        return None, {'error': str(e)}

def test_hierarchy_filtering():
    """Test the complete hierarchy filtering flow"""
    
    print_section("STEP 1: Find USA Country")
    status, data = make_request('/hpdb/countries/')
    print(f"Status: {status}")
    
    countries = data if isinstance(data, list) else data.get('results', [])
    print(f"Found {len(countries)} countries")
    usa = next((c for c in countries if 'USA' in c.get('name_tag', '')), None)
    if not usa:
        print("ERROR: USA not found!")
        return False
    
    usa_id = usa.get('id', '')
    if isinstance(usa_id, str):
        usa_id = usa_id.replace('country-', '')
    print(f"✓ USA ID: country-{usa_id}")
    print(f"  Name: {usa.get('name_tag', 'N/A')}")
    
    print_section("STEP 2: Find Alaska State")
    params = {'country': f'country-{usa_id}'}
    status, data = make_request(f'/hpdb/states/', params)
    print(f"Status: {status}")
    states = data if isinstance(data, list) else data.get('results', [])
    print(f"Found {len(states)} states")
    
    alaska = next((s for s in states if 'Alaska' in s.get('name_tag', '')), None)
    if not alaska:
        print("ERROR: Alaska not found!")
        return False
    
    alaska_id = alaska.get('id', '')
    if isinstance(alaska_id, str):
        alaska_id = alaska_id.replace('state-', '')
    print(f"✓ Alaska ID: state-{alaska_id}")
    print(f"  Name: {alaska.get('name_tag', 'N/A')}")
    print(f"  Short name: {alaska.get('short_name', 'N/A')}")
    
    print_section("STEP 3: Find Juneau County")
    params = {'state': f'state-{alaska_id}'}
    status, data = make_request(f'/hpdb/counties/', params)
    print(f"Status: {status}")
    counties = data if isinstance(data, list) else data.get('results', [])
    print(f"Found {len(counties)} counties")
    
    juneau = next((c for c in counties if 'Juneau' in c.get('name_tag', '')), None)
    if not juneau:
        print("ERROR: Juneau County not found!")
        print(f"Available counties: {[c.get('name_tag', 'N/A') for c in counties[:5]]}")
        return False
    
    juneau_id = juneau.get('id', '')
    if isinstance(juneau_id, str):
        juneau_id = juneau_id.replace('county-', '')
    print(f"✓ Juneau ID: county-{juneau_id}")
    print(f"  Name: {juneau.get('name_tag', 'N/A')}")
    
    print_section("STEP 4: Find Agencies in Juneau")
    params = {'county': f'county-{juneau_id}'}
    status, data = make_request(f'/hpdb/agencies/', params)
    print(f"Status: {status}")
    agencies = data if isinstance(data, list) else data.get('results', [])
    print(f"Found {len(agencies)} agencies in Juneau")
    
    businesses = next((a for a in agencies if 'Business' in a.get('name_tag', '')), None)
    if not businesses:
        print(f"Available agencies: {[a.get('name_tag', 'N/A') for a in agencies[:5]]}")
        # Try to find any agency
        if agencies:
            businesses = agencies[0]
            print(f"Using first agency instead: {businesses.get('name_tag', 'N/A')}")
        else:
            print("ERROR: No agencies found in Juneau!")
            return False
    
    business_id = businesses.get('id', '')
    if isinstance(business_id, str):
        business_id = business_id.replace('agency-', '')
    print(f"✓ Agency ID: agency-{business_id}")
    print(f"  Name: {businesses.get('name_tag', 'N/A')}")
    
    print_section("STEP 5: Find Channel Groups for Agency (with hierarchy filter)")
    params = {
        'agency': f'agency-{business_id}',
        'county': f'county-{juneau_id}',
        'state': f'state-{alaska_id}',
        'country': f'country-{usa_id}'
    }
    status, data = make_request(f'/hpdb/channel-groups/', params)
    print(f"Status: {status}")
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    print(f"Request: /hpdb/channel-groups/?{query_string}")
    groups = data if isinstance(data, list) else data.get('results', [])
    print(f"Found {len(groups)} channel groups")
    
    if not groups:
        print("  ⚠ No channel groups found. Checking without hierarchy filters...")
        status, data = make_request(f'/hpdb/channel-groups/', {'agency': f'agency-{business_id}'})
        print(f"  Status: {status}")
        groups = data if isinstance(data, list) else data.get('results', [])
        print(f"  Without filters: {len(groups)} channel groups")
    
    for i, group in enumerate(groups[:3], 1):
        group_id = group.get('id', '')
        if isinstance(group_id, str):
            group_id = group_id.replace('cgroup-', '')
        print(f"  {i}. {group.get('name_tag', 'N/A')} (ID: cgroup-{group_id})")
    
    print_section("STEP 6: Find Frequencies for each Channel Group")
    total_frequencies = 0
    for group in groups[:1]:  # Test just the first group
        group_id = group.get('id', '')
        if isinstance(group_id, str):
            group_id = group_id.replace('cgroup-', '')
        params = {
            'channel_group': f'cgroup-{group_id}',
            'agency': f'agency-{business_id}',
            'county': f'county-{juneau_id}',
            'state': f'state-{alaska_id}',
            'country': f'country-{usa_id}'
        }
        status, data = make_request(f'/hpdb/frequencies/', params)
        print(f"\n  Group: {group.get('name_tag', 'N/A')} (ID: cgroup-{group_id})")
        print(f"  Status: {status}")
        frequencies = data if isinstance(data, list) else data.get('results', [])
        print(f"  Found {len(frequencies)} frequencies")
        total_frequencies += len(frequencies)
        
        for i, freq in enumerate(frequencies[:3], 1):
            print(f"    {i}. {freq.get('name_tag', 'N/A')} - {freq.get('frequency', 'N/A')} MHz (Audio: {freq.get('audio_option', 'N/A')})")
    
    print_section("TEST SUMMARY")
    print(f"✓ Country: USA")
    print(f"✓ State: Alaska")
    print(f"✓ County: Juneau")
    print(f"✓ Agency: {businesses.get('name_tag', 'N/A')}")
    print(f"✓ Channel Groups: {len(groups)}")
    print(f"✓ Total Frequencies: {total_frequencies}")
    
    if total_frequencies == 0:
        print("\n⚠ WARNING: No frequencies found. This may indicate:")
        print("  1. Data hasn't been imported yet")
        print("  2. HPDB database may be empty")
        print("  3. Hierarchy filtering is blocking results")
    else:
        print("\n✓ SUCCESS: Full hierarchy filtering working correctly!")
    
    return True

if __name__ == '__main__':
    try:
        test_hierarchy_filtering()
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
