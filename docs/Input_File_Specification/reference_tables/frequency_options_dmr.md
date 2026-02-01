# DMR Frequency Options (Color Code)

DMR/MotoTRBO systems use **Color Code** (0–15) for channel access control and interference rejection.

[← Back to Main Index](../README.md)

---

## Used By

This reference table is used by the following record types:
- [C-Freq (Conventional Frequency)](../record_types/favorites_records.md#c-freq) — `ColorCode` field (DMR mode)
- [TGID (Talkgroup ID)](../record_types/favorites_records.md#tgid) — `ColorCode` field (DMR trunked systems)
- [TrunkDiscovery](../record_types/discovery_records.md#trunkdiscovery) — Discovery folder naming

---

## Format Specifications

- **File Format**: `ColorCode=x` (decimal, 0–15) or just `x`
- **Display Format**: `Color Code x` (single digit or two digits)
- **Discovery Folder String**: `ColorCodex` (e.g., `ColorCode1`)
- **Value Range**: 0–15 (16 codes total)

**Discovery Rules:**
- Color Code always exists in Discovery folder names for DMR systems
- Color Code Search (`Srch`) is not persisted in Discovery folders
- Discovery shows "None" only if system detection fails

---

## Color Code Table

All 16 DMR Color Codes (0–15):

| Display Format | File Format | Discovery Folder String | Notes |
|---|---|---|---|
| Color Code Search | Srch | (not persisted) | Scanner searches for any Color Code |
| Color Code 0 | 0 | ColorCode0 | Minimum value |
| Color Code 1 | 1 | ColorCode1 | Common default value |
| Color Code 2 | 2 | ColorCode2 | |
| Color Code 3 | 3 | ColorCode3 | |
| Color Code 4 | 4 | ColorCode4 | |
| Color Code 5 | 5 | ColorCode5 | |
| Color Code 6 | 6 | ColorCode6 | |
| Color Code 7 | 7 | ColorCode7 | |
| Color Code 8 | 8 | ColorCode8 | |
| Color Code 9 | 9 | ColorCode9 | |
| Color Code 10 | 10 | ColorCode10 | |
| Color Code 11 | 11 | ColorCode11 | |
| Color Code 12 | 12 | ColorCode12 | |
| Color Code 13 | 13 | ColorCode13 | |
| Color Code 14 | 14 | ColorCode14 | |
| Color Code 15 | 15 | ColorCode15 | Maximum value |

---

## Summary

**Total Codes**: **16 Color Codes** (0–15)

**Usage Pattern:**
- Used by all DMR (Digital Mobile Radio) systems including MotoTRBO
- Color Code must match between transmitter and receiver for communication
- Different agencies/repeaters use different Color Codes to prevent interference on shared frequencies
- Color Code is always transmitted with DMR digital signals

**Common Assignments:**
- Color Code 1 — Most common default value for DMR repeaters
- Color Code 0 — Sometimes used for simplex or direct mode
- Color Codes 2–15 — Assigned to avoid interference with nearby repeaters

**Technical Details:**
- Color Code is part of the DMR CACH (Common Announcement Channel)
- Prevents co-channel interference in DMR Tier II systems
- Similar function to CTCSS/DCS in analog systems, but for digital

---

[← Back to Main Index](../README.md)
