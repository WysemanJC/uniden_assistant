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
      :width="280"
      :breakpoint="500"
      bordered
    >
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        
        <q-item 
          clickable 
          @click="router.push('/')"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          icon="folder"
          label="Data Management"
          default-opened
        >
          <q-item 
            clickable 
            @click="navigateToDatabase"
            active-class="bg-primary text-white"
            class="q-pl-lg"
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
            active
            active-class="bg-primary text-white"
            @click="navigateToFavorites"
            class="q-pl-lg"
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
            @click="router.push('/?section=load-data')"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section avatar>
              <q-icon name="cloud_upload" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Load Data</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <q-expansion-item
          icon="description"
          label="File Specifications"
        >
          <q-item 
            clickable 
            @click="router.push('/?section=spec-readme')"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section>
              <q-item-label>Overview</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            @click="router.push('/?section=global-rules')"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section>
              <q-item-label>Global Parsing Rules</q-item-label>
            </q-item-section>
          </q-item>

          <q-expansion-item
            icon="article"
            label="Record Types"
            header-class="q-pl-lg"
          >
            <q-item 
              clickable 
              @click="router.push('/?section=hpdb-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>HPDB Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=system-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>System Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=favorites-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Favorites Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=scan-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Scan Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=profile-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Scanner/Profile Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=discovery-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Discovery Records</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>

          <q-expansion-item
            icon="table_chart"
            label="Reference Tables"
            header-class="q-pl-lg"
          >
            <q-item 
              clickable 
              @click="router.push('/?section=service-types')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Service Types</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=freq-ctcss-dcs')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>CTCSS/DCS Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=freq-p25')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>P25 NAC Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=freq-dmr')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>DMR Color Code</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=freq-nxdn')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>NXDN RAN/Area</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=display-opts')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=display-colors')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Colors</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              @click="router.push('/?section=display-layouts')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Layouts</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        <!-- Header Card -->
        <q-card v-if="favoriteDetail" flat bordered class="q-mb-md">
          <q-card-section>
            <div class="text-h6 q-mb-sm">{{ favoriteDetail.user_name }}</div>
            <div class="row q-gutter-md">
              <div class="col-auto">
                <div class="text-caption text-grey-7">File</div>
                <div class="text-body2">{{ favoriteDetail.filename }}</div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Total Systems</div>
                <div class="text-body2">{{ favoriteDetail.total_groups }}</div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Total Channels</div>
                <div class="text-body2">{{ favoriteDetail.total_frequencies }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Tree + Table Layout -->
        <div v-if="favoriteDetail" class="row q-col-gutter-md">
          <!-- Left Pane: Tree Structure -->
          <div class="col-12 col-md-3">
            <q-card flat bordered style="height: 100%; min-height: 600px;">
              <q-card-section class="q-pa-sm">
                <div class="text-subtitle2 q-mb-sm">Favorites List Structure</div>
                <q-tree
                  :nodes="treeNodes"
                  node-key="id"
                  v-model:selected="selectedNodeId"
                  default-expand-all
                >
                  <template v-slot:default-header="prop">
                    <div 
                      class="row items-center q-gutter-xs cursor-pointer" 
                      style="flex: 1;"
                      @click.stop="selectNode(prop.node)"
                    >
                      <q-icon 
                        :name="getNodeIcon(prop.node)" 
                        :color="getNodeColor(prop.node)" 
                        size="sm"
                      />
                      <span class="text-body2">{{ prop.node.label }}</span>
                      <q-badge 
                        v-if="prop.node.type === 'department' && prop.node.channel_count"
                        :label="prop.node.channel_count"
                        color="blue"
                        class="q-ml-xs"
                      />
                    </div>
                  </template>
                </q-tree>
              </q-card-section>
            </q-card>
          </div>

          <!-- Right Pane: Channel Table -->
          <div class="col-12 col-md-9">
            <q-card flat bordered style="height: 100%; min-height: 600px;">
              <q-card-section class="q-pa-sm">
                <div v-if="selectedDepartment">
                  <div class="row items-center q-mb-md">
                    <div class="col">
                      <div class="text-h6">{{ selectedDepartment.label }}</div>
                      <div class="text-caption text-grey-7">Channels</div>
                    </div>
                  </div>

                  <div v-if="departmentChannels.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                    <q-table
                      :rows="departmentChannels"
                      :columns="channelColumns"
                      row-key="id"
                      flat
                      dense
                      :rows-per-page-options="[0]"
                      virtual-scroll
                      style="max-height: calc(100vh - 380px);"
                    >
                      <template #body-cell-frequency="props">
                        <q-td :props="props">
                          {{ (props.value / 1000000).toFixed(4) }} MHz
                        </q-td>
                      </template>
                      <template #body-cell-enabled="props">
                        <q-td :props="props">
                          <q-icon 
                            :name="props.value ? 'check_circle' : 'cancel'" 
                            :color="props.value ? 'positive' : 'negative'"
                            size="xs"
                          />
                        </q-td>
                      </template>
                    </q-table>
                  </div>

                  <div v-else class="text-center q-pa-xl text-grey-7">
                    <q-icon name="info" size="2em" />
                    <div class="q-mt-md text-caption">No channels found</div>
                  </div>
                </div>

                <div v-else class="text-center q-pa-xl text-grey-7">
                  <q-icon name="radio" size="3em" />
                  <div class="q-mt-md">Select a department from the tree to view channels</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <q-inner-loading :showing="loading" />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import api from '../api'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const leftDrawerOpen = ref(true)
const favoriteDetail = ref(null)
const loading = ref(false)
const selectedNodeId = ref(null)
const selectedDepartment = ref(null)

const channelColumns = [
  { name: 'name', label: 'Name', field: 'name', align: 'left', sortable: true },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'nac', label: 'Tone/NAC', field: 'nac', align: 'left', sortable: true },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' }
]

