# P25 Frequency Options (NAC)

P25 digital systems use **Network Access Code (NAC)** for channel identification and access control. NAC values range from 0x000 to 0xFFF (4096 total codes).

[← Back to Main Index](../README.md)

---

## Used By

This reference table is used by the following record types:
- [C-Freq (Conventional Frequency)](../record_types/favorites_records.md#c-freq) — `NAC` field (P25 mode)
- [TGID (Talkgroup ID)](../record_types/favorites_records.md#tgid) — `NAC` field (P25 trunked systems)
- [TrunkDiscovery](../record_types/discovery_records.md#trunkdiscovery) — Discovery folder naming

---

## Format Specifications

- **File Format**: `NAC=xxx` (hexadecimal value, 0–FFF)
- **Display Format**: `NAC xxx` (3-digit hex, zero-padded)
- **Discovery Folder String**: `Nxxx` (e.g., `N293` for NAC 0x293)
- **Value Range**: 0x000–0xFFF (4096 codes)

**Discovery Rules:**
- NAC always exists in Discovery folder names for P25 systems
- NAC Search (`NAC=Srch`) is not persisted in Discovery folders
- Discovery shows "None" only if system detection fails

---

## NAC Code Range

NAC codes are stored and displayed in hexadecimal format (0–F for each digit).

| Display Format | File Format | Discovery Folder String | Notes |
|---|---|---|---|
| NAC Search | NAC=Srch | (not persisted) | Scanner searches for any NAC |
| NAC 000 | NAC=0 | N0 | Minimum NAC value |
| NAC 001 | NAC=1 | N1 | |
| NAC 002 | NAC=2 | N2 | |
| NAC 003 | NAC=3 | N3 | |
| NAC 004 | NAC=4 | N4 | |
| NAC 005 | NAC=5 | N5 | |
| NAC 006 | NAC=6 | N6 | |
| NAC 007 | NAC=7 | N7 | |
| NAC 008 | NAC=8 | N8 | |
| NAC 009 | NAC=9 | N9 | |
| NAC 00A | NAC=A | NA | Hex digit A (10 decimal) |
| NAC 00B | NAC=B | NB | Hex digit B (11 decimal) |
| NAC 00C | NAC=C | NC | Hex digit C (12 decimal) |
| NAC 00D | NAC=D | ND | Hex digit D (13 decimal) |
| NAC 00E | NAC=E | NE | Hex digit E (14 decimal) |
| NAC 00F | NAC=F | NF | Hex digit F (15 decimal) |
| NAC 010 | NAC=10 | N10 | |
| NAC 011 | NAC=11 | N11 | |
| NAC 012 | NAC=12 | N12 | |
| ... | ... | ... | *Pattern continues through all hex values* |
| NAC 0FF | NAC=FF | NFF | |
| NAC 100 | NAC=100 | N100 | |
| NAC 293 | NAC=293 | N293 | Common example value |
| NAC 2F0 | NAC=2F0 | N2F0 | |
| ... | ... | ... | *Pattern continues* |
| NAC FFE | NAC=FFE | NFFE | |
| NAC FFF | NAC=FFF | NFFF | Maximum NAC value |

---

## Summary

**Total Codes**: **4096 NAC codes** (0x000–0xFFF in hexadecimal)

**Usage Pattern:**
- Used by all P25 Phase I and Phase II systems
- NAC must match between transmitter and receiver for communication
- Different agencies/systems typically use different NAC values to prevent interference
- NAC is always transmitted with P25 digital signals

**Common NAC Values:**
- `0x293` (N293) — Frequently used by many P25 systems
- `0xF00`–`0xFFF` — Often reserved for interoperability channels
- `0x000` — Sometimes used for unencrypted emergency channels

---

[← Back to Main Index](../README.md)
