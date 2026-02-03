"""Spec-aligned field name maps for SDSx00 input files.

Field names are taken directly from docs/Input_File_Specification/*.md.
When a record contains reserved fields, names are assigned as Reserve, Reserve1..N.
"""
from typing import Dict, List, Tuple


def _seq(prefix: str, start: int, end: int, width: int = 2) -> List[str]:
    if end < start:
        return []
    return [f"{prefix}{str(i).zfill(width)}" for i in range(start, end + 1)]


def _reserve(count: int, start: int = 1) -> List[str]:
    if count <= 0:
        return []
    if count == 1:
        return ["Reserve"]
    return [f"Reserve{idx}" for idx in range(start, start + count)]


FIXED_FIELD_MAPS: Dict[str, List[str]] = {
    # File metadata
    "TargetModel": ["ModelName"],
    "FormatVersion": ["Version"],
    "DateModified": ["TimeStamp"],

    # hpdb.cfg
    "StateInfo": ["StateId", "CountryId", "NameTag", "ShortName"],
    "CountyInfo": ["CountyId", "StateId", "NameTag"],
    "LM": ["StateId", "CountyId", "TrunkId", "SiteId", "LM_SystemID", "LM_SiteID", "Latitude", "Longitude"],
    "LM_Frequency": ["Frequency", "Reserve", "LmTypeArray"],

    # System records (HPDB + Favorites)
    "Conventional": [
        "MyId", "ParentId", "NameTag", "Avoid", "Reserve", "SystemType", "QuickKey", "NumberTag",
        "SystemHoldTime", "AnalogAGC", "DigitalAGC", "DigitalWaitingTime", "DigitalThresholdMode",
        "DigitalThresholdLevel",
    ],
    "Trunk": [
        "MyId", "ParentId", "NameTag", "Avoid", "Reserve", "SystemType", "IDSearch", "AlertTone",
        "AlertVolume", "StatusBit", "NAC", "QuickKey", "NumberTag", "SiteHoldTime", "AnalogAGC",
        "DigitalAGC", "EndCode", "PriorityIDScan", "AlertColor", "AlertPattern", "TGIDFormat",
    ],
    "AreaState": ["MyId", "StateId"],
    "AreaCounty": ["MyId", "CountyId"],
    "FleetMap": ["MyId", "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
    "UnitIds": ["Reserve1", "Reserve2", "NameTag", "UnitId", "AlertTone", "AlertVolume", "AlertColor", "AlertPattern"],
    "Site": [
        "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range", "Modulation",
        "MotBandType", "EdacsBandType", "LocationType", "Attenuator", "DigitalWaitingTime",
        "DigitalThresholdMode", "DigitalThresholdLevel", "QuickKey", "NAC", "Filter",
    ],
    "Rectangle": ["MyId", "Latitude1", "Longitude1", "Latitude2", "Longitude2"],
    "C-Group": [
        "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range", "LocationType",
        "QuickKey", "Filter",
    ],
    "T-Group": [
        "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range", "LocationType",
        "QuickKey",
    ],
    "C-Freq": [
        "MyId", "ParentId", "NameTag", "Avoid", "Frequency", "Modulation", "AudioOption", "FuncTagId",
        "Attenuator", "Delay", "VolumeOffset", "AlertTone", "AlertVolume", "AlertColor", "AlertPattern",
        "NumberTag", "PriorityChannel",
    ],
    "TGID": [
        "MyId", "ParentId", "NameTag", "Avoid", "TGID", "AudioType", "FuncTagId", "Delay",
        "VolumeOffset", "AlertTone", "AlertVolume", "AlertColor", "AlertPattern", "NumberTag",
        "PriorityChannel", "TDMASlot",
    ],
    "T-Freq": ["Reserve(MyId)", "ParentId", "Reserve", "Reserve(Avoid)", "Frequency", "LCN", "ColorCode/RAN/Area"],

    # Scan configuration (app_data.cfg)
    "ScanListType": ["Type", "Name"],
    "ScanConvSystem": [
        "SystemHold", "MyId", "ParentId", "NameTag", "Avoid", "Reserve", "SystemType", "QuickKey",
        "NumberTag", "SystemHoldTime", "AnalogAGC", "DigitalAGC", "DigitalWaitingTime",
        "DigitalThresholdMode", "DigitalThresholdLevel",
    ],
    "ScanTrunkSystem": [
        "SystemHold", "MyId", "ParentId", "NameTag", "Avoid", "Reserve", "SystemType", "IDSearch",
        "AlertTone", "AlertVolume", "StatusBit", "NAC", "QuickKey", "NumberTag", "SiteHoldTime",
        "AnalogAGC", "DigitalAGC", "EndCode", "PriorityIDScan", "AlertColor", "AlertPattern",
        "TGIDFormat",
    ],
    "ScanC-Group": [
        "GroupHold", "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range",
        "LocationType", "Filter",
    ],
    "ScanT-Group": [
        "GroupHold", "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range",
        "LocationType",
    ],
    "ScanC-Freq": [
        "MyId", "ParentId", "NameTag", "Avoid", "Frequency", "Modulation", "AudioOption", "FuncTagId",
        "Attenuator", "Delay", "VolumeOffset", "AlertTone", "AlertVolume", "AlertColor", "AlertPattern",
        "NumberTag", "PriorityChannel",
    ],
    "ScanTGID": [
        "MyId", "ParentId", "NameTag", "Avoid", "TGID", "AudioType", "FuncTagId", "Delay",
        "VolumeOffset", "AlertTone", "AlertVolume", "AlertColor", "AlertPattern", "NumberTag",
        "PriorityChannel", "TDMASlot",
    ],
    "ScanSite": [
        "SiteHold", "MyId", "ParentId", "NameTag", "Avoid", "Latitude", "Longitude", "Range",
        "Modulation", "MotBandType", "EdacsBandType", "LocationType", "Attenuator",
        "DigitalWaitingTime", "DigitalThresholdMode", "DigitalThresholdLevel", "QuickKey", "NAC", "Filter",
    ],
    "ScanT-Freq": ["Reserve(MyId)", "ParentId", "Reserve", "Reserve(Avoid)", "Frequency", "LCN", "ColorCode/RAN/Area"],
    "ModeInfo": ["Mode", "SystemHold", "DeptHold"],
    "SearchWithScan": ["SystemIndex"],
    "CustomSearch": ["Bank", "Frequency"],
    "QuickSearch": ["Frequency"],
    "ToneOut": ["Channel"],
    "CloseCall": [],

    # Favorites list
    "F-List": [
        "UserName", "Filename", "LocationControl", "Monitor", "QuickKey", "NumberTag",
        *[f"StartupKey{idx}" for idx in range(10)],
        *_seq("S-Qkey_", 0, 99, width=2),
    ],

    # discovery.cfg
    "ConvDiscovery": [
        "Reserve", "Name", "Lower", "Upper", "Modulation", "Step", "Delay", "Logging", "CompareDB",
        "Duration", "TimeOut", "AutoStore",
    ],
    "TrunkDiscovery": [
        "Reserve", "Name", "Delay", "Logging", "CompareDB", "Duration", "FavName", "SystemName",
        "TrunkId", "SystemType", "SiteId", "SiteName", "TimeOut", "AutoStore",
    ],

    # profile.cfg / scanner.inf
    "ProductName": ["Model"],
    "GlobalSetting": [
        "ScanHpdb", "G-Attenuator", "Reserve", "PriorityScanMode", "CloseCallMode", "WXPriorityMode",
        "PriorityInterval", "PriorityMaxChannels", "SrchKey1", "SrchKey2", "SrchKey3", "KeyLock",
        "KeyBeep", "Volume", "Squelch", "SearchWithScanList", "SearchWithScanSystemAvoid",
        "SiteNACOperation", "GlobalAutoFilter",
    ],
    "SearchCommon": [
        "Reserve", "RepeaterFind", "Attenuator", "Delay", "Modulation", "agc_analog", "agc_digital",
        "Digital_waiting_time", "Digital_threshold_Mode", "Digital_threshold_Level", "Filter",
    ],
    "PresetBroadcastScreen": ["Pager", "FM", "UHF_TV", "VHF_TV", "NOAA_WX"],
    "CustomBroadcastScreen": [
        *[f"Band{idx}Enable" for idx in range(10)],
        *[f"Band{idx}Lower" for idx in range(10)],
        *[f"Band{idx}Upper" for idx in range(10)],
    ],
    "CurrentLocation": ["Latitude", "Longitude", "Range"],
    "GpsOption": ["GpsFormat", "BaudRate"],
    "InterestingLocation": ["Name", "Latitude", "Longitude", "Range"],
    "Weather": ["Reserve", "Delay", "Attenuator", "agc_analog"],
    "WxSameList": ["SameId", "Name", *[f"FIPS{idx}" for idx in range(8)]],
    "DisplayOption": [
        "Reserve1", "Reserve2", "Reserve3", "MotTgidFormat", "ScnDispMode", "SimpleMode",
        "EdacTgidFormat", "ColorMode",
    ],
    "Backlight": [
        "Reserve1", "Reserve2", "Reserve3", "Brightness", "Key_Backlight", "FlashLed", "Ext_PWR_Light",
        "SQ_Light", "KeyLight", "Dimmer_mode", "Auto_Polarity", "Manual_Level", "Dimmer_L", "Dimmer_H",
        "Key_Backlight2",
    ],
    "QuickKeys": [*_seq("F-Qkey_", 0, 99, width=2)],
    "Battery": ["BatterySave", "Reserve1", "Reserve2", "AlertInterval", "AlertTone", "AlertVolume"],
    "DispOptItems": ["DispOptId", "DispLayoutId"],
    "DispColors": ["DispColorId", "ColorLayoutId"],
    "OwnerInfo": ["OwnerName", "ProductName", "Line1", "Line2"],
    "ClockOption": ["TimeFormat", "TimeZone", "DST"],
    "RecordingOption": ["Duration"],
    "StandbyOption": ["StandbyMode", "KeyBehavior"],
    "LimitSearch": ["SrchId", "Name", "Lower", "Upper", "Modulation", "Step"],
    "BandDefault": ["BandId", "Modulation", "Step"],
    "IfxFreqs": [],
    "Scanner": ["Model", "ESN", "F_Ver", "R_Ver", "Reserve", "Zip_Ver", "City_Ver", "WiFi_Ver", "SCPU_Ver"],
}


def _service_type_fields() -> List[str]:
    return [f"Id{str(i).zfill(2)}_state" for i in range(1, 38)]


def _custom_service_type_fields() -> List[str]:
    return [f"Id{str(i).zfill(2)}_state" for i in range(1, 11)]


def _dynamic_field_names(record_type: str, field_count: int, fields: List[str]) -> List[str]:
    if record_type == "AvoidTgids":
        return ["MyId", *[f"TGID{idx}" for idx in range(1, field_count)]]

    if record_type == "BandPlan_Mot":
        names = ["MyId"]
        for idx in range(6):
            names.extend([f"Lower{idx}", f"Upper{idx}", f"Spacing{idx}", f"Offset{idx}"])
        return names

    if record_type == "BandPlan_P25":
        names = ["MyId"]
        for idx in range(16):
            hex_idx = f"{idx:X}"
            names.extend([f"Base{hex_idx}", f"Spacing{hex_idx}"])
        return names

    if record_type == "DQKs_Status":
        return ["MyId", *[f"D-Qkey_{str(i).zfill(2)}" for i in range(100)]]

    if record_type == "ServiceType":
        return _service_type_fields()

    if record_type == "CustomServiceType":
        return _custom_service_type_fields()

    if record_type == "DispOptItems":
        extra = max(field_count - 2, 0)
        return ["DispOptId", "DispLayoutId", *[f"OptItem{idx}" for idx in range(1, extra + 1)]]

    if record_type == "DispColors":
        extra = max(field_count - 2, 0)
        text_count = extra // 2
        back_count = extra - text_count
        return [
            "DispColorId", "ColorLayoutId",
            *[f"TextColor{idx}" for idx in range(1, text_count + 1)],
            *[f"BackColor{idx}" for idx in range(1, back_count + 1)],
        ]

    if record_type == "F-List":
        base = [
            "UserName", "Filename", "LocationControl", "Monitor", "QuickKey", "NumberTag",
            *[f"StartupKey{idx}" for idx in range(10)],
        ]
        remaining = max(field_count - len(base), 0)
        return [*base, *_seq("S-Qkey_", 0, remaining - 1, width=2)]

    if record_type == "Avoid":
        if field_count >= 4:
            return ["StateId", "SystemId", "DeptId", "ChannelId"]
        if field_count == 3:
            if fields and fields[2].startswith("SiteId="):
                return ["StateId", "SystemId", "SiteId"]
            return ["StateId", "SystemId", "DeptId"]
        if field_count == 2:
            return ["StateId", "SystemId"]
        return []

    if record_type in {"LimitSearch", "ToneOut", "CloseCall"}:
        # Use known leading fields, then reserved placeholders for remaining
        base = FIXED_FIELD_MAPS.get(record_type, [])
        extra = max(field_count - len(base), 0)
        return [*base, *_reserve(extra)]

    return []


def get_spec_field_names(record_type: str, fields: List[str]) -> List[str]:
    if record_type in {"ServiceType", "CustomServiceType"}:
        return _dynamic_field_names(record_type, len(fields), fields)

    if record_type in FIXED_FIELD_MAPS:
        names = FIXED_FIELD_MAPS[record_type]
        if record_type in {"DispOptItems", "DispColors", "F-List"}:
            return _dynamic_field_names(record_type, len(fields), fields)
        return names

    return _dynamic_field_names(record_type, len(fields), fields)


def build_spec_field_map(record_type: str, fields: List[str]) -> Tuple[List[str], Dict[str, str]]:
    names = get_spec_field_names(record_type, fields)
    field_map = {names[idx]: fields[idx] for idx in range(min(len(names), len(fields)))}
    return names, field_map
