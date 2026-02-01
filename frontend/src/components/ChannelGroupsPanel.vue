<template>
  <div>
    <div class="row q-mb-md">
      <q-input
        v-model="searchText"
        placeholder="Search channel groups..."
        outlined
        dense
        class="flex col"
      >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
      <q-btn
        color="primary"
        label="New Group"
        icon="add"
        @click="showAddGroupDialog = true"
        class="q-ml-md"
      />
    </div>

    <div class="row q-col-gutter-md">
      <div
        v-for="group in filteredGroups"
        :key="group.id"
        class="col-12 col-md-6 col-lg-4"
      >
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ group.name_tag }}</div>
            <div class="text-caption text-grey">
              {{ group.frequencies?.length || 0 }} frequencies
            </div>
            <div class="text-body2 q-mt-md">{{ group.description }}</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div class="row q-gutter-xs">
              <q-chip
                v-for="freq in group.frequencies"
                :key="freq.id"
                removable
                @remove="removeFrequencyFromGroup(group.id, freq.id)"
                size="sm"
              >
                {{ freq.name_tag }}
              </q-chip>
            </div>
          </q-card-section>

          <q-card-actions>
            <q-btn
              flat
              size="sm"
              icon="edit"
              @click="editGroup(group)"
            />
            <q-space />
            <q-btn
              flat
              size="sm"
              icon="delete"
              color="negative"
              @click="deleteGroup(group.id)"
            />
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <ChannelGroupDialog
      v-model="showAddGroupDialog"
      :group="editingGroup"
      :profile-id="profileId"
      :available-frequencies="frequencies"
      @save="saveGroup"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { channelGroupAPI, frequencyAPI } from '../api'
import ChannelGroupDialog from './ChannelGroupDialog.vue'
import { useQuasar } from 'quasar'

const props = defineProps({
  profileId: {
    type: Number,
    required: true
  }
})

const $q = useQuasar()

const groups = ref([])
const frequencies = ref([])
const searchText = ref('')
const showAddGroupDialog = ref(false)
const editingGroup = ref(null)

const filteredGroups = computed(() => {
  if (!searchText.value) return groups.value
  return groups.value.filter(g =>
    g.name_tag.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const fetchGroups = async () => {
  try {
    const { data } = await channelGroupAPI.list(props.profileId)
    groups.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error loading groups: ' + error.message
    })
  }
}

const fetchFrequencies = async () => {
  try {
    const { data } = await frequencyAPI.list(props.profileId)
    frequencies.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Error loading frequencies:', error)
  }
}

const saveGroup = async (groupData) => {
  try {
    groupData.profile = props.profileId
    if (editingGroup.value?.id) {
      await channelGroupAPI.update(editingGroup.value.id, groupData)
    } else {
      await channelGroupAPI.create(groupData)
    }
    await fetchGroups()
    showAddGroupDialog.value = false
    editingGroup.value = null
    $q.notify({
      type: 'positive',
      message: 'Channel group saved successfully'
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error saving group: ' + error.message
    })
  }
}

const editGroup = (group) => {
  editingGroup.value = { ...group }
  showAddGroupDialog.value = true
}

const deleteGroup = async (id) => {
  if (confirm('Are you sure?')) {
    try {
      await channelGroupAPI.delete(id)
      await fetchGroups()
      $q.notify({
        type: 'positive',
        message: 'Channel group deleted'
      })
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Error deleting group: ' + error.message
      })
    }
  }
}

const removeFrequencyFromGroup = async (groupId, frequencyId) => {
  try {
    const group = groups.value.find(g => g.id === groupId)
    if (group) {
      group.frequency_ids = group.frequencies.map(f => f.id).filter(id => id !== frequencyId)
      await channelGroupAPI.update(groupId, group)
      await fetchGroups()
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error updating group: ' + error.message
    })
  }
}

onMounted(() => {
  fetchGroups()
  fetchFrequencies()
})
</script>
