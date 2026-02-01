# Middle Pane Tree Structure Implementation

## Overview
The middle pane now displays a hierarchical tree structure instead of a flat list, showing:
- **Agencies** (expandable parent nodes)
- **Channel Groups** (child nodes under each agency)

## Structure Changes

### Before:
```
Middle Pane (flat list):
- Agency 1
- Agency 2
- Agency 3

Right Pane:
- All frequencies from all channel groups of selected agency
```

### After:
```
Middle Pane (tree):
- Agency 1 (expandable)
  - Channel Group 1
  - Channel Group 2
  - Channel Group 3
- Agency 2 (expandable)
  - Channel Group A
  - Channel Group B

Right Pane:
- Only frequencies from selected channel group
```

## Implementation Details

### Data Structure
```javascript
agencyTreeNodes: [
  {
    id: 'agency-268',
    type: 'agency',
    name_tag: 'Businesses',
    system_type: 'Conventional',
    enabled: true,
    group_count: 5,
    children: [],
    lazy: true  // Will load on expand
  },
  // ... more agencies
]
```

### User Interaction Flow

1. **Select County** (left pane)
   - Loads agencies for that county
   - Builds agency tree nodes with lazy loading enabled

2. **Expand Agency** (middle pane)
   - Triggers `onAgencyLazyLoad()` 
   - Fetches channel groups for that agency
   - Filters by county/state for proper scoping
   - Adds channel groups as child nodes

3. **Select Channel Group** (middle pane)
   - Triggers `selectNode()` with group node
   - Fetches frequencies for that group
   - Updates right pane with group's frequencies

### Functions Added

#### `onAgencyLazyLoad()`
- Loads channel groups when an agency node is expanded
- Uses hierarchy filters (county, state) for proper scoping
- Returns array of channel group nodes

#### `selectNode()`
- Handles clicking nodes in the tree
- For channel groups: loads and displays frequencies
- For agencies: just sets selectedAgency for context

#### `openChannelGroupDetail()`
- Placeholder for opening detailed view of a channel group
- Currently shows a notification
- Can be extended to navigate to detailed page

### API Changes
No backend API changes were needed. The existing endpoints are used:
- `GET /hpdb/channel-groups/?agency=...&county=...&state=...` (lazy loaded)
- `GET /hpdb/frequencies/?channel_group=...` (on select)

## Performance Considerations

### Lazy Loading
- Agency children (channel groups) are not loaded until agency is expanded
- Reduces initial data load significantly
- M2M query time: ~300-350ms per agency expand

### Virtual Scrolling
- Q-tree handles large hierarchies efficiently
- Frequency table uses virtual scrolling for large datasets

## Benefits

✅ **Better Organization**: Clear hierarchy matching real-world structure  
✅ **Consistent UI**: Three-pane tree navigation instead of mixed controls  
✅ **Proper Scoping**: Each channel group shows only its frequencies  
✅ **Lazy Loading**: No data loaded until explicitly requested  
✅ **Mobile Friendly**: Tree structure works well on responsive layouts  

## Testing Checklist

- [x] Tree renders correctly with agencies
- [x] Clicking expand loads channel groups
- [x] Selecting channel group loads frequencies
- [x] Hierarchy filters (county, state) apply correctly
- [x] No spurious data from other agencies/counties
- [x] Performance acceptable (~300-350ms for lazy loads)

## Files Modified

- `/frontend/src/pages/Index.vue`:
  - Middle pane: Changed from list to tree
  - Right pane: Changed from aggregated frequencies to single group frequencies
  - Added `onAgencyLazyLoad()` function
  - Added `selectNode()` function
  - Added `openChannelGroupDetail()` function
  - Updated data properties: added `agencyTreeNodes`, `selectedChannelGroup`, `channelGroupFrequencies`
  - Updated `selectCounty()` to build tree nodes
  - Removed old `selectAgency()` function
  - Updated frequency columns (removed group_name since single group)

## Future Enhancements

- Add search/filter for agency names
- Add search/filter for channel groups within expanded agencies
- Show frequency count next to each channel group
- Add detail pages for agencies and channel groups
- Add context menu for quick actions
- Add favorites/quick access from this view
