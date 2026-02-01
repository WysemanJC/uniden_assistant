# Scan Configuration Records

Scan lists and scan configuration record types (ScanListType, Scan*, etc.).

[← Back to Main Index](../README.md)

---

## Records in app_data.cfg

### TargetModel

**Format**: `TargetModel\tModelName`

---

### FormatVersion

**Format**: `FormatVersion\tVersion`

---

**Observed in sample data**: `app_data.cfg` contains only `TargetModel`, `FormatVersion`, and `ModeInfo` records.

### ScanListType

- **Type**: `FullDatabase` | `FavoritesList` | `SearchWithScan`
- **Name**: Favorites List Name (string, required only for FavoritesList type)

---

### ScanConvSystem

- **SystemHold**: `On` | `Off`
- **MyId**: `CountyId=xx` | `AgencyId=xx`
- **ParentId**: `StateId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Reserve**: (reserved field)
- **SystemType**: `Conventional`
- **QuickKey**: `Off` | `0-99`
- **NumberTag**: `Off` | `0-99`
- **SystemHoldTime**: `0-255` (ms)
- **AnalogAGC**: `Off` | `On`
- **DigitalAGC**: `Off` | `On`
- **DigitalWaitingTime**: `0-1000` (ms)
- **DigitalThresholdMode**: `Auto` | `Manual` | `Default`
- **DigitalThresholdLevel**: `5-13`

---

### ScanTrunkSystem

- **SystemHold**: `On` | `Off`
- **MyId**: `TrunkId=xx`
- **ParentId**: `StateId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Reserve**: (reserved field)
- **SystemType**: `Motorola` | `Edacs` | `Scat` | `Ltr` | `P25Standard` | `P25OneFrequency` | `P25X2_TDMA` | `MotoTrbo` | `DmrOneFrequency` | `Nxdn` | `NxdnOneFrequency`
- **IDSearch**: `Off` | `On`
- **AlertTone**: `Off` | `0-9`
- **AlertVolume**: `Auto` | `1-15`
- **StatusBit**: `Yes` | `Ignore`
- **NAC**: `Srch` | `0-FFF`
- **QuickKey**: `Off` | `0-99`
- **NumberTag**: `Off` | `0-99`
- **SiteHoldTime**: `0-255` (ms)
- **AnalogAGC**: `Off` | `On`
- **DigitalAGC**: `Off` | `On`
- **EndCode**: `Analog` | `Analog+Digital` | `Ignore`
- **PriorityIDScan**: `Off` | `On`
- **AlertColor**: Alert Light Color format
- **AlertPattern**: Alert Light Pattern format
- **TGIDFormat**: `NEXEDGE` | `IDAS`

---

### ScanC-Group

- **GroupHold**: `On` | `Off`
- **MyId**: `CGroupId=xx`
- **ParentId**: `AgencyId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Latitude/Longitude**: degree format, up to 6 decimals
- **Range**: `1=1mile`, up to 1 decimal point
- **LocationType**: `Circle` | `Rectangles`
- **Filter**: `Global` | `Normal` | `Invert` | `Auto`

---

### ScanT-Group

- **GroupHold**: `On` | `Off`
- **MyId**: `TGroupId=xx`
- **ParentId**: `TrunkId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Latitude/Longitude**: degree format, up to 6 decimals
- **Range**: `1=1mile`, up to 1 decimal point
- **LocationType**: `Circle` | `Rectangles`

---

### ScanC-Freq

- **MyId**: `CFreqId=xx`
- **ParentId**: `CGroupId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Frequency**: Hz integer (1 = 1 Hz)
- **Modulation**: `AUTO` | `AM` | `NFM` | `FM`
- **AudioOption**: `null` | `Tone=xxxx` | `NAC=xxx` | `ColorCode=xx` | `RAN=xx` | `Area=x`
- **FuncTagId**: `1-37` | `208-218`
- **Attenuator**: `On` | `Off`
- **Delay**: `30|10|5|4|3|2|1|0|-5|-10` (ms)
- **VolumeOffset**: `-3|-2|-1|0|1|2|3` (dB)
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`
- **AlertColor**: Alert Light Color format
- **AlertPattern**: Alert Light Pattern format
- **NumberTag**: `Off` | `0-999`
- **PriorityChannel**: `Off` | `On`

