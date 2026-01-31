<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>Uniden Assistant</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="250"
      :breakpoint="500"
      bordered
    >
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        
        <q-item 
          clickable 
          :active="activeSection === 'home'" 
          @click="activeSection = 'home'"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>

        <q-item 
          clickable 
          :active="activeSection === 'database'" 
          @click="activeSection = 'database'"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="storage" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Database</q-item-label>
          </q-item-section>
        </q-item>

        <q-item 
          clickable 
          :active="activeSection === 'favorites'" 
          @click="activeSection = 'favorites'"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="star" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Favourites</q-item-label>
          </q-item-section>
        </q-item>

        <q-item 
          clickable 
          :active="activeSection === 'load-data'" 
          @click="activeSection = 'load-data'"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="cloud_upload" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Load Data</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        
        <!-- Home Section -->
        <div v-if="activeSection === 'home'">
          <div class="text-h4 q-mb-md">HPDB and Favourites Statistics</div>
          <div class="text-body1 q-mb-lg">
            Live totals from the HPDB and Favourites databases.
          </div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-lg-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="storage" color="primary" size="sm" class="q-mr-sm" />
                    HPDB Statistics
                  </div>
                  <div v-if="statsLoading" class="q-py-md">
                    <q-spinner color="primary" size="24px" />
                  </div>
                  <div v-else-if="hpdbStats" class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Countries</div>
                      <div class="text-h6">{{ hpdbStats.countries }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">States</div>
                      <div class="text-h6">{{ hpdbStats.states }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Counties</div>
                      <div class="text-h6">{{ hpdbStats.counties }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Agencies</div>
                      <div class="text-h6">{{ hpdbStats.agencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Systems</div>
                      <div class="text-h6">{{ hpdbStats.systems }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Departments</div>
                      <div class="text-h6">{{ hpdbStats.departments }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channel Groups</div>
                      <div class="text-h6">{{ hpdbStats.channel_groups }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channels</div>
                      <div class="text-h6">{{ hpdbStats.channels }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Frequencies</div>
                      <div class="text-h6">{{ hpdbStats.frequencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Conventional</div>
                      <div class="text-h6">{{ hpdbStats.system_types?.conventional || 0 }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Trunk</div>
                      <div class="text-h6">{{ hpdbStats.system_types?.trunk || 0 }}</div>
                    </div>
                  </div>
                  <div v-else class="text-body2 text-grey-7">No HPDB statistics available.</div>
                </q-card-section>
              </q-card>
            </div>

            <div class="col-12 col-lg-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="star" color="primary" size="sm" class="q-mr-sm" />
                    Favourites Statistics
                  </div>
                  <div v-if="statsLoading" class="q-py-md">
                    <q-spinner color="primary" size="24px" />
                  </div>
                  <div v-else-if="favoritesStats" class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Profiles</div>
                      <div class="text-h6">{{ favoritesStats.profiles }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Favourites Lists</div>
                      <div class="text-h6">{{ favoritesStats.favorites_lists }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Agencies</div>
                      <div class="text-h6">{{ favoritesStats.agencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channel Groups</div>
                      <div class="text-h6">{{ favoritesStats.channel_groups }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channels</div>
                      <div class="text-h6">{{ favoritesStats.channels }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Frequencies</div>
                      <div class="text-h6">{{ favoritesStats.frequencies }}</div>
                    </div>
                  </div>
                  <div v-else class="text-body2 text-grey-7">No favourites statistics available.</div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Database Editor Section -->
        <div v-if="activeSection === 'database'">
          <div class="text-h5 q-mb-md">HPDB Database Editor</div>
          <div class="text-body2 text-grey-7 q-mb-lg">
            Browse and search the Uniden Homepatrol database organized by Country &gt; State &gt; County
          </div>

          <q-input
            v-model="searchQuery"
            label="Search agencies..."
            outlined
            dense
            class="q-mb-md"
            style="max-width: 500px"
          >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <q-tree
            :nodes="hpdbTree"
            node-key="id"
            label-key="name"
            children-key="children"
            v-model:expanded="expandedNodes"
            @lazy-load="onLazyLoad"
            :filter="searchQuery"
            :filter-method="filterMethod"
          >
            <template #default-header="prop">
              <div 
                class="row items-center q-gutter-sm" 
                style="flex: 1;"
                :class="{ 'cursor-pointer': prop.node.type === 'agency' }"
                @click="prop.node.type === 'agency' ? openAgencyDetail(prop.node) : null"
              >
                <q-icon 
                  :name="getNodeIcon(prop.node)" 
                  :color="getNodeColor(prop.node)" 
                />
                <span>{{ prop.node.name }}</span>
                
                <!-- County info -->
                <span v-if="prop.node.type === 'county'" class="text-caption text-grey-7">
                  (County)
                </span>
                
                <!-- Agency info -->
                <q-badge 
                  v-if="prop.node.type === 'agency' && prop.node.group_count" 
                  :label="prop.node.group_count + ' groups'" 
                  color="blue" 
                />
                <q-chip 
                  v-if="prop.node.type === 'agency'" 
                  :label="prop.node.system_type" 
                  size="sm" 
                  dense 
                />
                <q-toggle
                  v-if="prop.node.type === 'agency'"
                  v-model="prop.node.enabled"
                  dense
                  @click.stop
                />
                
                <!-- Channel Group info -->
                <span v-if="prop.node.type === 'group'" class="text-caption text-grey-7">
                  ({{ prop.node.location_type || 'Location' }})
                </span>
              </div>
            </template>
          </q-tree>
        </div>

        <!-- Favourites Editor Section -->
        <div v-if="activeSection === 'favorites'">
          <div class="text-h5 q-mb-md">Favourites Editor</div>
          <div class="row q-mb-md q-gutter-sm">
            <q-btn
              color="primary"
              label="Export to SD Card Directory"
              icon="save"
              @click="exportToSd"
            />
            <q-btn
              color="secondary"
              label="New Profile"
              icon="add"
              @click="showCreateDialog = true"
            />
          </div>

          <q-table
            :rows="favorites"
            :columns="favoritesColumns"
            row-key="id"
            :loading="favoritesLoading"
            @row-click="openFavoriteDetail"
            class="cursor-pointer"
          />
        </div>

        <!-- Load Data Section -->
        <div v-if="activeSection === 'load-data'">
          <div class="text-h5 q-mb-md">Load Data</div>
          <div class="text-body2 text-grey-7 q-mb-lg">
            Upload HPDB database files or favourites files.
          </div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="storage" color="primary" size="sm" class="q-mr-sm" />
                    Load HPDB Database
                  </div>
                  <div class="text-body2">
                    Select a directory containing hpdb.cfg and s_*.hpd files.
                  </div>
                  <q-file
                    ref="hpdbFilePicker"
                    v-model="hpdbFiles"
                    class="q-mt-md"
                    filled
                    multiple
                    use-chips
                    label="Select HPDB directory"
                    accept=".cfg,.hpd"
                    :directory="true"
                    :webkitdirectory="true"
                  />
                </q-card-section>
                <q-card-actions>
                  <q-btn
                    flat
                    color="primary"
                    label="Choose Directory"
                    @click="openHpdbPicker"
                  />
                  <q-btn
                    flat
                    color="primary"
                    label="Load HPDB"
                    :loading="hpdbImportLoading"
                    @click="importHpdb"
                  />
                </q-card-actions>
              </q-card>
            </div>

            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="star" color="primary" size="sm" class="q-mr-sm" />
                    Load Favourites
                  </div>
                  <div class="text-body2">
                    Select a directory containing f_list.cfg and favourites .hpd files.
                  </div>
                  <q-file
                    ref="favoritesFilePicker"
                    v-model="favoritesFiles"
                    class="q-mt-md"
                    filled
                    multiple
                    use-chips
                    label="Select Favourites directory"
                    accept=".cfg,.hpd"
                    :directory="true"
                    :webkitdirectory="true"
                  />
                </q-card-section>
                <q-card-actions>
                  <q-btn
                    flat
                    color="primary"
                    label="Choose Directory"
                    @click="openFavoritesPicker"
                  />
                  <q-btn
                    flat
                    color="primary"
                    label="Load Favourites"
                    :loading="favoritesImportLoading"
                    @click="importFavorites"
                  />
                </q-card-actions>
              </q-card>
            </div>
          </div>
        </div>

      </q-page>
    </q-page-container>

    <q-dialog v-model="showCreateDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Create New Profile</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showCreateDialog = false" />
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="newProfile.name"
            label="Profile Name"
            class="q-mb-md"
          />
          <q-input
            v-model="newProfile.model"
            label="Scanner Model"
            class="q-mb-md"
          />
          <q-input
            v-model="newProfile.firmware_version"
            label="Firmware Version"
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showCreateDialog = false" />
          <q-btn
            flat
            label="Create"
            color="primary"
            @click="createNewProfile"
            :loading="scanner.loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- SD card import dialog removed; use Load Data page uploads -->
  </q-layout>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScannerStore } from '../stores/scanner'
import api, { sdAPI } from '../api'
import { useQuasar } from 'quasar'

const route = useRoute()
const router = useRouter()
const scanner = useScannerStore()
const $q = useQuasar()

// Navigation
const leftDrawerOpen = ref(true)
const activeSection = ref('home')

// HPDB Tree
const hpdbTree = ref([])
const expandedNodes = ref([])
const searchQuery = ref('')
const hpdbImportLoading = ref(false)
const favoritesImportLoading = ref(false)
const statsLoading = ref(false)
const hpdbStats = ref(null)
const favoritesStats = ref(null)

// Favourites
const favorites = ref([])
const favoritesLoading = ref(false)
const favoritesColumns = [
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'filename', label: 'File', field: 'filename', align: 'left' },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' },
  { name: 'disabled_on_power', label: 'Disable on Power Up', field: 'disabled_on_power', align: 'center' },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center' },
  { name: 'list_number', label: 'List #', field: 'list_number', align: 'center' }
]

const showCreateDialog = ref(false)
const hpdbFiles = ref([])
const favoritesFiles = ref([])
const hpdbFilePicker = ref(null)
const favoritesFilePicker = ref(null)
const newProfile = ref({
  name: '',
  model: '',
  firmware_version: ''
})

onMounted(() => {
  // Check for section query parameter
  const section = route.query.section
  if (section && ['home', 'database', 'favorites'].includes(section)) {
    activeSection.value = section
  }
  
  scanner.fetchProfiles()
  loadHPDBTree()
  loadFavoritesList()
  loadStats()
})

const loadStats = async () => {
  statsLoading.value = true
  try {
    const [hpdbResp, favResp] = await Promise.all([
      api.get('/hpdb/stats/'),
      api.get('/usersettings/stats/')
    ])
    hpdbStats.value = hpdbResp.data
    favoritesStats.value = favResp.data
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to load statistics' })
  } finally {
    statsLoading.value = false
  }
}

// HPDB Tree Methods
const loadHPDBTree = async () => {
  try {
    const { data } = await api.get('/hpdb/tree/tree/')
    // Mark agencies as lazy-loadable for channel groups
    const markLazy = (nodes) => {
      nodes.forEach(node => {
        if (node.type === 'agency' && node.group_count > 0) {
          node.lazy = true
        }
        if (node.children) {
          markLazy(node.children)
        }
      })
    }
    markLazy(data)
    hpdbTree.value = data
  } catch (error) {
    console.error('Error loading HPDB tree:', error)
    $q.notify({ type: 'negative', message: 'Failed to load database tree' })
  }
}

const expandAgencyGroups = async (agencyId) => {
  try {
    // Extract numeric ID from node ID (e.g., "agency-268" -> "268")
    const numericId = agencyId.toString().replace('agency-', '')
    const { data } = await api.get(`/hpdb/channel-groups/?agency=${numericId}`)
    // Handle paginated response
    const groups = data.results || []
    return groups.map(group => ({
      id: `group-${group.id}`,
      type: 'group',
      name: group.name,
      location_type: group.location_type,
      latitude: group.latitude,
      longitude: group.longitude,
      range_miles: group.range_miles,
      frequency_count: group.frequency_count
    }))
  } catch (error) {
    console.error('Error loading channel groups:', error)
    return []
  }
}

const loadFavoritesList = async () => {
  favoritesLoading.value = true
  try {
    const { data } = await api.get('/usersettings/favorites-lists/')
    // Handle paginated response
    favorites.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    console.error('Error loading favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to load favourites list' })
  } finally {
    favoritesLoading.value = false
  }
}

const openFavoriteDetail = (evt, row) => {
  router.push(`/favorite/${row.id}`)
}

const getNodeIcon = (node) => {
  switch (node.type) {
    case 'country': return 'public'
    case 'state': return 'map'
    case 'county': return 'location_city'
    case 'agency': return 'radio'
    case 'group': return 'waves'
    default: return 'folder'
  }
}

const getNodeColor = (node) => {
  switch (node.type) {
    case 'country': return 'blue'
    case 'state': return 'green'
    case 'county': return 'orange'
    case 'agency': return node.enabled ? 'primary' : 'grey'
    case 'group': return 'purple'
    default: return 'grey'
  }
}

const onLazyLoad = (node) => {
  // Lazy load channel groups when agency node is expanded
  if (node.node.type === 'agency') {
    return new Promise((resolve, reject) => {
      expandAgencyGroups(node.node.id).then(children => {
        node.done(children)
      }).catch(error => {
        node.fail()
        $q.notify({ type: 'negative', message: 'Failed to load channel groups' })
      })
    })
  }
}

const filterMethod = (node, filter) => {
  const filt = filter.toLowerCase()
  return node.name.toLowerCase().includes(filt)
}

const openAgencyDetail = (node) => {
  // Extract numeric ID from node.id (format is "agency-123")
  const agencyId = node.id.toString().replace('agency-', '')
  router.push(`/database/${agencyId}`)
}

// Import/Export Methods

const validateHpdbFiles = (files) => {
  const names = files.map(f => f.name.toLowerCase())
  const hasCfg = names.includes('hpdb.cfg')
  const hasSystem = names.some(n => n.startsWith('s_') && n.endsWith('.hpd'))
  return { hasCfg, hasSystem }
}

const validateFavoritesFiles = (files) => {
  const names = files.map(f => f.name.toLowerCase())
  const hasCfg = names.includes('f_list.cfg')
  const hasHpd = names.some(n => n.endsWith('.hpd'))
  return { hasCfg, hasHpd }
}

const triggerFilePicker = (pickerRef) => {
  const el = pickerRef?.value?.$el
  const input = el?.querySelector('input[type="file"]')
  input?.click()
}

const openHpdbPicker = () => {
  triggerFilePicker(hpdbFilePicker)
}

const openFavoritesPicker = () => {
  triggerFilePicker(favoritesFilePicker)
}

const importHpdb = async () => {
  const files = Array.isArray(hpdbFiles.value)
    ? hpdbFiles.value
    : Array.from(hpdbFiles.value || [])
  if (files.length === 0) {
    openHpdbPicker()
    return
  }
  const { hasCfg, hasSystem } = validateHpdbFiles(files)
  if (!hasCfg || !hasSystem) {
    $q.notify({ type: 'negative', message: 'HPDB upload requires hpdb.cfg and at least one s_*.hpd file.' })
    return
  }

  hpdbImportLoading.value = true
  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    const { data } = await api.post('/hpdb/import-files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (data.errors?.length) {
      $q.notify({ type: 'warning', message: `HPDB import completed with ${data.errors.length} error(s)` })
    } else {
      $q.notify({ type: 'positive', message: `HPDB import completed (${data.imported} files)` })
    }
    await loadHPDBTree()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'HPDB import failed: ' + (error.response?.data?.error || error.message) })
  } finally {
    hpdbImportLoading.value = false
  }
}

const importFavorites = async () => {
  const files = Array.isArray(favoritesFiles.value)
    ? favoritesFiles.value
    : Array.from(favoritesFiles.value || [])
  if (files.length === 0) {
    openFavoritesPicker()
    return
  }
  const { hasCfg, hasHpd } = validateFavoritesFiles(files)
  if (!hasCfg || !hasHpd) {
    $q.notify({ type: 'negative', message: 'Favourites upload requires f_list.cfg and at least one .hpd file.' })
    return
  }

  favoritesImportLoading.value = true
  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    const { data } = await api.post('/usersettings/import-files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (data.errors?.length) {
      $q.notify({ type: 'warning', message: `Imported with ${data.errors.length} error(s)` })
    } else {
      $q.notify({ type: 'positive', message: `Imported ${data.imported} profile(s)` })
    }
    await scanner.fetchProfiles()
    await loadFavoritesList()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Favourites import failed: ' + (error.response?.data?.error || error.message) })
  } finally {
    favoritesImportLoading.value = false
  }
}

const exportToSd = async () => {
  try {
    const { data } = await sdAPI.exportToSd()
    if (data.errors?.length) {
      $q.notify({ type: 'warning', message: `Exported with ${data.errors.length} error(s)` })
    } else {
      $q.notify({ type: 'positive', message: `Exported ${data.exported} profile(s)` })
    }
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Export failed: ' + error.message })
  }
}

const createNewProfile = async () => {
  try {
    await scanner.createProfile(newProfile.value)
    showCreateDialog.value = false
    newProfile.value = { name: '', model: '', firmware_version: '' }
  } catch (error) {
    console.error('Error creating profile:', error)
  }
}

const openProfile = (row) => {
  router.push(`/profile/${row.id}`)
}

const deleteProfile = async (id) => {
  if (confirm('Are you sure you want to delete this profile?')) {
    try {
      await scanner.deleteProfile(id)
    } catch (error) {
      console.error('Error deleting profile:', error)
    }
  }
}
</script>
