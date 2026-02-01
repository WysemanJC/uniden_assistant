# Discovery Records

Discovery record types (ConvDiscovery, TrunkDiscovery).

[← Back to Main Index](../README.md)

---

## Records in discovery.cfg

**Observed in sample data**: The file is named `discvery.cfg` (missing "o") and contains only `TargetModel` and `FormatVersion` records.

### TargetModel

**Format**: `TargetModel\tModelName`

---

### FormatVersion

**Format**: `FormatVersion\tVersion`

---

### ConvDiscovery

- **Reserve**: (reserved field)
- **Name**: discovery session name (ASCII string, max 32 chars)
- **Lower**: frequency lower bound (Hz integer)
- **Upper**: frequency upper bound (Hz integer)
- **Modulation**: `AUTO` | `AM` | `NFM` | `FM` | `WFM` | `FMB`
- **Step**: `Auto` | `5000|6250|7500|8333|10000|12500|15000|20000|25000|50000|100000` (Hz)
- **Delay**: `5|4|3|2|1|0` (ms; no negative values)
- **Logging**: `All` | `New`
- **CompareDB**: `On` | `Off`
- **Duration**: `0|30|60|90|120|150|180|300|600` (seconds; 0 = OFF)
- **TimeOut**: `0|10|30|60` (seconds; 0 = OFF)
- **AutoStore**: `Off` | `On`

---

### TrunkDiscovery

- **Reserve**: (reserved field)
- **Name**: discovery session name (ASCII string, max 32 chars)
- **Delay**: `5|4|3|2|1|0` (ms)
- **Logging**: `All` | `New`
- **CompareDB**: `On` | `Off`
- **Duration**: `0|30|60|90|120|150|180|300|600` (seconds)
- **FavName**: Favorites List name string (null if using Full Database)
- **SystemName**: system name tag (ASCII string)
- **TrunkId**: `TrunkId=xx` (integer; null if using Favorites List)
- **SystemType**: `Motorola` | `Edacs` | `Scat` | `Ltr` | `P25Standard` | `P25OneFrequency` | `P25X2_TDMA` | `MotoTrbo` | `DmrOneFrequency` | `Nxdn` | `NxdnOneFrequency`
- **SiteId**: `SiteId=xx` (integer; null if using Favorites List)
- **SiteName**: site name tag (ASCII string)
- **TimeOut**: `0|10|30|60` (seconds; 0 = OFF)
- **AutoStore**: `Off` | `On`
- **Note**: FavName, SystemName, TrunkId, SystemType, SiteId, SiteName are set by device only; PC app reads/writes same values

---

## Related References

- [System Records](system_records.md)
- [Favorites Records](favorites_records.md)

---

[← Back to Main Index](../README.md)
