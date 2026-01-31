<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-btn flat round dense icon="arrow_back" @click="goBack" class="q-ml-sm" />
        <q-toolbar-title>{{ favoriteDetail?.name || 'Favorite Detail' }}</q-toolbar-title>
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
          active
          active-class="bg-primary text-white"
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
        <q-card v-if="favoriteDetail" flat bordered>
          <q-card-section>
            <div class="row q-mb-md q-gutter-md">
              <div class="col-auto">
                <div class="text-caption text-grey-7">File</div>
                <div class="text-body1">{{ favoriteDetail.filename }}</div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Total Groups</div>
                <div class="text-body1">{{ favoriteDetail.total_groups }}</div>
              </div>
              <div class="col-auto">
                <div class="text-caption text-grey-7">Total Frequencies</div>
                <div class="text-body1">{{ favoriteDetail.total_frequencies }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <div v-if="favoriteDetail" class="q-mt-md">
          <q-expansion-item
            v-for="group in favoriteDetail.groups"
            :key="group.id"
            :label="`${group.name} (${group.frequencies.length} frequencies)`"
            class="q-mb-md bg-white"
            icon="radio"
            header-class="bg-blue-1"
            default-opened
          >
            <q-card>
              <q-card-section class="q-pa-none">
                <q-table
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
const favoriteDetail = ref(null)
const loading = ref(false)

const frequencyColumns = [
  { name: 'name', label: 'Name', field: 'name', align: 'left', sortable: true },
  { name: 'frequency_mhz', label: 'Frequency', field: 'frequency_mhz', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true }
]

const goBack = () => {
  router.push('/?section=favorites')
}

const navigateToDatabase = () => {
  router.push('/?section=database')
}

const navigateToFavorites = () => {
  router.push('/?section=favorites')
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
