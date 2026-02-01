# Conventional Channel Options (CTCSS/DCS)

Analog conventional channels use **Continuous Tone-Coded Squelch System (CTCSS)** or **Digital-Coded Squelch (DCS)** for sub-audio signaling to filter unwanted transmissions on shared frequencies.

[← Back to Main Index](../README.md)

---

## Used By

This reference table is used by the following record types:
- [C-Freq (Conventional Frequency)](../record_types/favorites_records.md#c-freq) — `TONE` field (analog mode)
- [ConvDiscovery](../record_types/discovery_records.md#convdiscovery) — Discovery folder naming

---

## Format Specifications

- **File Format**: `TONE=Cxxx.x` (CTCSS) or `TONE=Dxxx` (DCS)
- **Display Format**: `CTCSS xx.xHz` or `DCS xxx`
- **Discovery Folder String**: `Cxx.x` (CTCSS) or `Dxxx` (DCS)
- **Tone Lockout**: Append `,L/O` suffix when Tone Lockout is enabled (e.g., `TONE=C67.0,L/O`)

**Discovery Rules:**
- If no CTCSS/DCS is specified, Discovery shows "None"
- Tone Search is not persisted in Discovery folders

---

## CTCSS Tones (50 Frequencies)

CTCSS uses continuous sub-audible tones from 67.0 Hz to 254.1 Hz.

| Display Format | File Format | Discovery Folder String |
|---|---|---|
| (null) | (null) | None |
| Tone Search | TONE=Srch | Tone Search |
| CTCSS 67.0Hz | TONE=C67.0 | C67.0 |
| CTCSS 69.3Hz | TONE=C69.3 | C69.3 |
| CTCSS 71.9Hz | TONE=C71.9 | C71.9 |
| CTCSS 74.4Hz | TONE=C74.4 | C74.4 |
| CTCSS 77.0Hz | TONE=C77.0 | C77.0 |
| CTCSS 79.7Hz | TONE=C79.7 | C79.7 |
| CTCSS 82.5Hz | TONE=C82.5 | C82.5 |
| CTCSS 85.4Hz | TONE=C85.4 | C85.4 |
| CTCSS 88.5Hz | TONE=C88.5 | C88.5 |
| CTCSS 91.5Hz | TONE=C91.5 | C91.5 |
| CTCSS 94.8Hz | TONE=C94.8 | C94.8 |
| CTCSS 97.4Hz | TONE=C97.4 | C97.4 |
| CTCSS 100.0Hz | TONE=C100.0 | C100.0 |
| CTCSS 103.5Hz | TONE=C103.5 | C103.5 |
| CTCSS 107.2Hz | TONE=C107.2 | C107.2 |
| CTCSS 110.9Hz | TONE=C110.9 | C110.9 |
| CTCSS 114.8Hz | TONE=C114.8 | C114.8 |
| CTCSS 118.8Hz | TONE=C118.8 | C118.8 |
| CTCSS 123.0Hz | TONE=C123.0 | C123.0 |
| CTCSS 127.3Hz | TONE=C127.3 | C127.3 |
| CTCSS 131.8Hz | TONE=C131.8 | C131.8 |
| CTCSS 136.5Hz | TONE=C136.5 | C136.5 |
| CTCSS 141.3Hz | TONE=C141.3 | C141.3 |
| CTCSS 146.2Hz | TONE=C146.2 | C146.2 |
| CTCSS 151.4Hz | TONE=C151.4 | C151.4 |
| CTCSS 156.7Hz | TONE=C156.7 | C156.7 |
| CTCSS 159.8Hz | TONE=C159.8 | C159.8 |
| CTCSS 162.2Hz | TONE=C162.2 | C162.2 |
| CTCSS 165.5Hz | TONE=C165.5 | C165.5 |
| CTCSS 167.9Hz | TONE=C167.9 | C167.9 |
| CTCSS 171.3Hz | TONE=C171.3 | C171.3 |
| CTCSS 173.8Hz | TONE=C173.8 | C173.8 |
| CTCSS 177.3Hz | TONE=C177.3 | C177.3 |
| CTCSS 179.9Hz | TONE=C179.9 | C179.9 |
| CTCSS 183.5Hz | TONE=C183.5 | C183.5 |
| CTCSS 186.2Hz | TONE=C186.2 | C186.2 |
| CTCSS 189.9Hz | TONE=C189.9 | C189.9 |
| CTCSS 192.8Hz | TONE=C192.8 | C192.8 |
| CTCSS 196.6Hz | TONE=C196.6 | C196.6 |
| CTCSS 199.5Hz | TONE=C199.5 | C199.5 |
| CTCSS 203.5Hz | TONE=C203.5 | C203.5 |
| CTCSS 206.5Hz | TONE=C206.5 | C206.5 |
| CTCSS 210.7Hz | TONE=C210.7 | C210.7 |
| CTCSS 218.1Hz | TONE=C218.1 | C218.1 |
| CTCSS 225.7Hz | TONE=C225.7 | C225.7 |
| CTCSS 229.1Hz | TONE=C229.1 | C229.1 |
| CTCSS 233.6Hz | TONE=C233.6 | C233.6 |
| CTCSS 241.8Hz | TONE=C241.8 | C241.8 |
| CTCSS 250.3Hz | TONE=C250.3 | C250.3 |
| CTCSS 254.1Hz | TONE=C254.1 | C254.1 |

---

## DCS Codes (104 Codes)

DCS uses digital squelch codes from 006 to 754 (octal-based numbering).

| Display Format | File Format | Discovery Folder String |
|---|---|---|
| DCS 006 | TONE=D006 | D006 |
| DCS 007 | TONE=D007 | D007 |
| DCS 015 | TONE=D015 | D015 |
| DCS 017 | TONE=D017 | D017 |
| DCS 021 | TONE=D021 | D021 |
| DCS 023 | TONE=D023 | D023 |
| DCS 025 | TONE=D025 | D025 |
| DCS 026 | TONE=D026 | D026 |
| DCS 031 | TONE=D031 | D031 |
| DCS 032 | TONE=D032 | D032 |
| DCS 036 | TONE=D036 | D036 |
| DCS 043 | TONE=D043 | D043 |
| DCS 047 | TONE=D047 | D047 |
| DCS 050 | TONE=D050 | D050 |
| DCS 051 | TONE=D051 | D051 |
| DCS 053 | TONE=D053 | D053 |
| DCS 054 | TONE=D054 | D054 |
| DCS 065 | TONE=D065 | D065 |
| DCS 071 | TONE=D071 | D071 |
| DCS 072 | TONE=D072 | D072 |
| DCS 073 | TONE=D073 | D073 |
| DCS 074 | TONE=D074 | D074 |
| DCS 114 | TONE=D114 | D114 |
| DCS 115 | TONE=D115 | D115 |
| DCS 116 | TONE=D116 | D116 |
| DCS 122 | TONE=D122 | D122 |
| DCS 125 | TONE=D125 | D125 |
| DCS 131 | TONE=D131 | D131 |
| DCS 132 | TONE=D132 | D132 |
| DCS 134 | TONE=D134 | D134 |
| DCS 141 | TONE=D141 | D141 |
| DCS 143 | TONE=D143 | D143 |
| DCS 145 | TONE=D145 | D145 |
| DCS 152 | TONE=D152 | D152 |
| DCS 155 | TONE=D155 | D155 |
| DCS 156 | TONE=D156 | D156 |
| DCS 162 | TONE=D162 | D162 |
| DCS 165 | TONE=D165 | D165 |
| DCS 172 | TONE=D172 | D172 |
| DCS 174 | TONE=D174 | D174 |
| DCS 205 | TONE=D205 | D205 |
| DCS 212 | TONE=D212 | D212 |
| DCS 214 | TONE=D214 | D214 |
| DCS 223 | TONE=D223 | D223 |
| DCS 225 | TONE=D225 | D225 |
| DCS 226 | TONE=D226 | D226 |
| DCS 243 | TONE=D243 | D243 |
| DCS 244 | TONE=D244 | D244 |
| DCS 245 | TONE=D245 | D245 |
| DCS 246 | TONE=D246 | D246 |
| DCS 251 | TONE=D251 | D251 |
| DCS 252 | TONE=D252 | D252 |
| DCS 255 | TONE=D255 | D255 |
| DCS 261 | TONE=D261 | D261 |
| DCS 263 | TONE=D263 | D263 |
| DCS 265 | TONE=D265 | D265 |
| DCS 266 | TONE=D266 | D266 |
| DCS 271 | TONE=D271 | D271 |
| DCS 274 | TONE=D274 | D274 |
| DCS 306 | TONE=D306 | D306 |
| DCS 311 | TONE=D311 | D311 |
| DCS 315 | TONE=D315 | D315 |
| DCS 325 | TONE=D325 | D325 |
| DCS 331 | TONE=D331 | D331 |
| DCS 332 | TONE=D332 | D332 |
| DCS 343 | TONE=D343 | D343 |
| DCS 346 | TONE=D346 | D346 |
| DCS 351 | TONE=D351 | D351 |
| DCS 356 | TONE=D356 | D356 |
| DCS 364 | TONE=D364 | D364 |
| DCS 365 | TONE=D365 | D365 |
| DCS 371 | TONE=D371 | D371 |
| DCS 411 | TONE=D411 | D411 |
| DCS 412 | TONE=D412 | D412 |
| DCS 413 | TONE=D413 | D413 |
| DCS 423 | TONE=D423 | D423 |
| DCS 431 | TONE=D431 | D431 |
| DCS 432 | TONE=D432 | D432 |
| DCS 445 | TONE=D445 | D445 |
| DCS 446 | TONE=D446 | D446 |
| DCS 452 | TONE=D452 | D452 |
| DCS 454 | TONE=D454 | D454 |
| DCS 455 | TONE=D455 | D455 |
| DCS 462 | TONE=D462 | D462 |
| DCS 464 | TONE=D464 | D464 |
| DCS 465 | TONE=D465 | D465 |
| DCS 466 | TONE=D466 | D466 |
| DCS 503 | TONE=D503 | D503 |
| DCS 506 | TONE=D506 | D506 |
| DCS 516 | TONE=D516 | D516 |
| DCS 523 | TONE=D523 | D523 |
| DCS 526 | TONE=D526 | D526 |
| DCS 532 | TONE=D532 | D532 |
| DCS 546 | TONE=D546 | D546 |
| DCS 565 | TONE=D565 | D565 |
| DCS 606 | TONE=D606 | D606 |
| DCS 612 | TONE=D612 | D612 |
| DCS 624 | TONE=D624 | D624 |
| DCS 627 | TONE=D627 | D627 |
| DCS 631 | TONE=D631 | D631 |
| DCS 632 | TONE=D632 | D632 |
| DCS 654 | TONE=D654 | D654 |
| DCS 662 | TONE=D662 | D662 |
| DCS 664 | TONE=D664 | D664 |
| DCS 703 | TONE=D703 | D703 |
| DCS 712 | TONE=D712 | D712 |
| DCS 723 | TONE=D723 | D723 |
| DCS 731 | TONE=D731 | D731 |
| DCS 732 | TONE=D732 | D732 |
| DCS 734 | TONE=D734 | D734 |
| DCS 743 | TONE=D743 | D743 |
| DCS 754 | TONE=D754 | D754 |

---

## Summary

**Total Options**: 50 CTCSS tones + 104 DCS codes = **154 analog channel options**

**Usage Pattern:**
- Conventional FM systems use CTCSS for analog voice
- CTCSS provides basic privacy and interference rejection
- DCS offers better interference rejection than CTCSS
- Both systems are mutually exclusive (cannot use both simultaneously)

---

[← Back to Main Index](../README.md)