---

### ScanTGID

- **MyId**: `Tid=xx`
- **ParentId**: `TGroupId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **TGID**: TGID character string (see [TGID formats](../global_parsing_rules.md#tgid-talkgroup-id-format-specifications))
- **AudioType**: `ALL` | `ANALOG` | `DIGITAL`
- **FuncTagId**: `1-37` | `208-218`
- **Delay**: `30|10|5|4|3|2|1|0|-5|-10` (ms)
- **VolumeOffset**: `-3|-2|-1|0|1|2|3` (dB)
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`
- **AlertColor**: Alert Light Color format
- **AlertPattern**: Alert Light Pattern format
- **NumberTag**: `Off` | `0-999`
- **PriorityChannel**: `Off` | `On`
- **TDMASlot**: `1` | `2` | `Any`

---

### ScanSite

- **SiteHold**: `On` | `Off`
- **MyId**: `SiteId=xx`
- **ParentId**: `TrunkId=xx`
- **NameTag**: ASCII string, max 64 chars
- **Avoid**: `On` | `Off`
- **Latitude/Longitude**: degree format, up to 6 decimals
- **Range**: `1=1mile`, up to 1 decimal point
- **Modulation**: `AUTO` | `NFM` | `FM`
- **MotBandType**: `Standard` | `Sprinter` | `Custom`
- **EdacsBandType**: `Wide` | `Narrow`
- **LocationType**: `Circle` | `Rectangles`
- **Attenuator**: `On` | `Off`
- **DigitalWaitingTime**: `0-1000` (ms)
- **DigitalThresholdMode**: `Auto` | `Manual` | `Default`
- **DigitalThresholdLevel**: `5-13`
- **QuickKey**: `Off` | `0-99`
- **NAC**: `Srch` | `0-FFF`
- **Filter**: `Global` | `Normal` | `Invert` | `Auto`

---

### ScanT-Freq

- **Reserve(MyId)**: `TFreqId=xx`
- **ParentId**: `TFreqId=xx`
- **Reserve**: (reserved field)
- **Reserve(Avoid)**: `Off` (always Off)
- **Frequency**: Hz integer (1 = 1 Hz)
- **LCN**: `0` | `1-30` | `1-20` | `1-4094` | `1-1023`
- **ColorCode/RAN/Area**: `0-15` | `RAN=0-63` | `Area=0-1` | `Srch`

---

### ModeInfo

- **Mode**: `Scan` | `ScanHold` | `ToneOut` | `ToneOutHold` | `CustomSearch` | `CustomSearchHold` | `QuickSearch` | `QuickSearchHold` | `IDsearch` | `IDsearchhold` | `IDscan` | `IDmanual` | `EdacsIDSearch` | `EdacsIDSearchHold` | `EdacsIDScan` | `EdacsIDManual` | `LTRIDSearch` | `LTRIDSearchHold` | `LTRIDScan` | `LTRIDManual` | `CloseCallOnly` | `WeatherScan` | `WeatherHold`
- **SystemHold**: `On` | `Off`
- **DeptHold**: `On` | `Off`

---

### SearchWithScan

- **SystemIndex**: (integer, index reference to scan system)

---

### CustomSearch

- **Bank**: `0-9` (custom search bank)
- **Frequency**: `0x00250000 - 0x13000000` (hex range)

---

### QuickSearch

- **Frequency**: `0x00250000 - 0x13000000` (hex frequency)

---

### ToneOut

- **Channel**: `1-32` (tone out channel number)

---

### CloseCall

- (No parameters; presence indicates Close Call mode enabled)

---

## Related References

- [Global Parsing Rules](../global_parsing_rules.md)
- [Service Types](../reference_tables/service_types.md)
- [Frequency Options](../reference_tables/frequency_options_ctcss_dcs.md)

---

[← Back to Main Index](../README.md)
