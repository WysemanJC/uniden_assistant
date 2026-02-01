#!/usr/bin/env python3
"""
Verify and create MongoDB indexes on M2M join tables
"""
import os
import sys
import django
from pymongo import MongoClient, ASCENDING

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
django.setup()

from django.conf import settings

# Get MongoDB connection from Django settings
host = settings.DATABASES['hpdb']['HOST']
db_name = settings.DATABASES['hpdb']['NAME']

print(f"Connecting to MongoDB at {host}")
print(f"Database: {db_name}")

client = MongoClient(host)
db = client[db_name]

# Collections
counties_collection = db['hpdb_hpdbagency_counties']
states_collection = db['hpdb_hpdbagency_states']

print("\n=== EXISTING INDEXES ===")

print("\nhpdb_hpdbagency_counties indexes:")
for index in counties_collection.list_indexes():
    print(f"  - {index['name']}: {index['key']}")

print("\nhpdb_hpdbagency_states indexes:")
for index in states_collection.list_indexes():
    print(f"  - {index['name']}: {index['key']}")

# Define indexes to create
counties_indexes = [
    ('county_id_idx', [('county_id', ASCENDING)]),
    ('hpdbagency_id_idx', [('hpdbagency_id', ASCENDING)]),
    ('county_agency_idx', [('county_id', ASCENDING), ('hpdbagency_id', ASCENDING)])
]

states_indexes = [
    ('state_id_idx', [('state_id', ASCENDING)]),
    ('hpdbagency_id_idx', [('hpdbagency_id', ASCENDING)]),
    ('state_agency_idx', [('state_id', ASCENDING), ('hpdbagency_id', ASCENDING)])
]

print("\n=== CREATING INDEXES ===")

# Create indexes on counties collection
print("\nCreating indexes on hpdb_hpdbagency_counties:")
for index_name, keys in counties_indexes:
    try:
        result = counties_collection.create_index(keys, name=index_name, background=False)
        print(f"  ✓ Created index: {index_name} -> {result}")
    except Exception as e:
        print(f"  ✗ Error creating {index_name}: {e}")

# Create indexes on states collection
print("\nCreating indexes on hpdb_hpdbagency_states:")
for index_name, keys in states_indexes:
    try:
        result = states_collection.create_index(keys, name=index_name, background=False)
        print(f"  ✓ Created index: {index_name} -> {result}")
    except Exception as e:
        print(f"  ✗ Error creating {index_name}: {e}")

print("\n=== FINAL INDEX LIST ===")

print("\nhpdb_hpdbagency_counties indexes:")
for index in counties_collection.list_indexes():
    print(f"  - {index['name']}: {index['key']}")

print("\nhpdb_hpdbagency_states indexes:")
for index in states_collection.list_indexes():
    print(f"  - {index['name']}: {index['key']}")

# Get collection stats
print("\n=== COLLECTION STATS ===")
print(f"\nhpdb_hpdbagency_counties: {counties_collection.count_documents({})} documents")
print(f"hpdb_hpdbagency_states: {states_collection.count_documents({})} documents")

client.close()
print("\n✓ Done!")
