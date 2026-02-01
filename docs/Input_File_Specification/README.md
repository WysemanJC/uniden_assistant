# SDSx00 Input File Specification

Complete documentation for the Uniden SDSx00 series scanner file format (SDSx00_File_Specification_V1_03).

**Source**: SDSx00_File_Specification_V1_03.pdf (converted and restructured)

---

## Document Structure

### Core Specification
- [Global Parsing Rules](global_parsing_rules.md) — Encoding, delimiters, ID hierarchy, TGID formats, common parameters

### Record Type References
- [HPDB Records](record_types/hpdb_records.md) — HPDB database records (DateModified, StateInfo, CountyInfo, LM, etc.)
- [System Records](record_types/system_records.md) — Conventional and Trunk system definitions
- [Favorites Records](record_types/favorites_records.md) — C-Group, T-Group, C-Freq, TGID, T-Freq
- [Scan Configuration Records](record_types/scan_records.md) — Scan lists and configuration
- [Scanner/Profile Records](record_types/scanner_profile_records.md) — Scanner, ProductName, GlobalSetting, DisplayOption
- [Discovery Records](record_types/discovery_records.md) — ConvDiscovery, TrunkDiscovery

### Reference Tables
- [Service Types (FuncTagId)](reference_tables/service_types.md) — Standard and custom service type mappings (1-37, 208-218)
- [Frequency Options: CTCSS/DCS](reference_tables/frequency_options_ctcss_dcs.md) — Analog conventional channel options (50 CTCSS + 104 DCS)
- [Frequency Options: P25 NAC](reference_tables/frequency_options_p25.md) — P25 Network Access Codes (0x000-0xFFF)
- [Frequency Options: DMR Color Code](reference_tables/frequency_options_dmr.md) — DMR/MotoTRBO Color Codes (0-15)
- [Frequency Options: NXDN RAN/Area](reference_tables/frequency_options_nxdn.md) — NXDN Regional Area Network codes (0-63) and Area (0-1)
- [Display Area Options](reference_tables/display_options.md) — DispOptId mappings (Huge/Large/Small/Icon)
- [Display Colors](reference_tables/display_colors.md) — Complete color palette with hex codes and usage
- [Display Layout Modes](reference_tables/display_layouts.md) — DispLayoutId and ColorLayoutId mappings

---

## Quick Reference

### File Layout

#### MicroSD Root

```
microSD directory image

\ root
 + \ BCDx36HP
 |  |
 |  |  scanner.inf    Scanner Information (Ex. ESN, ModelName...)
 |  |  profile.cfg    Profile (owner's info, wx, location, ...) and Limit Search
 |  |  discvery.cfg   Conventional and Trunking Discovery
 |  |  app_data.cfg   Scanner settings data which scanner reads when scanner resumes last mode.
 |  |                PC application must delete this file, when it writes program data to scanner.
 |  |
 |  + \ audio
 |  |  |
 |  |  + \ inner_rec
 |  |  |  YYYY-MM-DD_hh-mm-ss.wav
 |  |  |
 |  |  + \ user_rec
 |  |     + \XXXXXXXXX  (hexadecimal time stamp name)
 |  |     |  YYYY-MM-DD_hh-mm-ss.wav
 |  |     |  YYYY-MM-DD_hh-mm-ss.wav
 |  |     |  YYYY-MM-DD_hh-mm-ss.wav
 |  |     + \XXXXXXXXX  (hexadecimal time stamp name)
 |  |        YYYY-MM-DD_hh-mm-ss.wav
 |  |        YYYY-MM-DD_hh-mm-ss.wav
 |  |        YYYY-MM-DD_hh-mm-ss.wav
 |  |
 |  + \ alert
 |  |  YYYY-MM-DD_hh-mm-ss.wav
 |  |  YYYY-MM-DD_hh-mm-ss.wav
 |  |  YYYY-MM-DD_hh-mm-ss.wav
 |  |
 |  + \ favorites_lists
 |  |  f_list.cfg
 |  |  f_000001.hpd
 |  |  f_000002.hpd
 |  |  f_000003.hpd
 |  |  favorites_xxxxxx.hpd (xxxxxx = 000001–999999)
 |  |  The name of file is managed by favorite_list.config.
 |  |
 |  + \ HPDB
 |  |  hpdb.cfg (State, County list, Locate me info)
 |  |  s_*.avd (avoid list (each state))
 |  |  s_*.hpd (Scan channel (each state))
 |  |
 |  + \ discovery
 |  |  + \ Conventional
 |  |  + \ Trunk
 |  |
 |  + \ firmware
 |  |  BCD536HP_Vx_xx_xx.scn
 |  |  BCD436HP_Vx_xx_xx.scn
 |  |  ZipTable_Vx_xx_xx.dat
 |  |  CityTable_Vx_xx_xx.dat
```

- `scanner.inf` — Scanner information ([Scanner record](record_types/scanner_profile_records.md#scanner))
- `profile.cfg` — Profile settings ([ProductName, GlobalSetting](record_types/scanner_profile_records.md))
- `app_data.cfg` — Runtime scan state ([Scan* records](record_types/scan_records.md))
- `favorites_lists/f_list.cfg` — Favorites list index ([F-List records](record_types/favorites_records.md#f-list))
- `favorites_lists/f_*.hpd` — Favorites list systems (same record types as HPDB)
- `HPDB/hpdb.cfg` — HPDB metadata ([DateModified, StateInfo, CountyInfo, LM](record_types/hpdb_records.md))
- `HPDB/s_*.hpd` — HPDB systems and channels ([System records](record_types/system_records.md))
- `*.avoid` — Avoid lists (Avoid records)
- `discovery.cfg` — Discovery settings ([ConvDiscovery, TrunkDiscovery](record_types/discovery_records.md))

### Common Field Types
- **Audio Option**: See [CTCSS/DCS](reference_tables/frequency_options_ctcss_dcs.md), [P25 NAC](reference_tables/frequency_options_p25.md), [DMR Color Code](reference_tables/frequency_options_dmr.md), [NXDN RAN/Area](reference_tables/frequency_options_nxdn.md)
- **FuncTagId**: See [Service Types](reference_tables/service_types.md)
- **DispOptId**: See [Display Area Options](reference_tables/display_options.md)
- **DispColorId**: See [Display Colors](reference_tables/display_colors.md)
- **DispLayoutId/ColorLayoutId**: See [Display Layout Modes](reference_tables/display_layouts.md)

### Record Type Categories
- **Parsed (implemented)**: 50+ record types
- **Unknown/Unspecified**: Circle (referenced but no explicit definition)

---

## Navigation Tips

1. Start with [Global Parsing Rules](global_parsing_rules.md) to understand the file format basics
2. Use the [Record Type References](#record-type-references) to find specific record definitions
3. Reference tables are linked from field descriptions throughout the documentation
4. Each reference table includes "Used by" sections showing where it's referenced
