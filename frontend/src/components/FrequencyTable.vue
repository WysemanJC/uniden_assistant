<template>
  <div>
    <div class="row q-mb-md">
      <q-input
        v-model="searchText"
        placeholder="Search frequencies..."
        outlined
        dense
        class="flex col"
        @update:model-value="filterFrequencies"
      >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
      <q-btn
        color="primary"
        label="Add Frequency"
        icon="add"
        @click="showAddDialog = true"
        class="q-ml-md"
      />
    </div>

    <q-table
      :rows="filteredFrequencies"
      :columns="columns"
      row-key="id"
      :loading="loading"
      paginated
      :rows-per-page="25"
    >
      <template #body-cell-frequency="props">
        <q-td :props="props">
          {{ (props.row.frequency / 1000000).toFixed(4) }} MHz
        </q-td>
      </template>

      <template #body-cell-enabled="props">
        <q-td :props="props">
          <q-toggle
            :model-value="props.row.enabled"
            @update:model-value="updateFrequency(props.row.id, { enabled: $event })"
          />
        </q-td>
      </template>

      <template #body-cell-actions="props">
        <q-td :props="props">
          <q-btn
            flat
            dense
            round
            icon="edit"
            size="sm"
            @click="editFrequency(props.row)"
          />
          <q-btn
            flat
            dense
            round
            icon="delete"
            size="sm"
            color="negative"
            @click="deleteFrequency(props.row.id)"
          />
        </q-td>
      </template>
    </q-table>

    <FrequencyDialog
      v-model="showAddDialog"
      :frequency="editingFrequency"
      :profile-id="profileId"
      @save="saveFrequency"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { frequencyAPI } from '../api'
import FrequencyDialog from './FrequencyDialog.vue'
import { useQuasar } from 'quasar'

const props = defineProps({
  profileId: {
    type: Number,
    required: true
  }
})

const $q = useQuasar()

const columns = [
  { name: 'name_tag', label: 'Name', field: 'name_tag', align: 'left' },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left' },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left' },
  { name: 'audio_option', label: 'Audio Option', field: 'audio_option', align: 'left' },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const frequencies = ref([])
const filteredFrequencies = ref([])
const loading = ref(false)
const searchText = ref('')
const showAddDialog = ref(false)
const editingFrequency = ref(null)

const filterFrequencies = () => {
  if (!searchText.value) {
    filteredFrequencies.value = frequencies.value
  } else {
    const search = searchText.value.toLowerCase()
    filteredFrequencies.value = frequencies.value.filter(f =>
      f.name_tag.toLowerCase().includes(search) ||
      (f.audio_option && f.audio_option.toLowerCase().includes(search))
    )
  }
}

const fetchFrequencies = async () => {
  loading.value = true
  try {
    const { data } = await frequencyAPI.list(props.profileId)
    frequencies.value = Array.isArray(data) ? data : data.results || []
    filterFrequencies()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error loading frequencies: ' + error.message
    })
  } finally {
    loading.value = false
  }
}

const saveFrequency = async (frequencyData) => {
  loading.value = true
  try {
    frequencyData.profile = props.profileId
    if (editingFrequency.value?.id) {
      await frequencyAPI.update(editingFrequency.value.id, frequencyData)
    } else {
      await frequencyAPI.create(frequencyData)
    }
    await fetchFrequencies()
    showAddDialog.value = false
    editingFrequency.value = null
    $q.notify({
      type: 'positive',
      message: 'Frequency saved successfully'
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error saving frequency: ' + error.message
    })
  } finally {
    loading.value = false
  }
}

const editFrequency = (frequency) => {
  editingFrequency.value = { ...frequency }
  showAddDialog.value = true
}

const deleteFrequency = async (id) => {
  if (confirm('Are you sure you want to delete this frequency?')) {
    try {
      await frequencyAPI.delete(id)
      await fetchFrequencies()
      $q.notify({
        type: 'positive',
        message: 'Frequency deleted successfully'
      })
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Error deleting frequency: ' + error.message
      })
    }
  }
}

const updateFrequency = async (id, data) => {
  try {
    await frequencyAPI.update(id, data)
    await fetchFrequencies()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error updating frequency: ' + error.message
    })
  }
}

onMounted(() => {
  fetchFrequencies()
})
</script>