// Build tree structure from groups
const treeNodes = computed(() => {
  if (!favoriteDetail.value || !favoriteDetail.value.groups) return []
  
  // Group by system type (for now, single level - can be expanded)
  const favoritesNode = {
    id: 'root',
    label: favoriteDetail.value.user_name,
    type: 'favorites_list',
    children: []
  }
  
  // Add each system as a child with departments
  favoriteDetail.value.groups.forEach((group, idx) => {
    const systemNode = {
      id: `system_${idx}`,
      label: `System ${idx + 1}`,
      type: 'system',
      children: [{
        id: `dept_${idx}`,
        label: group.name,
        type: 'department',
        channel_count: group.freq_count,
        groupData: group
      }]
    }
    favoritesNode.children.push(systemNode)
  })
  
  return [favoritesNode]
})

// Get channels for selected department
const departmentChannels = computed(() => {
  if (!selectedDepartment.value || !selectedDepartment.value.groupData) return []
  return selectedDepartment.value.groupData.channels || []
})

const goBack = () => {
  router.push('/?section=favorites')
}

const navigateToDatabase = () => {
  router.push('/?section=database')
}

const navigateToFavorites = () => {
  router.push('/?section=favorites')
}

const selectNode = (node) => {
  if (node.type === 'department') {
    selectedDepartment.value = node
    selectedNodeId.value = node.id
  }
}

const getNodeIcon = (node) => {
  switch (node.type) {
    case 'favorites_list': return 'star'
    case 'system': return 'folder'
    case 'department': return 'radio'
    default: return 'circle'
  }
}

const getNodeColor = (node) => {
  switch (node.type) {
    case 'favorites_list': return 'amber'
    case 'system': return 'blue'
    case 'department': return 'green'
    default: return 'grey'
  }
}

const loadFavoriteDetail = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/usersettings/favorites-lists/${route.params.id}/detail/`)
    favoriteDetail.value = data
  } catch (error) {
    console.error('Error loading favorite detail:', error)
    $q.notify({ type: 'negative', message: 'Failed to load favorite details' })
    router.push('/?section=favorites')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFavoriteDetail()
})
</script>
