<template>
  <q-dialog v-model="isOpen" @update:model-value="closeDialog">
    <q-card style="min-width: 500px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ group?.id ? 'Edit' : 'New' }} Channel Group</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="isOpen = false" />
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="formData.name"
          label="Group Name"
          outlined
          dense
          class="q-mb-md"
        />

        <q-input
          v-model="formData.description"
          label="Description"
          outlined
          dense
          type="textarea"
          class="q-mb-md"
        />

        <q-checkbox
          v-model="formData.enabled"
          label="Enabled"
          class="q-mb-md"
        />

        <div class="q-mb-md">
          <div class="text-subtitle2 q-mb-sm">Frequencies in this group:</div>
          <q-select
            v-model="formData.frequency_ids"
            :options="availableFrequencies"
            option-value="id"
            option-label="name"
            outlined
            dense
            multiple
            @update:model-value="updateFrequencyIds"
          />
        </div>

        <div v-if="formData.frequency_ids.length">
          <div class="text-subtitle2 q-mb-sm">Selected:</div>
          <div class="row q-gutter-xs">
            <q-chip
              v-for="freqId in formData.frequency_ids"
              :key="freqId"
              removable
              @remove="removeFrequency(freqId)"
            >
              {{ getFrequencyName(freqId) }}
            </q-chip>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" @click="isOpen = false" />
        <q-btn
          flat
          label="Save"
          color="primary"
          @click="save"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  group: Object,
  profileId: Number,
  availableFrequencies: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const isOpen = ref(false)
const formData = ref({
  name: '',
  description: '',
  enabled: true,
  frequency_ids: []
})

watch(() => props.modelValue, (newVal) => {
  isOpen.value = newVal
  if (newVal) {
    if (props.group) {
      formData.value = {
        name: props.group.name || '',
        description: props.group.description || '',
        enabled: props.group.enabled !== false,
        frequency_ids: props.group.frequencies?.map(f => f.id) || []
      }
    } else {
      formData.value = {
        name: '',
        description: '',
        enabled: true,
        frequency_ids: []
      }
    }
  }
})

const getFrequencyName = (freqId) => {
  const freq = props.availableFrequencies.find(f => f.id === freqId)
  return freq ? freq.name : 'Unknown'
}

const updateFrequencyIds = (selected) => {
  formData.value.frequency_ids = selected.map(f => f.id)
}

const removeFrequency = (freqId) => {
  formData.value.frequency_ids = formData.value.frequency_ids.filter(id => id !== freqId)
}

const closeDialog = (value) => {
  emit('update:modelValue', value)
}

const save = () => {
  if (!formData.value.name) {
    alert('Please enter a group name')
    return
  }
  emit('save', formData.value)
  isOpen.value = false
}
</script>
