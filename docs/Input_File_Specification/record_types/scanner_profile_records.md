# Scanner/Profile Records

Scanner, ProductName, GlobalSetting, DisplayOption, DispColors, and related profile records.

[← Back to Main Index](../README.md)

---

## Profile Configuration (profile.cfg)

### TargetModel

**Format**: `TargetModel\tModelName`

---

### FormatVersion

**Format**: `FormatVersion\tVersion`

---

### ProductName

- **Model**: model name string (e.g., `SDS100`)

---

### GlobalSetting

- **ScanHpdb**: `Off` | `On`
- **G-Attenuator**: `On` | `Off`
- **Reserve**: (reserved field)
- **PriorityScanMode**: `Off` | `DND` | `Priority`
- **CloseCallMode**: `Off` | `DND` | `Priority`
- **WXPriorityMode**: `Off` | `Priority`
- **PriorityInterval**: `1-10` (seconds)
- **PriorityMaxChannels**: `1-100`
- **SrchKey1/2/3**: `Off` | `Custom0-Custom9` | `ToneOut` | `CloseCall`
- **KeyLock**: `Off` | `On`
- **KeyBeep**: `Off` | `1-15` | `Auto`
- **Volume**: `0-29` (Mobile) | `0-15` (Handy)
- **Squelch**: `0-19` (Mobile) | `0-15` (Handy)
- **SearchWithScanList**: `Off` | `On`
- **SearchWithScanSystemAvoid**: `Off` | `On`
- **SiteNACOperation**: `Ignore` | `Compare`
- **GlobalAutoFilter**: `Normal` | `Invert` | `Auto`

---

### SearchCommon

- **Reserve**: (reserved field)
- **RepeaterFind**: `Off` | `On`
- **Attenuator**: `Off` | `On`
- **Delay**: `30|10|5|4|3|2|1|0|-5|-10` (ms)
- **Modulation**: `Auto` | `AM` | `NFM` | `FM` | `WFM` | `FMB`
- **agc_analog**: `Off` | `On`
- **agc_digital**: `Off` | `On`
- **Digital_waiting_time**: `0-1000` (ms)
- **Digital_threshold_Mode**: `Auto` | `Manual` | `Default`
- **Digital_threshold_Level**: `5-13`
- **Filter**: `Global` | `Normal` | `Invert` | `Auto`

---

### PresetBroadcastScreen

- **Pager**: `Off` | `On`
- **FM**: `Off` | `On`
- **UHF_TV**: `Off` | `On`
- **VHF_TV**: `Off` | `On`
- **NOAA_WX**: `Off` | `On`

---

### CustomBroadcastScreen

- **Band0Enable–Band9Enable**: `Off` | `On`
- **Band0Lower–Band9Lower**: `0-1300MHz` (Hz)
- **Band0Upper–Band9Upper**: `0-1300MHz` (Hz)

---

### CurrentLocation

- **Latitude**: degree format, up to 6 decimals
- **Longitude**: degree format, up to 6 decimals
- **Range**: `0.0-50.0` (0.5-mile steps)

---

### GpsOption

- **GpsFormat**: `DMS` | `Decimal`
- **BaudRate**: `Off` | `4800` | `9600` | `19200` | `38400` | `57600` | `115200`

---

### InterestingLocation

- **Name**: ASCII string (location name/tag)
- **Latitude**: degree format, up to 6 decimals
- **Longitude**: degree format, up to 6 decimals
- **Range**: `0-50` (integer, 0.5-mile steps)

---

### ServiceType

- **Id01_state–Id37_state**: `Off` | `On` (service type IDs 1–37)

---

### CustomServiceType

- **Id01_state–Id10_state**: `Off` | `On`
	- Id01_state–Id08_state: Custom 1–8
	- Id09_state: Racing Officials
	- Id10_state: Racing Teams

---

### Weather

- **Reserve**: (reserved field)
- **Delay**: `30|10|5|4|3|2|1|0|-5|-10` (ms)
- **Attenuator**: `Off` | `On`
- **agc_analog**: `Off` | `On`

---

### WxSameList

- **SameId**: `SameId=x` where `x = 1-5`
- **Name**: same group name (ASCII string)
- **FIPS0–FIPS7**: `000000-999999` or `------` (string × 8)

---

### DisplayOption

- **Reserve**: (multiple reserved fields)
- **MotTgidFormat**: `DEC` | `HEX`
- **ScnDispMode**: `Mode 1` | `Mode 2`
- **SimpleMode**: `Off` | `On` (SDS100 only)
- **EdacTgidFormat**: `AFS` | `DEC`
- **ColorMode**: `COLOR` | `BLACK` | `WHITE`

