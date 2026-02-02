# Favorites Export Requirement

## Critical Requirement
**The system MUST be able to export fully functional f_list.cfg and f_*.hpd files that work on actual scanner hardware without any data loss.**

All record types and fields must be:
1. Parsed and stored in editable models
2. Available for frontend editing
3. Exportable back to source file format with 100% fidelity

## Record Types Found in Sample Data

From analysis of `SAMPLE_DATA/Uniden_Card/uniden/ubcdx36/favorites_lists/`:

### File Metadata (every file)
- `TargetModel` - Scanner model identifier
- `FormatVersion` - File format version
- `DQKs_Status` - Status field (purpose TBD)

### System Definitions
- `Conventional` - Conventional system parameters
- `Trunk` - Trunked system parameters
- `Site` - Trunked system site/tower locations

### Conventional Records (FM/AM)
- `C-Group` - Conventional department/channel group
- `C-Freq` - Conventional frequency/channel

### Trunked Records (Motorola/P25/EDACS)
- `T-Group` - Trunked department/talkgroup
- `TGID` - Talkgroup ID configuration
- `T-Freq` - Trunked frequency/channel

### Band Plans
- `BandPlan_P25` - P25 digital band plan
- `BandPlan_Mot` - Motorola band plan (not in all files but spec mentions it)

### Geographic Boundaries
- `Rectangle` - Geographic boundary definition (not in sample but in spec)

## Current Status

### ✅ Implemented
- F-List parsing (favorites list metadata from f_list.cfg)
- C-Group parsing (partial - missing many fields)
- C-Freq parsing (partial - missing many fields)

### ❌ Missing (CRITICAL)
- Conventional system records
- Trunk system records
- Site records
- T-Group records
- TGID records
- T-Freq records
- BandPlan_P25 records
- BandPlan_Mot records
- Rectangle records
- DQKs_Status records
- TargetModel/FormatVersion metadata handling

### 🔧 Incomplete Fields
Many fields are missing from existing C-Group and C-Freq models. Need full field mapping per spec.

## Implementation Plan

### Phase 1: Model Expansion
Create comprehensive models for ALL record types with ALL fields from spec

### Phase 2: Parser Enhancement
Update hpdb_parser.py to parse all record types and store in models

### Phase 3: Exporter Creation
Create export functionality that reconstructs:
- f_list.cfg (F-List records)
- f_*.hpd files (all system/group/frequency records)
With exact field order and format per spec

### Phase 4: Frontend Integration
Add "Export Favorites Folder" button to UI that:
- Generates zip file with f_list.cfg + all f_*.hpd files
- Files are ready to copy to scanner SD card
- Data is editable before export

## Success Criteria
✅ Parse sample data without losing any records
✅ Export back to files byte-for-byte identical (or functionally identical)
✅ Files work on actual scanner hardware
✅ All record types editable in frontend
✅ No data loss in round-trip (import → edit → export)

## Next Steps
1. Analyze spec to extract ALL fields for each record type
2. Create/update models
3. Create migration to add new models/fields
4. Update parser
5. Create exporter
6. Add frontend export button
