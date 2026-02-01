<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-btn flat round dense icon="arrow_back" @click="goBack" class="q-ml-sm" />
        <q-toolbar-title>{{ agencyDetail?.name || 'Agency Detail' }}</q-toolbar-title>
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
          @click="router.push('/')"
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
          active
          active-class="bg-primary text-white"
          @click="navigateToDatabase"
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
          @click="navigateToFavorites"
        >
          <q-item-section avatar>
            <q-icon name="star" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Favourites</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        <q-card v-if="agencyDetail" flat bordered class="q-mb-md">
          <q-card-section>
            <div class="row q-mb-md q-gutter-md">
              <div class="col-auto">
                <div class="text-caption text-grey-7">System Type</div>
                <div class="text-body1">
                  <q-chip :label="agencyDetail.system_type" size="sm" color="primary" />
                </div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Status</div>
                <div class="text-body1">
                  <q-toggle v-model="agencyDetail.enabled" label="Enabled" />
                </div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Total Groups</div>
                <div class="text-body1">{{ agencyDetail.group_count || 0 }}</div>
              </div>
            </div>
            
            <div v-if="agencyDetail.states && agencyDetail.states.length" class="q-mb-sm">
              <div class="text-caption text-grey-7">States</div>
              <q-chip
                v-for="state in agencyDetail.states"
                :key="state.id"
                :label="state.name"
                size="sm"
                outline
                color="blue"
                class="q-mr-xs"
              />
            </div>
            
            <div v-if="agencyDetail.counties && agencyDetail.counties.length" class="q-mb-sm">
              <div class="text-caption text-grey-7">Counties</div>
              <q-chip
                v-for="county in agencyDetail.counties"
                :key="county.id"
                :label="county.name"
                size="sm"
                outline
                color="teal"
                class="q-mr-xs q-mb-xs"
              />
            </div>
          </q-card-section>
        </q-card>

        <div v-if="channelGroups && channelGroups.length" class="q-mt-md">
          <q-expansion-item
            v-for="group in channelGroups"
            :key="group.id"
            :label="`${group.name} (${group.frequency_count || 0} frequencies)`"
            class="q-mb-md bg-white"
            icon="cell_tower"
            header-class="bg-blue-1"
            default-opened
          >
            <q-card>
              <q-card-section>
                <div class="row q-gutter-md q-mb-md">
                  <div class="col-auto">
                    <div class="text-caption text-grey-7">Location Type</div>
                    <div class="text-body2">{{ group.location_type || 'N/A' }}</div>
                  </div>
                  <div class="col-auto" v-if="group.latitude">
                    <div class="text-caption text-grey-7">Latitude</div>
                    <div class="text-body2">{{ group.latitude }}</div>
                  </div>
                  <div class="col-auto" v-if="group.longitude">
                    <div class="text-caption text-grey-7">Longitude</div>
                    <div class="text-body2">{{ group.longitude }}</div>
                  </div>
                  <div class="col-auto" v-if="group.range_miles">
                    <div class="text-caption text-grey-7">Range</div>
                    <div class="text-body2">{{ group.range_miles }} miles</div>
                  </div>
                </div>
                
                <q-table
                  v-if="group.frequencies && group.frequencies.length"
                  :rows="group.frequencies"
                  :columns="frequencyColumns"
                  row-key="id"
                  flat
                  dense
                  :pagination="{ rowsPerPage: 0 }"
                />
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </div>

        <div v-else-if="!loading" class="text-center text-grey-6 q-mt-xl">
          <q-icon name="info" size="lg" class="q-mb-md" />
          <div class="text-body1">No channel groups found for this agency</div>
        </div>

        <q-inner-loading :showing="loading" />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import api from '../api'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const leftDrawerOpen = ref(true)
const agencyDetail = ref(null)
const channelGroups = ref([])
const loading = ref(false)

const frequencyColumns = [
  { name: 'name', label: 'Name', field: 'name', align: 'left', sortable: true },
  { name: 'frequency', label: 'Frequency (Hz)', field: 'frequency', align: 'left', sortable: true, format: val => val.toLocaleString() },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'tone', label: 'Tone', field: 'tone', align: 'left', sortable: true },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center', format: val => val ? 'Yes' : 'No' }
]

const goBack = () => {
  router.push('/?section=database')
}

const navigateToDatabase = () => {
  router.push('/?section=database')
}

const navigateToFavorites = () => {
  router.push('/?section=favorites')
}

const loadAgencyDetail = async () => {
  loading.value = true
  try {
    // Load agency details
    const { data: agency } = await api.get(`/uniden_manager/hpdb/agencies/${route.params.id}/`)
    agencyDetail.value = agency
    
    // Load channel groups for this agency
    const { data: groupsResponse } = await api.get(`/uniden_manager/hpdb/channel-groups/?agency=${route.params.id}`)
    const groups = Array.isArray(groupsResponse) ? groupsResponse : (groupsResponse.results || [])
    
    // Load frequencies for each group
    const groupsWithFrequencies = await Promise.all(
      groups.map(async (group) => {
        try {
          const { data: frequencies } = await api.get(`/uniden_manager/hpdb/frequencies/?channel_group=${group.id}`)
          return {
            ...group,
            frequencies: Array.isArray(frequencies) ? frequencies : (frequencies.results || [])
          }
        } catch (error) {
          console.error(`Error loading frequencies for group ${group.id}:`, error)
          return {
            ...group,
            frequencies: []
          }
        }
      })
    )
    
    channelGroups.value = groupsWithFrequencies
  } catch (error) {
    console.error('Error loading agency detail:', error)
    $q.notify({ type: 'negative', message: 'Failed to load agency details' })
    router.push('/?section=database')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAgencyDetail()
})
</script>
