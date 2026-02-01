# Display Options & Area Sizing

Display area options define how UI information is rendered on the scanner device. Options are organized into 4 display area size categories (**DispOptId**), each supporting different display layouts and modes.

[← Back to Main Index](../README.md)

---

## Used By

This reference is used by the following record types:
- [DisplayOption](../record_types/scanner_profile_records.md#displayoption) — Defines display area configurations
- [DispColors](../record_types/scanner_profile_records.md#dispcolors) — References DispColorId for color mapping

---

## Display Area Size Options (DispOptId)

Each **DispOptId** maps to a display area size category that determines screen real estate allocation:

| DispOptId | Area Size | Description | Screen Space |
|---|---|---|---|
| **1** | Huge area option | Full-screen, maximum visibility | ~100% |
| **2** | Large area option | Prominent display region | 50–75% |
| **3** | Small area option | Compact information area | 25–50% |
| **4** | Icon area option | Icon-only display | ≤25% (10 icon positions) |

---

## Display Layout Modes (DispLayoutId & ColorLayoutId)

Display modes determine which **DispOptItems** (display elements) and **DispColors** (color schemes) are active for different radio modes.

| DispLayoutId | ColorLayoutId | Mode | Available DispOptId | Available DispColorId | Description |
|---|---|---|---|---|---|
| **1** | **1** | Simple Conventional | 1, 2, 3, 4 | 1–7 | Simplified conventional channel display |
| **2** | **6** | Simple Trunk | 1, 2, 3, 4 | 1–7 | Simplified trunked system display |
| **3** | **2** | Detail Conventional | 1, 2, 3, 4 | 1–7 | Detailed conventional channel display |
| **4** | **7** | Detail Trunk | 1, 2, 3, 4 | 1–7 | Detailed trunked system display |
| **5** | **3** | Search/CC | 2, 3, 4 | 1–7 | Search and Close Call mode |
| **6** | **4** | Weather | 2, 3, 4 | 1–7 | Weather channel display |
| **7** | **5** | Tone Out | 2, 3, 4 | 1–7 | Tone-out alert display |

**Notes:**
- **Simple modes** (1, 2): Minimize displayed information, focus on essentials
- **Detail modes** (3, 4): Show comprehensive system/channel metadata
- **Special modes** (5, 6, 7): Specialized displays for search, weather, and alerts
- Search/CC, Weather, and Tone Out modes do not support Huge (DispOptId=1) display areas

---

## Display Color Codes (DispColorId)

Each **DispColorId** maps to specific UI elements or layout components. Colors are stored as hex RGB triplets in TextColor/BackColor pairs.

| DispColorId | Display Elements | Usage |
|---|---|---|
| **1** | System/Header Information | System Name, Department Name, Channel Name, Info areas, Avoid indicators |
| **2** | Primary Options | System Option, Dept Option, Channel Option |
| **3** | Secondary Options | Option_1 through Option_8 |
| **4** | Extended Options | Option A/B sets (A_1–A_5, B_1–B_5, C_1–C_2) |
| **5** | Icon Display Colors | ICON1 through ICON10 |
| **6** | Status Bar | F, SIG, BAT, KEY, DIR buttons/indicators |
| **7** | Soft Keys | Soft Key 1–3, SP0–SP2 |

**Color Reversal Note**: **F**, **Soft Key 1**, **Soft Key 2**, and **Soft Key 3** use **reversed text/back colors** (text color becomes background, background becomes text) for UI emphasis.

---

## Standard Color Palette

Default colors used across layout modes (for complete palette, see [Display Colors Reference](display_colors.md)):

| Color Name | Hex Code | Primary Usage |
|---|---|---|
| **Orange** | `ff4600` | System Name, main highlights |
| **Orange-Red** | `ff8800` | Department, secondary highlights |
| **Yellow** | `ffd600` | Channel, accent elements |
| **White** | `ffffff` | Standard text/options |
| **Tan** | `e79473` | Extended options (Option A/B) |
| **Black** | `000000` | Default background |

---

## Color Specification Principles

Key color assignment principles across all display modes:

- **System-level**: Orange (`ff4600`) for maximum visibility
- **Department-level**: Orange-Red (`ff8800`) for secondary importance  
- **Channel-level**: Yellow (`ffd600`) for tertiary information
- **Options/Details**: White (`ffffff`) for standard content
- **Extended options**: Tan (`e79473`) for Option A/B variants
- **Status elements**: White (`ffffff`) for status indicators
- **All backgrounds**: Black (`000000`) unless specified
- **Text reversal**: F and Soft Key elements swap text/back colors for UI emphasis

---

## Display Mode Examples

### Simple Conventional Mode (ColorLayoutId=1)

**DispColorId=1** (System/Header Information):
- System Name: `TextColor=ff4600, BackColor=000000`
- Dept Name: `TextColor=ff8800, BackColor=000000`
- Channel Name: `TextColor=ffd600, BackColor=000000`

**DispColorId=2** (Primary Options):
- System Option: `TextColor=ff4600, BackColor=000000`
- Dept Option: `TextColor=ff8800, BackColor=000000`
- Channel Option: `TextColor=ffd600, BackColor=000000`

**DispColorId=3** (Secondary Options 1–8):
- All Option_1 through Option_8: `TextColor=ffffff, BackColor=000000`

### Detail Conventional Mode (ColorLayoutId=2)

**DispColorId=1** (System/Header + Info Areas):
- System Name: `TextColor=ff4600, BackColor=000000`
- Dept Name: `TextColor=ff8800, BackColor=000000`
- Channel Name: `TextColor=ffd600, BackColor=000000`
- Info area 1, 2, 3: `TextColor=ffffff, BackColor=000000`

**DispColorId=4** (Extended Options A/B):
- Option A_1 through Option_B_5, Option C_1, Option C_2: `TextColor=e79473, BackColor=000000`

---

## Related References

- [Display Colors Reference](display_colors.md) — Complete 164-color palette with display area mappings
- [Display Layouts](display_layouts.md) — Detailed layout configuration for each mode
- [DisplayOption Record](../record_types/scanner_profile_records.md#displayoption) — Record format for display configurations

---

[← Back to Main Index](../README.md)
