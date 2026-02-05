<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat round dense icon="arrow_back" @click="goBack" />
        <q-toolbar-title>Quick Reference</q-toolbar-title>
        <q-select
          v-model="viewFilter"
          :options="filterOptions"
          dense
          outlined
          emit-value
          map-options
          style="width: 200px; margin-right: 16px"
          class="bg-white text-dark"
        />
        <q-btn flat round dense icon="print" @click="printPage" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-md">
        <div v-if="loading" class="row items-center justify-center q-pa-lg">
          <q-spinner size="32px" />
          <div class="q-ml-sm">Loading quick reference…</div>
        </div>

        <!-- All view -->
        <div v-if="!loading && viewFilter === 'all'" class="row q-col-gutter-md">
          <div
            v-for="card in quickReferenceCards"
            :key="card.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3"
          >
            <q-card flat bordered>
              <q-card-section class="row items-center">
                <div class="text-subtitle1">{{ card.name }}</div>
                <q-space />
                <q-badge color="primary" :label="card.quickKeyDisplay" />
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div v-if="card.systems.length === 0" class="text-caption text-grey-7">
                  No systems
                </div>
                <div v-else>
                  <div v-for="system in card.systems" :key="system.key" class="q-mb-sm">
                    <div class="row items-center">
                      <div class="text-body2">{{ system.name }}</div>
                      <q-space />
                      <q-badge color="secondary" :label="system.quickKeyDisplay" />
                    </div>
                    <div v-if="system.departments.length > 0" class="q-ml-md q-mt-xs">
                      <div
                        v-for="dept in system.departments"
                        :key="dept.key"
                        class="row items-center q-mb-xs"
                      >
                        <div class="text-caption">{{ dept.name }}</div>
                        <q-space />
                        <q-badge color="grey-7" text-color="white" :label="dept.quickKeyDisplay" />
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Favourites and Systems view -->
        <div v-if="!loading && viewFilter === 'favSys'" class="row q-col-gutter-md">
          <div
            v-for="card in quickReferenceCards"
            :key="card.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3"
          >
            <q-card flat bordered>
              <q-card-section class="row items-center">
                <div class="text-subtitle1">{{ card.name }}</div>
                <q-space />
                <q-badge color="primary" :label="card.quickKeyDisplay" />
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div v-if="card.systems.length === 0" class="text-caption text-grey-7">
                  No systems
                </div>
                <div v-else>
                  <div v-for="system in card.systems" :key="system.key" class="q-mb-sm">
                    <div class="row items-center">
                      <div class="text-body2">{{ system.name }}</div>
                      <q-space />
                      <q-badge color="secondary" :label="system.quickKeyDisplay" />
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Favourites Only view -->
        <div v-if="!loading && viewFilter === 'favOnly'" class="row">
          <div class="col-auto">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6">Favourites Quick Keys</div>
              </q-card-section>
              <q-separator />
              <q-card-section>
                <div class="favs-only-list">
                  <div class="row items-center q-mb-sm" v-for="card in quickReferenceCards" :key="card.id">
                    <div class="text-body2">{{ card.name }}</div>
                    <q-space />
                    <q-badge color="primary" :label="card.quickKeyDisplay" />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import api from '../api'

const router = useRouter()
const $q = useQuasar()

const loading = ref(false)
const favorites = ref([])
const systemsByFav = ref({})
const viewFilter = ref('all')
const filterOptions = [
  { label: 'All', value: 'all' },
  { label: 'Favourites and Systems', value: 'favSys' },
  { label: 'Favourites Only', value: 'favOnly' }
]

const goBack = () => {
  router.push('/?section=favorites')
}

const printPage = () => {
  window.print()
}

const formatQuickKey = (value) => {
  if (value === null || value === undefined) return 'Off'
  const raw = String(value).trim()
  if (raw === '' || raw.toLowerCase() === 'off') return 'Off'
  const num = parseInt(raw, 10)
  if (isNaN(num)) return raw
  return num.toString().padStart(2, '0')
}

const quickKeySortValue = (value) => {
  if (value === null || value === undefined) return Number.POSITIVE_INFINITY
  const raw = String(value).trim()
  if (raw === '' || raw.toLowerCase() === 'off') return Number.POSITIVE_INFINITY
  const num = parseInt(raw, 10)
  return isNaN(num) ? Number.POSITIVE_INFINITY : num
}

const buildQuickKeyChain = (parts) => parts.map(formatQuickKey).join('.')

const isQuickKeyActive = (value) => {
  if (value === null || value === undefined) return false
  const raw = String(value).trim().toLowerCase()
  return raw !== '' && raw !== 'off'
}

