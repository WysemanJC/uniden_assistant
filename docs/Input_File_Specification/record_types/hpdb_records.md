# HPDB Records

HPDB database records stored in `HPDB/hpdb.cfg` (TargetModel, FormatVersion, DateModified, StateInfo, CountyInfo, LM, LM_Frequency, etc.).

[← Back to Main Index](../README.md)

---

## Records in hpdb.cfg

**Observed in sample data**: `TargetModel` and `FormatVersion` appear in `HPDB/hpdb.cfg` as the first records. They also appear in `HPDB/s_*.hpd` files (see [System Records](system_records.md)).

### TargetModel

**Format**: `TargetModel\tModelName`

---

### FormatVersion

**Format**: `FormatVersion\tVersion`

### DateModified

**Format**: `DateModified\tTimeStamp`

- **TimeStamp**: `MM/DD/YYYY hh:mm:ss`

---

### StateInfo

**Format**: `StateInfo\tStateId\tCountryId\tNameTag\tShortName`

- **StateId**: `StateId=xx` (integer)
- **CountryId**: `CountryId=xx` (integer)
- **NameTag**: ASCII string, max 64 chars
- **ShortName**: 2-letter code (e.g., AL, TX)

---

### CountyInfo

**Format**: `CountyInfo\tCountyId\tStateId\tNameTag`

- **CountyId**: `CountyId=xx` (integer)
- **StateId**: `StateId=xx` (integer)
- **NameTag**: ASCII string, max 64 chars

---

### LM

**Format**: `LM\tStateId\tCountyId\tTrunkId\tSiteId\tLM_SystemID\tLM_SiteID\tLatitude\tLongitude`

- **StateId**: `StateId=xx` (integer)
- **CountyId**: `CountyId=xx` (integer)
- **TrunkId**: `TrunkId=xx` (integer)
- **SiteId**: `SiteId=xx` (integer)
- **LM_SystemID**: string (Locate Me system identifier)
- **LM_SiteID**: string (Locate Me site identifier)
- **Latitude**: degree format, up to 6 decimals
- **Longitude**: degree format, up to 6 decimals
- **Note**: First sort key = `LM_SystemID`; second sort key = `LM_SiteID`

---

### LM_Frequency

**Format**: `LM_Frequency\tFrequency\tReserve\tLmTypeArray`

- **Frequency**: Hz integer (1 = 1 Hz)
- **Reserve**: (reserved field)
- **LmTypeArray**: bit flags encoding detected system types
	- Bit 0 (LSB): Motorola (1 = detected, 0 = not detected)
	- Bit 1: P25 Standard (1 = detected, 0 = not detected)
	- Bit 2: P25 X2-TDMA (1 = detected, 0 = not detected)

---

## Related References

- [System Records](system_records.md) — HPDB systems and channels in `s_*.hpd`
- [Global Parsing Rules](../global_parsing_rules.md)

---

[← Back to Main Index](../README.md)