---

### Backlight

- **Reserve**: (multiple reserved fields)
- **Brightness**: `10|20|30|...|100` (SDS100 only)
- **Key_Backlight**: `Off` | `On` (SDS100 only)
- **FlashLed**: `Off` | `On`
- **Ext_PWR_Light**: `Off` | `On` (SDS100 only)
- **SQ_Light**: `Off` | `5` | `10` | `15` | `OpenSquelch`
- **KeyLight**: `15|30|60|120|Infinite`
- **Dimmer_mode**: `Auto` | `Manual` (SDS200 only)
- **Auto_Polarity**: `Auto+` | `Auto-` (SDS200 only)
- **Manual_Level**: `Low` | `Middle` | `High` (SDS200 only)
- **Dimmer_L–Dimmer_H**: `10|20|30|...|100` (SDS200 only)
- **Key_Backlight2**: `Off` | `On` (SDS200 only)

---

### QuickKeys

- **F-Qkey_00–F-Qkey_99**: `Off` | `On` (boolean × 100)

---

### Battery

- **BatterySave**: `Off` | `On`
- **Reserve**: (reserved fields × 2)
- **AlertInterval**: `1-60` (seconds)
- **AlertTone**: `Off` | `1-9`
- **AlertVolume**: `Auto` | `1-15`

---

### DispOptItems

- **DispOptId**: `1` | `2` | `3` | `4`
- **DispLayoutId**: `1-7`
- **OptItem1–OptItemN**: optional item codes (see Color/Item code sheet)

---

### DispColors

- **DispColorId**: `1-5`
- **ColorLayoutId**: `1-7`
- **TextColor1–TextColorN**: hex color codes (text colors)
- **BackColor1–BackColorN**: hex color codes (background colors)

---

## Additional Records Observed in Sample Data

The following records appear in `profile.cfg` in the sample card image but are not explicitly defined in the spec text. Field meanings are inferred from observed values.

### OwnerInfo

**Observed format**: `OwnerInfo\tOwnerName\tProductName\tLine1\tLine2`

Example (sample data):

`OwnerInfo	Uniden Bearcat	UBCD436-PT CFA_2020A	Digital Trunking	Dynamic Scanning`

---

### ClockOption

**Observed format**: `ClockOption\tTimeFormat\tTimeZone\tDST`

Example (sample data):

`ClockOption	24H	10.0	Off`

---

### RecordingOption

**Observed format**: `RecordingOption\tDuration`

Example (sample data):

`RecordingOption	30`

---

### StandbyOption

**Observed format**: `StandbyOption\tStandbyMode\tKeyBehavior`

Example (sample data):

`StandbyOption	Clock Standby	All Off`

---

### LimitSearch

**Observed format**: `LimitSearch\tSrchId=xx\tName\tLower\tUpper\tModulation\tStep\t...`

Example (sample data):

`LimitSearch	SrchId=01	Custom 0	25000000	27999900	AUTO	Auto	2	Off	On	Off					2	Off	Off	400	Auto	8`

---

### BandDefault

**Observed format**: `BandDefault\tBandId=xx\tModulation\tStep`

Example (sample data):

`BandDefault	BandId=01	AM	5000`

---

### IfxFreqs

**Observed format**: `IfxFreqs` (no parameters in sample data)

---

### ToneOut

**Observed format**: `ToneOut\tToneOutId=xx\tName\tToneA\tFrequency\tModulation\t...`

Example (sample data):

`ToneOut	ToneOutId=01	Tone-Out 0		137000000	FM	0	0	Off	2	Off	Off	Auto	Off	On`

---

### CloseCall

**Observed format**: `CloseCall\t...` (multiple fields; not specified in spec)

Example (sample data):

`CloseCall			Off	3	1	Auto	Yellow	Slow Blink	On	On	On	On	On	On	On			2`

---

## Scanner Information (scanner.inf)

### Scanner

- **Model**: model name string (e.g., `BCD536HP`)
- **ESN**: Electronic Serial Number (string)
- **F_Ver**: firmware version string (e.g., `1.05`)
- **R_Ver**: registry version string
- **Reserve**: (reserved field)
- **Zip_Ver**: zip table version string
- **City_Ver**: city table version string
- **WiFi_Ver**: WiFi module version string (SDS100 only)
- **SCPU_Ver**: sub-CPU version string

---

## Related References

- [Display Options](../reference_tables/display_options.md)
- [Display Colors](../reference_tables/display_colors.md)
- [Display Layout Modes](../reference_tables/display_layouts.md)

---

[← Back to Main Index](../README.md)
