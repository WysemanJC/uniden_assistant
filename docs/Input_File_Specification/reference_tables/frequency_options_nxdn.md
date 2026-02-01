# NXDN Frequency Options (RAN/Area)

NXDN systems use **RAN (Regional Area Network, 0–63)** and optional **Area code (0–1)** for channel identification and access control.

[← Back to Main Index](../README.md)

---

## Used By

This reference table is used by the following record types:
- [C-Freq (Conventional Frequency)](../record_types/favorites_records.md#c-freq) — `RAN` or `Area` field (NXDN mode)
- [TGID (Talkgroup ID)](../record_types/favorites_records.md#tgid) — `RAN` or `Area` field (NXDN trunked systems)
- [TrunkDiscovery](../record_types/discovery_records.md#trunkdiscovery) — Discovery folder naming

---

## Format Specifications

- **File Format**: `RAN=xx` (decimal, 0–63) or `Area=x` (0–1)
- **Display Format**: `RAN xx` or `Area x`
- **Discovery Folder String**: `RANxx` (e.g., `RAN15`) or `Areax` (e.g., `Area0`)
- **Value Range**: RAN 0–63 (64 codes), Area 0–1 (2 codes)

**Discovery Rules:**
- RAN always exists in Discovery folder names for NXDN systems
- RAN/Area Search (`Srch`) is not persisted in Discovery folders
- Area code is optional and system-dependent

---

## Area Codes

NXDN systems may use an optional Area identifier (2 values):

| Display Format | File Format | Discovery Folder String | Notes |
|---|---|---|---|
| RAN/Area Search | Srch | (not persisted) | Scanner searches for any RAN/Area |
| Area 0 | Area=0 | Area0 | Area identifier 0 |
| Area 1 | Area=1 | Area1 | Area identifier 1 |

---

## RAN Codes

NXDN Regional Area Network codes (64 values, 0–63):

| Display Format | File Format | Discovery Folder String | Notes |
|---|---|---|---|
| RAN 0 | RAN=0 | RAN0 | Minimum RAN value |
| RAN 1 | RAN=1 | RAN1 | Common default value |
| RAN 2 | RAN=2 | RAN2 | |
| RAN 3 | RAN=3 | RAN3 | |
| RAN 4 | RAN=4 | RAN4 | |
| RAN 5 | RAN=5 | RAN5 | |
| RAN 6 | RAN=6 | RAN6 | |
| RAN 7 | RAN=7 | RAN7 | |
| RAN 8 | RAN=8 | RAN8 | |
| RAN 9 | RAN=9 | RAN9 | |
| RAN 10 | RAN=10 | RAN10 | |
| RAN 11 | RAN=11 | RAN11 | |
| RAN 12 | RAN=12 | RAN12 | |
| RAN 13 | RAN=13 | RAN13 | |
| RAN 14 | RAN=14 | RAN14 | |
| RAN 15 | RAN=15 | RAN15 | |
| RAN 16 | RAN=16 | RAN16 | |
| RAN 17 | RAN=17 | RAN17 | |
| RAN 18 | RAN=18 | RAN18 | |
| RAN 19 | RAN=19 | RAN19 | |
| RAN 20 | RAN=20 | RAN20 | |
| RAN 21 | RAN=21 | RAN21 | |
| RAN 22 | RAN=22 | RAN22 | |
| RAN 23 | RAN=23 | RAN23 | |
| RAN 24 | RAN=24 | RAN24 | |
| RAN 25 | RAN=25 | RAN25 | |
| RAN 26 | RAN=26 | RAN26 | |
| RAN 27 | RAN=27 | RAN27 | |
| RAN 28 | RAN=28 | RAN28 | |
| RAN 29 | RAN=29 | RAN29 | |
| RAN 30 | RAN=30 | RAN30 | |
| RAN 31 | RAN=31 | RAN31 | |
| RAN 32 | RAN=32 | RAN32 | |
| RAN 33 | RAN=33 | RAN33 | |
| RAN 34 | RAN=34 | RAN34 | |
| RAN 35 | RAN=35 | RAN35 | |
| RAN 36 | RAN=36 | RAN36 | |
| RAN 37 | RAN=37 | RAN37 | |
| RAN 38 | RAN=38 | RAN38 | |
| RAN 39 | RAN=39 | RAN39 | |
| RAN 40 | RAN=40 | RAN40 | |
| RAN 41 | RAN=41 | RAN41 | |
| RAN 42 | RAN=42 | RAN42 | |
| RAN 43 | RAN=43 | RAN43 | |
| RAN 44 | RAN=44 | RAN44 | |
| RAN 45 | RAN=45 | RAN45 | |
| RAN 46 | RAN=46 | RAN46 | |
| RAN 47 | RAN=47 | RAN47 | |
| RAN 48 | RAN=48 | RAN48 | |
| RAN 49 | RAN=49 | RAN49 | |
| RAN 50 | RAN=50 | RAN50 | |
| RAN 51 | RAN=51 | RAN51 | |
| RAN 52 | RAN=52 | RAN52 | |
| RAN 53 | RAN=53 | RAN53 | |
| RAN 54 | RAN=54 | RAN54 | |
| RAN 55 | RAN=55 | RAN55 | |
| RAN 56 | RAN=56 | RAN56 | |
| RAN 57 | RAN=57 | RAN57 | |
| RAN 58 | RAN=58 | RAN58 | |
| RAN 59 | RAN=59 | RAN59 | |
| RAN 60 | RAN=60 | RAN60 | |
| RAN 61 | RAN=61 | RAN61 | |
| RAN 62 | RAN=62 | RAN62 | |
| RAN 63 | RAN=63 | RAN63 | Maximum RAN value |

---

## Summary

**Total Codes**: **64 RAN codes** (0–63) + **2 Area codes** (0–1) = **66 total identifiers**

**Usage Pattern:**
- Used by all NXDN digital systems
- RAN must match between transmitter and receiver for communication
- Different agencies/systems use different RAN values to prevent interference
- Area code provides additional geographic or organizational grouping (optional)
- RAN is always transmitted with NXDN digital signals

**Common Assignments:**
- RAN 1 — Common default value for NXDN systems
- RAN 0 — Sometimes used for simplex or direct mode
- RANs 2–63 — Assigned to avoid interference with nearby systems

**Technical Details:**
- RAN provides access control similar to NAC in P25
- Area code can provide additional hierarchical organization
- NXDN systems may use RAN alone or RAN + Area code together

---

[← Back to Main Index](../README.md)
