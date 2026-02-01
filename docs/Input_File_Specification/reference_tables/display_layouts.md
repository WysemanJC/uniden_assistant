# Display Layout Modes (DispLayoutId & ColorLayoutId)

Reference table for layout modes used by the scanner UI.

[← Back to Main Index](../README.md)

---

## Used By

- [DisplayOption](../record_types/scanner_profile_records.md#displayoption) — Layout mode selection
- [DispColors](../record_types/scanner_profile_records.md#dispcolors) — Color layout selection

---

## Layout Mode Mapping

| DispLayoutId | ColorLayoutId | Mode | Available DispOptId | Available DispColorId | Description |
|---|---|---|---|---|---|
| **1** | **1** | Simple Conventional | 1, 2, 3, 4 | 1–7 | Simplified conventional channel display |
| **2** | **6** | Simple Trunk | 1, 2, 3, 4 | 1–7 | Simplified trunked system display |
| **3** | **2** | Detail Conventional | 1, 2, 3, 4 | 1–7 | Detailed conventional channel display |
| **4** | **7** | Detail Trunk | 1, 2, 3, 4 | 1–7 | Detailed trunked system display |
| **5** | **3** | Search/CC | 2, 3, 4 | 1–7 | Search and Close Call mode |
| **6** | **4** | Weather | 2, 3, 4 | 1–7 | Weather channel display |
| **7** | **5** | Tone Out | 2, 3, 4 | 1–7 | Tone-out alert display |

---

## Related References

- [Display Options](display_options.md)
- [Display Colors](display_colors.md)

---

[← Back to Main Index](../README.md)
