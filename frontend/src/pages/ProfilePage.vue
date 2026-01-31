<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          @click="router.back()"
          class="q-mr-md text-white"
        />
        <q-toolbar-title>{{ scanner.currentProfile?.name || 'Profile' }}</q-toolbar-title>
        <q-space />
        <q-btn
          color="white"
          label="Upload File"
          icon="upload"
          @click="uploadFile"
          class="q-mr-md"
        />
        <q-btn
          color="positive"
          label="Export"
          icon="download"
          @click="exportFile"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-md">
        <q-tabs
          v-model="activeTab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="left"
        >
          <q-tab name="frequencies" label="Frequencies" />
          <q-tab name="groups" label="Channel Groups" />
        </q-tabs>

        <q-tab-panels v-model="activeTab" animated class="q-mt-md">
          <q-tab-panel name="frequencies">
            <FrequencyTable :profile-id="profileId" />
          </q-tab-panel>

          <q-tab-panel name="groups">
            <ChannelGroupsPanel :profile-id="profileId" />
          </q-tab-panel>
        </q-tab-panels>

        <input
          ref="fileInput"
          type="file"
          style="display: none"
          @change="handleFileUpload"
          accept=".hpd,.cfg"
        />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScannerStore } from '../stores/scanner'
import { useQuasar } from 'quasar'
import FrequencyTable from '../components/FrequencyTable.vue'
import ChannelGroupsPanel from '../components/ChannelGroupsPanel.vue'

const route = useRoute()
const router = useRouter()
const scanner = useScannerStore()
const $q = useQuasar()

const profileId = ref(parseInt(route.params.id, 10))
const activeTab = ref('frequencies')
const fileInput = ref(null)

onMounted(() => {
  scanner.fetchProfile(profileId.value)
})

const uploadFile = () => {
  fileInput.value?.click()
}

const handleFileUpload = async (event) => {
  const file = event.target.files?.[0]
  if (file) {
    try {
      await scanner.uploadFile(profileId.value, file)
      $q.notify({
        type: 'positive',
        message: 'File uploaded successfully'
      })
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Error uploading file: ' + error.message
      })
    }
  }
}

const exportFile = async () => {
  try {
    const data = await scanner.exportProfile(profileId.value)
    const element = document.createElement('a')
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data.content))
    element.setAttribute('download', `${scanner.currentProfile?.name}.hpd`)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
    $q.notify({
      type: 'positive',
      message: 'File exported successfully'
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error exporting file: ' + error.message
    })
  }
}
</script>
