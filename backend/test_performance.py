#!/usr/bin/env python
"""
Performance test script for HPDB hierarchy retrieval.
Measures time to retrieve agencies for USA > Alaska > Juneau
"""
import os
import sys
import django
import time
from django.conf import settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from uniden_assistant.hpdb.models import Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency

def measure_retrieval():
    """Measure time to retrieve agencies for USA/Alaska/Juneau"""
    
    print("\n" + "="*80)
    print("HPDB Hierarchy Retrieval Performance Test")
    print("="*80)
    
    # Step 1: Find USA
    print("\n[Step 1] Finding Country: USA...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        usa = Country.objects.using('hpdb').filter(name_tag__icontains='united states').first()
        if not usa:
            usa = Country.objects.using('hpdb').filter(name_tag__icontains='usa').first()
    step1_time = time.time() - start
    step1_queries = len(ctx)
    print(f"  Found: {usa} (ID: {usa.country_id if usa else 'N/A'})")
    print(f"  Time: {step1_time*1000:.2f}ms | Queries: {step1_queries}")
    
    if not usa:
        print("  ERROR: Could not find USA!")
        return
    
    # Step 2: Find Alaska
    print("\n[Step 2] Finding State: Alaska...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        alaska = State.objects.using('hpdb').filter(country=usa, name_tag__icontains='alaska').first()
    step2_time = time.time() - start
    step2_queries = len(ctx)
    print(f"  Found: {alaska} (ID: {alaska.state_id if alaska else 'N/A'})")
    print(f"  Time: {step2_time*1000:.2f}ms | Queries: {step2_queries}")
    
    if not alaska:
        print("  ERROR: Could not find Alaska!")
        return
    
    # Step 3: Find Juneau County
    print("\n[Step 3] Finding County: Juneau...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        juneau = County.objects.using('hpdb').filter(state=alaska, name_tag__icontains='juneau').first()
    step3_time = time.time() - start
    step3_queries = len(ctx)
    print(f"  Found: {juneau} (ID: {juneau.county_id if juneau else 'N/A'})")
    print(f"  Time: {step3_time*1000:.2f}ms | Queries: {step3_queries}")
    
    if not juneau:
        print("  ERROR: Could not find Juneau!")
        return
    
    # Step 4: Get agencies for Juneau using M2M relationship
    print("\n[Step 4] Finding Agencies for Juneau (via M2M counties relationship)...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        agencies_m2m = HPDBAgency.objects.using('hpdb').filter(counties=juneau).distinct()
        agencies_m2m_list = list(agencies_m2m)
    step4_time = time.time() - start
    step4_queries = len(ctx)
    print(f"  Found: {len(agencies_m2m_list)} agencies")
    for agency in agencies_m2m_list[:5]:
        print(f"    - {agency.name_tag} ({agency.system_type})")
    if len(agencies_m2m_list) > 5:
        print(f"    ... and {len(agencies_m2m_list) - 5} more")
    print(f"  Time: {step4_time*1000:.2f}ms | Queries: {step4_queries}")
    
    # Step 5: Get agencies using state relationship
    print("\n[Step 5] Finding Agencies for Juneau (via M2M states relationship)...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        agencies_state = HPDBAgency.objects.using('hpdb').filter(states=alaska).distinct()
        agencies_state_list = list(agencies_state)
    step5_time = time.time() - start
    step5_queries = len(ctx)
    print(f"  Found: {len(agencies_state_list)} agencies")
    print(f"  Time: {step5_time*1000:.2f}ms | Queries: {step5_queries}")
    
    # Step 6: Full test (what the API does)
    print("\n[Step 6] Full API Path - Retrieve agencies via tree endpoint...")
    start = time.time()
    with CaptureQueriesContext(connection) as ctx:
        # This is what the tree/agencies endpoint does
        county_lookup = County.objects.using('hpdb').get(county_id=juneau.county_id)
        agencies_api = HPDBAgency.objects.using('hpdb').filter(counties=county_lookup).distinct()
        agencies_api_list = list(agencies_api)
    step6_time = time.time() - start
    step6_queries = len(ctx)
    print(f"  Found: {len(agencies_api_list)} agencies")
    print(f"  Time: {step6_time*1000:.2f}ms | Queries: {step6_queries}")
    
    # Step 7: Get channel groups for first agency (third column data)
    if agencies_api_list:
        test_agency = agencies_api_list[0]
        print(f"\n[Step 7] Finding Channel Groups for '{test_agency.name_tag}'...")
        start = time.time()
        with CaptureQueriesContext(connection) as ctx:
            channel_groups = HPDBChannelGroup.objects.using('hpdb').filter(agency=test_agency)
            channel_groups_list = list(channel_groups)
        step7_time = time.time() - start
        step7_queries = len(ctx)
        print(f"  Found: {len(channel_groups_list)} channel groups")
        for cg in channel_groups_list[:5]:
            print(f"    - {cg.name_tag} ({cg.cgroup_id})")
        if len(channel_groups_list) > 5:
            print(f"    ... and {len(channel_groups_list) - 5} more")
        print(f"  Time: {step7_time*1000:.2f}ms | Queries: {step7_queries}")
        
        # Step 8: Get frequencies for first channel group
        if channel_groups_list:
            test_cgroup = channel_groups_list[0]
            print(f"\n[Step 8] Finding Frequencies for '{test_cgroup.name_tag}'...")
            start = time.time()
            with CaptureQueriesContext(connection) as ctx:
                frequencies = HPDBFrequency.objects.using('hpdb').filter(cgroup=test_cgroup)
                frequencies_list = list(frequencies)
            step8_time = time.time() - start
            step8_queries = len(ctx)
            print(f"  Found: {len(frequencies_list)} frequencies")
            for freq in frequencies_list[:5]:
                audio = freq.audio_option if freq.audio_option else 'No audio option'
                print(f"    - {freq.frequency / 1000000:.4f} MHz: {freq.name_tag} ({audio})")
            if len(frequencies_list) > 5:
                print(f"    ... and {len(frequencies_list) - 5} more")
            print(f"  Time: {step8_time*1000:.2f}ms | Queries: {step8_queries}")
        else:
            step8_time = 0
            step8_queries = 0
            print("\n[Step 8] No channel groups found, skipping frequencies")
    else:
        step7_time = 0
        step7_queries = 0
        step8_time = 0
        step8_queries = 0
        print("\n[Step 7-8] No agencies found, skipping channel groups and frequencies")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_time = step1_time + step2_time + step3_time + step4_time + step5_time + step6_time + step7_time + step8_time
    total_queries = step1_queries + step2_queries + step3_queries + step4_queries + step5_queries + step6_queries + step7_queries + step8_queries
    
    print(f"\nStep 1 (Find USA):        {step1_time*1000:7.2f}ms | {step1_queries:3d} queries")
    print(f"Step 2 (Find Alaska):     {step2_time*1000:7.2f}ms | {step2_queries:3d} queries")
    print(f"Step 3 (Find Juneau):     {step3_time*1000:7.2f}ms | {step3_queries:3d} queries")
    print(f"Step 4 (Agencies via M2M):  {step4_time*1000:7.2f}ms | {step4_queries:3d} queries")
    print(f"Step 5 (Agencies via State):{step5_time*1000:7.2f}ms | {step5_queries:3d} queries")
    print(f"Step 6 (API Path):        {step6_time*1000:7.2f}ms | {step6_queries:3d} queries")
    print(f"Step 7 (Channel Groups):  {step7_time*1000:7.2f}ms | {step7_queries:3d} queries")
    print(f"Step 8 (Frequencies):     {step8_time*1000:7.2f}ms | {step8_queries:3d} queries")
    print(f"\nTotal:                    {total_time*1000:7.2f}ms | {total_queries:3d} queries")
    print("\n" + "="*80)

if __name__ == '__main__':
    measure_retrieval()
