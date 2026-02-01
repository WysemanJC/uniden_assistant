# Service Types Reference (FuncTagId)

Service types classify radio services by function. This table maps `FuncTagId` values to their service type names.

**Value Range**: 1–37 (standard), 208–218 (custom)

[← Back to Main Index](../README.md)

---

## Used By

This reference table is used by the following record types:
- [C-Freq (Conventional Frequency)](../record_types/favorites_records.md#c-freq) — `FuncTagId` field
- [TGID (Talkgroup ID)](../record_types/favorites_records.md#tgid) — `FuncTagId` field

---

## Standard Service Types (1-37)

| FuncTagId | Service Type | Description |
|---|---|---|
| 1 | Multi-Dispatch | Multi-agency dispatch |
| 2 | Law Dispatch | Law enforcement dispatch |
| 3 | Fire Dispatch | Fire department dispatch |
| 4 | EMS Dispatch | Emergency medical services dispatch |
| 5 | (reserved) | Not used |
| 6 | Multi-Tac | Multi-agency tactical |
| 7 | Law Tac | Law enforcement tactical |
| 8 | Fire-Tac | Fire department tactical |
| 9 | EMS-Tac | Emergency medical services tactical |
| 10 | (reserved) | Not used |
| 11 | Interop | Interoperability channels |
| 12 | Hospital | Hospital communications |
| 13 | Ham | Amateur radio |
| 14 | Public Works | Public works/utilities dispatch |
| 15 | Aircraft | Aircraft communications |
| 16 | Federal | Federal agency communications |
| 17 | Business | Business/commercial |
| 18–19 | (reserved) | Not used |
| 20 | Railroad | Railroad operations |
| 21 | Other | Miscellaneous/unclassified |
| 22 | Multi-Talk | Multi-agency talk/simplex |
| 23 | Law Talk | Law enforcement talk/simplex |
| 24 | Fire-Talk | Fire department talk/simplex |
| 25 | EMS-Talk | Emergency medical services talk/simplex |
| 26 | Transportation | Transportation/transit |
| 27–28 | (reserved) | Not used |
| 29 | Emergency Ops | Emergency operations center |
| 30 | Military | Military communications |
| 31 | Media | News/media |
| 32 | Schools | School/campus security |
| 33 | Security | Private security |
| 34 | Utilities | Utility companies |
| 35–36 | (reserved) | Not used |
| 37 | Corrections | Corrections/jail/prison |

---

## Custom Service Types (208-218)

| FuncTagId | Service Type | Description |
|---|---|---|
| 208 | Custom 1 | User-definable service type 1 |
| 209 | Custom 2 | User-definable service type 2 |
| 210 | Custom 3 | User-definable service type 3 |
| 211 | Custom 4 | User-definable service type 4 |
| 212 | Custom 5 | User-definable service type 5 |
| 213 | Custom 6 | User-definable service type 6 |
| 214 | Custom 7 | User-definable service type 7 |
| 215 | Custom 8 | User-definable service type 8 |
| 216 | Racing Officials | Racing event officials |
| 217 | Racing Teams | Racing teams communications |

---

## Usage Notes

- **File Format**: Stored as decimal integer (e.g., `FuncTagId=2` for Law Dispatch)
- **Display**: Shows service type name in scanner UI
- **Custom Types**: Can be renamed by user in scanner settings
- **Reserved Values**: 5, 10, 18, 19, 27, 28, 35, 36 are not assigned

---

[← Back to Main Index](../README.md)
