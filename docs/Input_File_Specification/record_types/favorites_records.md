# Favorites Records

Favorites list record types (C-Group, T-Group, C-Freq, TGID, T-Freq, F-List, etc.).

[← Back to Main Index](../README.md)

---

## Favorites List Files

Favorites list data is stored in:

- `favorites_lists/f_list.cfg` — favorites list index (`F-List` records)
- `favorites_lists/f_*.hpd` — favorites list systems and channels (same record types as HPDB system files)

**Note**: In Favorites List `.hpd` files, **MyId** and **ParentId** may be **null or empty** (spec note).

---

## F-List (favorites_lists/f_list.cfg)

### F-List

**Observed in sample data**: `TargetModel` and `FormatVersion` appear as the first two records in `f_list.cfg`. The `F-List` record label is followed by a trailing space before the tab delimiter (`"F-List \t"`).

- **UserName**: ASCII string (Favorites List display name)
- **Filename**: string, include extension (Favorites List file name)
- **LocationControl**: `On` (=Yes) | `Off` (=No)
- **Monitor**: `On` | `Off`
- **QuickKey**: `Off` | `0-99` (favorites list quick key)
- **NumberTag**: `Off` | `0-99` (favorites list number tag)
- **StartupKey0–StartupKey9**: `Off` | `On` (startup configuration keys × 10)
- **S-Qkey_00–S-Qkey_99**: `Off` | `On` (startup quick keys × 100)

---

## Favorites List System Records (f_*.hpd)

Favorites list system files use the **same record formats** as HPDB system files:

- [Conventional](system_records.md#conventional)
- [Trunk](system_records.md#trunk)
- [Site](system_records.md#site)
- [C-Group](system_records.md#c-group)
- [T-Group](system_records.md#t-group)
- [C-Freq](system_records.md#c-freq)
- [TGID](system_records.md#tgid)
- [T-Freq](system_records.md#t-freq)
- [Rectangle](system_records.md#rectangle)
- [BandPlan_Mot](system_records.md#bandplan_mot)
- [BandPlan_P25](system_records.md#bandplan_p25)

---

## Avoid Records (*.avoid)

### Avoid

**Four format variants**:

1. **Channel avoid** (conventional frequency or TGID)
	- StateId: `StateId=xx`
	- SystemId: (integer)
	- DeptId: (integer)
	- ChannelId: (integer)

2. **Department avoid**
	- StateId: `StateId=xx`
	- SystemId: (integer)
	- DeptId: (integer)

3. **Site avoid**
	- StateId: `StateId=xx`
	- SystemId: (integer)
	- SiteId: `SiteId=xx`

4. **System avoid**
	- StateId: `StateId=xx`
	- SystemId: (integer)

---

## Related References

- [System Records](system_records.md)
- [Global Parsing Rules](../global_parsing_rules.md)

---

[← Back to Main Index](../README.md)