const quickReferenceCards = computed(() => {
  const cards = (favorites.value || []).map((fav) => {
    const favKey = fav.quick_key ?? 'Off'
    if (!isQuickKeyActive(favKey)) return null
    const favName = fav.user_name || fav.filename || 'Favourite List'
    const systemsList = systemsByFav.value[fav.id] || []
    const systemMap = new Map()

    systemsList.forEach((sys) => {
      const systemName = sys.system_name || sys.name || 'Unknown System'
      const systemType = sys.system_type || sys.type || 'Unknown'
      const key = `${systemType}__${systemName}`
      if (!systemMap.has(key)) {
        systemMap.set(key, {
          key,
          name: systemName,
          system_type: systemType,
          quick_key: sys.quick_key ?? 'Off',
          departments: []
        })
      }
    })

    const groups = Array.isArray(fav.groups) ? fav.groups : []
    groups.forEach((group, idx) => {
      if (group.is_system_placeholder) return
      const systemName = group.system_name || 'Unknown System'
      const systemType = group.system_type || 'Conventional'
      const key = `${systemType}__${systemName}`
      if (!systemMap.has(key)) {
        systemMap.set(key, {
          key,
          name: systemName,
          system_type: systemType,
          quick_key: 'Off',
          departments: []
        })
      }
      const deptQuickKey = group.quick_key ?? 'Off'
      if (!isQuickKeyActive(deptQuickKey)) return
      systemMap.get(key).departments.push({
        key: `dept_${fav.id}_${group.id || idx}`,
        name: group.name_tag || `Department ${idx + 1}`,
        quick_key: deptQuickKey
      })
    })

    const systems = Array.from(systemMap.values())
      .filter((system) => isQuickKeyActive(system.quick_key))
      .map((system) => {
        const departments = system.departments
          .slice()
          .sort((a, b) => {
            const av = quickKeySortValue(a.quick_key)
            const bv = quickKeySortValue(b.quick_key)
            if (av !== bv) return av - bv
            return (a.name || '').localeCompare(b.name || '')
          })
          .map((dept) => ({
            ...dept,
            quickKeyDisplay: buildQuickKeyChain([favKey, system.quick_key, dept.quick_key])
          }))

        return {
          ...system,
          quickKeyDisplay: buildQuickKeyChain([favKey, system.quick_key]),
          departments
        }
      })
      .sort((a, b) => {
        const av = quickKeySortValue(a.quick_key)
        const bv = quickKeySortValue(b.quick_key)
        if (av !== bv) return av - bv
        return (a.name || '').localeCompare(b.name || '')
      })

    return {
      id: fav.id,
      name: favName,
      quick_key: favKey,
      quickKeyDisplay: formatQuickKey(favKey),
      systems
    }
  })

  return cards
    .filter(Boolean)
    .sort((a, b) => {
      const av = quickKeySortValue(a.quick_key)
      const bv = quickKeySortValue(b.quick_key)
      if (av !== bv) return av - bv
      return (a.name || '').localeCompare(b.name || '')
    })
})

const loadData = async () => {
  loading.value = true
  try {
    // Load favorites lists
    const { data } = await api.get('/favourites/favorites-lists/')
    let favList = Array.isArray(data) ? data : (data.results || [])
    favList.sort((a, b) => (a.filename || '').localeCompare(b.filename || ''))

    // Load detailed info for each favorite
    const favListsWithDetails = await Promise.all(
      favList.map(async (fav) => {
        try {
          const { data: detailData } = await api.get(`/favourites/favorites-lists/${fav.id}/detail/`)
          return { ...fav, ...detailData }
        } catch (err) {
          return fav
        }
      })
    )

    favorites.value = favListsWithDetails

    // Load systems for each favorite
    const systemsMap = {}
    await Promise.all(
      favListsWithDetails.map(async (fav) => {
        try {
          const { data } = await api.get(`/favourites/favorites-lists/${fav.id}/get-systems/`)
          systemsMap[fav.id] = data.systems || []
        } catch (error) {
          systemsMap[fav.id] = []
        }
      })
    )
    systemsByFav.value = systemsMap
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to load quick reference data' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* Favourites Only view - 3 columns for both screen and print */
.favs-only-list {
  column-count: 3;
  column-gap: 24px;
  column-rule: 1px solid #ddd;
}

.favs-only-list .row {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* Grid layout for cards - 2 columns for 1/4 page layout */
.row.q-col-gutter-md {
  display: grid !important;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin: 0 !important;
}

.row.q-col-gutter-md > div {
  width: auto !important;
  max-width: none !important;
  flex: none !important;
  page-break-inside: avoid;
  break-inside: avoid;
}

/* Individual reference cards - compact */
.q-card {
  page-break-inside: avoid;
  break-inside: avoid;
  border: 1px solid #ddd !important;
  margin: 0 !important;
}

.q-card .q-card-section {
  padding: 9px !important;
}

/* Typography adjustments - larger */
.text-subtitle1 {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.text-body2 {
  font-size: 0.75rem;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.text-caption {
  font-size: 0.68rem;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Badges - larger */
.q-badge {
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
  font-size: 0.68rem;
  padding: 3px 6px;
  min-height: auto;
  white-space: nowrap;
}

/* Separators - larger spacing */
.q-separator {
  print-color-adjust: exact;
  -webkit-print-color-adjust: exact;
  margin: 6px 0 !important;
}

/* Spacing between items */
.q-mb-sm {
  margin-bottom: 6px !important;
}

.q-mb-xs {
  margin-bottom: 4px !important;
}

.q-mt-xs {
  margin-top: 4px !important;
}

.q-ml-md {
  margin-left: 12px !important;
}

/* Loading spinner - hide */
.q-spinner {
  display: none !important;
}

/* Compact row spacing */
.row.items-center {
  min-height: auto;
  flex-wrap: nowrap !important;
}

/* Ensure q-space doesn't cause wrapping */
.q-space {
  flex: 1 1 auto;
  min-width: 4px;
}

@media print {
  @page {
    size: landscape;
    margin: 0.25in;
  }

  /* Hide header when printing */
  .q-header {
    display: none !important;
  }

  /* Remove padding for print */
  .q-page {
    padding: 0 !important;
  }
}
</style>
