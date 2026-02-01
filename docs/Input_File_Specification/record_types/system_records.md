# System Records

Conventional and trunked system definitions.

[← Back to Main Index](../README.md)

---

## Records in s_*.hpd

**Observed in sample data**: `TargetModel` and `FormatVersion` appear at the top of `HPDB/s_*.hpd` files and also in Favorites `f_*.hpd` files.

### TargetModel

**Format**: `TargetModel\tModelName`

**Parameters**:
- **ModelName**: `BCDx36HP` (for BCD436HP/BCD536HP models)

**Note**: Cannot be omitted.

---

### FormatVersion

**Format**: `FormatVersion\tVersion`

**Parameters**:
- **Version**: Version number (e.g., `1.03`)

**Note**: Cannot be omitted.

---

### Conventional

Conventional System Parameter

**Format**: `Conventional\tMyId\tParentId\tNameTag\tAvoid\tReserve\tSystemType\tQuickKey\tNumberTag\tSystemHoldTime\tAnalogAGC\tDigitalAGC\tDigitalWaitingTime\tDigitalThresholdMode\tDigitalThresholdLevel`

**Parameters**:
- **MyId**: `CountyId=xx` or `AgencyId=xx`
- **ParentId**: `StateId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Reserve**: Reserved field (empty)
- **SystemType**: System type identifier
- **QuickKey**: `Off` | `0-99`
- **NumberTag**: `Off` | `0-999`
- **SystemHoldTime**: `0-255` (seconds)
- **AnalogAGC**: `Off` | `On` (Automatic Gain Control)
- **DigitalAGC**: `Off` | `On`
- **DigitalWaitingTime**: `0-1000` (milliseconds, 1 = 1ms)
- **DigitalThresholdMode**: `Auto` | `Manual` | `Default`
- **DigitalThresholdLevel**: `5-13`

---

### Trunk

Trunked System Parameter

**Format**: `Trunk\tMyId\tParentId\tNameTag\tAvoid\tReserve\tSystemType\tIDSearch\tAlertTone\tAlertVolume\tStatusBit\tNAC\tQuickKey\tNumberTag\tSiteHoldTime\tAnalogAGC\tDigitalAGC\tEndCode\tPriorityIDScan\tAlertColor\tAlertPattern\tTGIDFormat`

**Parameters**:
- **MyId**: `TrunkId=xx`
- **ParentId**: `StateId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Reserve**: Reserved field (empty)
- **SystemType**: 
  - `Conventional`
  - `Motorola`
  - `Edacs`
  - `Scat` (reserve parameter)
  - `Ltr`
  - `P25Standard` (P25 Phase I & II)
  - `P25OneFrequency`
  - `P25X2_TDMA`
  - `MotoTrbo`
  - `DmrOneFrequency`
  - `Nxdn`
  - `NxdnOneFrequency`
