#!/usr/bin/env python
"""Check MongoDB indexes"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings
from pymongo import MongoClient, ASCENDING

mongo_config = settings.DATABASES.get('hpdb', {})
client_config = mongo_config.get('CLIENT', {})
host = client_config.get('host', 'mongodb://localhost:27017')

print(f'Connecting to MongoDB at: {host}')
client = MongoClient(host)
db = client[mongo_config.get('NAME', 'uniden_hpdb_db')]

print('\nIndexes on hpdb_hpdbagency_counties:')
try:
    for idx in db['hpdb_hpdbagency_counties'].list_indexes():
        print(f"  {idx['name']}: {idx['key']}")
except Exception as e:
    print(f"  Error: {e}")

print('\nIndexes on hpdb_hpdbagency_states:')
try:
    for idx in db['hpdb_hpdbagency_states'].list_indexes():
        print(f"  {idx['name']}: {idx['key']}")
except Exception as e:
    print(f"  Error: {e}")

# Try creating indexes
print('\n--- Creating indexes ---')
try:
    counties_collection = db['hpdb_hpdbagency_counties']
    counties_collection.create_index('county_id', name='county_id_idx')
    counties_collection.create_index('hpdbagency_id', name='hpdbagency_id_idx')
    counties_collection.create_index([('county_id', ASCENDING), ('hpdbagency_id', ASCENDING)], name='county_agency_idx')
    print('✓ Created indexes on hpdb_hpdbagency_counties')
except Exception as e:
    print(f'✗ Failed to create indexes: {e}')

try:
    states_collection = db['hpdb_hpdbagency_states']
    states_collection.create_index('state_id', name='state_id_idx')
    states_collection.create_index('hpdbagency_id', name='hpdbagency_id_idx')
    states_collection.create_index([('state_id', ASCENDING), ('hpdbagency_id', ASCENDING)], name='state_agency_idx')
    print('✓ Created indexes on hpdb_hpdbagency_states')
except Exception as e:
    print(f'✗ Failed to create indexes: {e}')

print('\n--- Verifying indexes ---')
print('\nIndexes on hpdb_hpdbagency_counties:')
for idx in db['hpdb_hpdbagency_counties'].list_indexes():
    print(f"  {idx['name']}: {idx['key']}")

print('\nIndexes on hpdb_hpdbagency_states:')
for idx in db['hpdb_hpdbagency_states'].list_indexes():
    print(f"  {idx['name']}: {idx['key']}")