- **IDSearch**: `Off` | `On`
- **AlertTone**: `Off` | `1-9` (Emergency Alert Tone)
- **AlertVolume**: `Auto` | `1-15`
- **StatusBit**: `Yes` | `Ignore`
- **NAC**: `Srch` | `0-FFF` (hexadecimal, see [P25 NAC reference](../reference_tables/frequency_options_p25.md))
- **QuickKey**: `Off` | `0-99`
- **NumberTag**: `Off` | `0-999`
- **SiteHoldTime**: `0-255` (seconds)
- **AnalogAGC**: `Off` | `On`
- **DigitalAGC**: `Off` | `On`
- **EndCode**: `Analog` | `Analog+Digital` | `Ignore`
- **PriorityIDScan**: `Off` | `On`
- **AlertColor**: Alert Light Color (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **AlertPattern**: Alert Light Pattern (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **TGIDFormat**: `NEXEDGE` | `IDAS`

---

### AreaState

State of System

**Format**: `AreaState\tMyId\tStateId`

**Parameters**:
- **MyId**: `CountyId=xx` | `AgencyId=xx` | `TrunkId=xx`
- **StateId**: `StateId=xx`

**Note**: Favorites List doesn't need AreaState sentence.

---

### AreaCounty

County of System

**Format**: `AreaCounty\tMyId\tCountyId`

**Parameters**:
- **MyId**: `CountyId=xx` | `AgencyId=xx` | `TrunkId=xx`
- **CountyId**: `CountyId=xx`

**Note**: Favorites List doesn't need AreaCounty sentence.

---

### FleetMap

Motorola Type I Fleet Map configuration

**Format**: `FleetMap\tMyId\tB0\tB1\tB2\tB3\tB4\tB5\tB6\tB7`

**Parameters**:
- **MyId**: `TrunkId=xx`
- **B0-B7**: Block sizes - `0` | `1-9` | `A` | `B` | `C` | `D` | `E`
  - `0` indicates all blocks are size 0 (Type II)
  - Other values define fleet block sizes for Type I systems

---

### UnitIds

Unit ID configuration

**Format**: `UnitIds\tReserve\tReserve\tNameTag\tUnitId\tAlertTone\tAlertVolume\tAlertColor\tAlertPattern`

**Parameters**:
- **Reserve**: Reserved fields (2 fields, empty)
- **NameTag**: ASCII character string
- **UnitId**: `1-16777215`
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`
- **AlertColor**: Alert Light Color (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **AlertPattern**: Alert Light Pattern (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))

---

### AvoidTgids

Avoided Talk Group IDs for ID Search mode

**Format**: `AvoidTgids\tMyId\tTGID1\tTGID2\t...\tTGID16`

**Parameters**:
- **MyId**: `TrunkId=xx`
- **TGID1-TGID16**: TGID character strings (see [TGID formats](../global_parsing_rules.md#tgid-talkgroup-id-format-specifications))

**Notes**:
- If no TGIDs are avoided on ID Search mode, AvoidTgids sentence is not outputted to `*.hpd` file
- If over 16 TGIDs are avoided, multiple AvoidTgids sentences are outputted

---

### Site

Trunked system site configuration

**Format**: `Site\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\tRange\tModulation\tMotBandType\tEdacsBandType\tLocationType\tAttenuator\tDigitalWaitingTime\tDigitalThresholdMode\tDigitalThresholdLevel\tQuickKey\tNAC\tFilter`

**Parameters**:
- **MyId**: `SiteId=xx`
- **ParentId**: `TrunkId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Latitude**: Degree format, up to 6 decimal places
- **Longitude**: Degree format, up to 6 decimal places
- **Range**: `1=1 mile`, up to 1 decimal point
- **Modulation**: `AUTO` | `NFM` | `FM`
- **MotBandType**: `Standard` | `Sprinter` | `Custom`
  - Set to `Standard` if [Trunk] System Type isn't Motorola
- **EdacsBandType**: `Wide` | `Narrow`
  - Set to `Wide` if [Trunk] System Type isn't Edacs
- **LocationType**: `Circle` | `Rectangles`
- **Attenuator**: `On` | `Off`
- **DigitalWaitingTime**: `0-1000` (milliseconds, 1 = 1ms)
- **DigitalThresholdMode**: `Auto` | `Manual` | `Default`
- **DigitalThresholdLevel**: `5-13`
- **QuickKey**: `Off` | `0-99`
- **NAC**: `Srch` | `0-FFF` (hexadecimal, see [P25 NAC reference](../reference_tables/frequency_options_p25.md))
- **Filter**: `Global` | `Normal` | `Invert` | `Auto`

---

### Rectangle

Additional geographic information for Department or Site

**Format**: `Rectangle\tMyId\tLatitude1\tLongitude1\tLatitude2\tLongitude2`

**Parameters**:
- **MyId**: `SiteId=xx` | `TGroupId=xx` | `CGroupId=xx`
- **Latitude1**: Degree format, up to 6 decimal places (first corner)
- **Longitude1**: Degree format, up to 6 decimal places (first corner)
- **Latitude2**: Degree format, up to 6 decimal places (opposite corner)
- **Longitude2**: Degree format, up to 6 decimal places (opposite corner)

**Note**: Rectangle sentence is additional information for Department or Site.

---

### BandPlan_Mot

Motorola Custom Band Plan parameter

**Format**: `BandPlan_Mot\tMyId\tLower0\tUpper0\tSpacing0\tOffset0\t...\tLower5\tUpper5\tSpacing5\tOffset5`

**Parameters**:
- **MyId**: `SiteId=xx` (of Site)
- **Lower0-Lower5**: Frequency format (Hz, 1 = 1 Hz)
- **Upper0-Upper5**: Frequency format (Hz, 1 = 1 Hz)
- **Spacing0-Spacing5**: Channel spacing in Hz. Valid values:
  - `5000`, `6250`, `10000`, `12500`, `15000`, `18750`, `20000`, `25000`
  - `30000`, `31250`, `35000`, `37500`, `40000`, `43750`, `45000`, `50000`
  - `55000`, `56250`, `60000`, `62500`, `65000`, `68750`, `70000`, `75000`
  - `80000`, `81250`, `85000`, `87500`, `90000`, `93750`, `95000`, `100000`
  - (5 kHz and 6.25 kHz multiples, up to 100 kHz)
- **Offset0-Offset5**: Offset value from `-1023` to `1023`

**Note**: Valid only when **MotBandType** is `Custom`.

---

### BandPlan_P25

P25 Band Plan configuration

**Format**: `BandPlan_P25\tMyId\tBase0\tSpacing0\tBase1\tSpacing1\t...\tBaseF\tSpacingF`

**Parameters**:
- **MyId**: `SiteId=xx`
- **Base0-BaseF**: Band Plan 0-F Base Frequency (Hz, 1 = 1 Hz)
  - Refer to Band Coverage specification
- **Spacing0-SpacingF**: Band Plan 0-F Spacing Frequency (Hz, 1 = 1 Hz)
  - Range: `125 Hz ≤ Spacing ≤ 128000 Hz`, in 125 Hz increments

**Note**: If Band Plan is undesignated, BandPlan_P25 is omissible (optional).

---

### DQKs_Status

Favorites List Quick Key Status

**Format**: `DQKs_Status\tMyId\tD-Qkey_00\tD-Qkey_01\tD-Qkey_02\t...\tD-Qkey_99`

**Parameters**:
- **MyId**: Parent context identifier
- **D-Qkey_00 through D-Qkey_99**: `Off` | `On` (100 quick key status flags)

---

### C-Group

Conventional Department/Group configuration

**Format**: `C-Group\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\tRange\tLocationType\tQuickKey\tFilter`

**Parameters**:
- **MyId**: `CGroupId=xx`
- **ParentId**: `AgencyId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Latitude**: Degree format, up to 6 decimal places
- **Longitude**: Degree format, up to 6 decimal places
- **Range**: `1=1 mile`, up to 1 decimal point
- **LocationType**: `Circle` | `Rectangles`
- **QuickKey**: `Off` | `0-99`
- **Filter**: `Global` | `Normal` | `Invert` | `Auto`

---

### T-Group

Trunked Talk Group configuration

**Format**: `T-Group\tMyId\tParentId\tNameTag\tAvoid\tLatitude\tLongitude\tRange\tLocationType\tQuickKey`

**Parameters**:
- **MyId**: `TGroupId=xx`
- **ParentId**: `TrunkId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Latitude**: Degree format, up to 6 decimal places
- **Longitude**: Degree format, up to 6 decimal places
- **Range**: `1=1 mile`, up to 1 decimal point
- **LocationType**: `Circle` | `Rectangles`
- **QuickKey**: `Off` | `0-99`

---

### C-Freq

Conventional Frequency/Channel configuration

**Format**: `C-Freq\tMyId\tParentId\tNameTag\tAvoid\tFrequency\tModulation\tAudioOption\tFuncTagId\tAttenuator\tDelay\tVolumeOffset\tAlertTone\tAlertVolume\tAlertColor\tAlertPattern\tNumberTag\tPriorityChannel`

**Parameters**:
- **MyId**: `CFreqId=xx`
- **ParentId**: `CGroupId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **Frequency**: Hz integer (1 = 1 Hz)
- **Modulation**: `AUTO` | `AM` | `NFM` | `FM`
- **AudioOption**: Sub-audio squelch options
  - `null` (All/none)
  - `TONE=xxxx` (CTCSS tone, see [CTCSS/DCS](../reference_tables/frequency_options_ctcss_dcs.md))
  - `NAC=xxx` (P25 NAC, see [P25 NAC](../reference_tables/frequency_options_p25.md))
  - `ColorCode=xx` (DMR color code, see [DMR Color Code](../reference_tables/frequency_options_dmr.md))
  - `RAN=xx` (NXDN RAN, see [NXDN RAN/Area](../reference_tables/frequency_options_nxdn.md))
  - `Area=x` (NXDN Area, see [NXDN RAN/Area](../reference_tables/frequency_options_nxdn.md))
- **FuncTagId**: `1-37` | `208-218` (see [Service Types](../reference_tables/service_types.md))
- **Attenuator**: `On` | `Off`
- **Delay**: `30` | `10` | `5` | `4` | `3` | `2` | `1` | `0` | `-5` | `-10` (seconds)
- **VolumeOffset**: `-3` | `-2` | `-1` | `0` | `1` | `2` | `3` (dB)
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`
- **AlertColor**: Alert Light Color (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **AlertPattern**: Alert Light Pattern (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **NumberTag**: `Off` | `0-999`
- **PriorityChannel**: `Off` | `On`

---

### TGID

Trunked Talk Group ID/Channel configuration

**Format**: `TGID\tMyId\tParentId\tNameTag\tAvoid\tTGID\tAudioType\tFuncTagId\tDelay\tVolumeOffset\tAlertTone\tAlertVolume\tAlertColor\tAlertPattern\tNumberTag\tPriorityChannel\tTDMASlot`

**Parameters**:
- **MyId**: `Tid=xx`
- **ParentId**: `TGroupId=xx`
- **NameTag**: ASCII character string, max 64 characters
- **Avoid**: `On` | `Off` (always `Off` in HPDB, managed by `*.avoid` file)
- **TGID**: TGID character string (see [TGID formats](../global_parsing_rules.md#tgid-talkgroup-id-format-specifications))
- **AudioType**: `ALL` | `ANALOG` | `DIGITAL`
- **FuncTagId**: `1-37` | `208-218` (see [Service Types](../reference_tables/service_types.md))
- **Delay**: `30` | `10` | `5` | `4` | `3` | `2` | `1` | `0` | `-5` | `-10` (seconds)
- **VolumeOffset**: `-3` | `-2` | `-1` | `0` | `1` | `2` | `3` (dB)
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`
- **AlertColor**: Alert Light Color (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **AlertPattern**: Alert Light Pattern (see [Global Parsing Rules](../global_parsing_rules.md#common-parameter-types))
- **NumberTag**: `Off` | `0-999`
- **PriorityChannel**: `Off` | `On`
- **TDMASlot**: `1` | `2` | `Any` (TDMA time slot selection)

---

### T-Freq

Trunked System Frequency configuration

**Format**: `T-Freq\tReserve(MyId)\tParentId\tReserve\tReserve(Avoid)\tFrequency\tLCN\tColorCode/RAN/Area`

**Parameters**:
- **Reserve(MyId)**: Always `TFreqId=0`
- **ParentId**: `SiteId=xx`
- **Reserve**: Reserved field (empty)
- **Reserve(Avoid)**: Always `Off`
- **Frequency**: Hz integer (1 = 1 Hz)
- **LCN**: Logical Channel Number
  - `0` (unassigned)
  - `1-30` (Motorola/LTR)
  - `1-20` (EDACS)
  - `1-4094` (P25)
  - `1-1023` (NXDN)
- **ColorCode/RAN/Area**: Depends on system type
  - `0-15` (DMR Color Code)
  - `RAN=0-63` (NXDN RAN)
  - `Area=0-1` (NXDN Area)
  - `Srch` (Search mode)

---

## Related References

- [Favorites Records](favorites_records.md)
- [Global Parsing Rules](../global_parsing_rules.md)

---

[← Back to Main Index](../README.md)
