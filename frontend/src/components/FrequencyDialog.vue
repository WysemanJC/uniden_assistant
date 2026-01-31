<template>
  <q-dialog v-model="isOpen" @update:model-value="closeDialog">
    <q-card style="min-width: 500px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ frequency?.id ? 'Edit' : 'Add' }} Frequency</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="isOpen = false" />
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="formData.name"
          label="Frequency Name"
          outlined
          dense
          class="q-mb-md"
        />

        <q-input
          v-model.number="formData.frequency"
          label="Frequency (Hz)"
          outlined
          dense
          type="number"
          class="q-mb-md"
          hint="Enter frequency in Hertz (e.g., 161000000 for 161 MHz)"
        />

        <q-select
          v-model="formData.modulation"
          :options="['FM', 'AM', 'AUTO']"
          label="Modulation"
          outlined
          dense
          class="q-mb-md"
        />

        <q-input
          v-model="formData.nac"
          label="NAC Code"
          outlined
          dense
          class="q-mb-md"
          placeholder="e.g., 40B"
        />

        <q-checkbox
          v-model="formData.enabled"
          label="Enabled"
          class="q-mb-md"
        />

        <q-input
          v-model.number="formData.priority"
          label="Priority"
          outlined
          dense
          type="number"
          class="q-mb-md"
        />
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
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  frequency: Object,
  profileId: Number
})

const emit = defineEmits(['update:modelValue', 'save'])

const isOpen = ref(false)
const formData = ref({
  name: '',
  frequency: 0,
  modulation: 'FM',
  nac: '',
  enabled: true,
  priority: 0
})

watch(() => props.modelValue, (newVal) => {
  isOpen.value = newVal
  if (newVal) {
    if (props.frequency) {
      formData.value = { ...props.frequency }
    } else {
      formData.value = {
        name: '',
        frequency: 0,
        modulation: 'FM',
        nac: '',
        enabled: true,
        priority: 0
      }
    }
  }
})

const closeDialog = (value) => {
  emit('update:modelValue', value)
}

const save = () => {
  if (!formData.value.name || !formData.value.frequency) {
    alert('Please fill in name and frequency')
    return
  }
  emit('save', formData.value)
  isOpen.value = false
}
</script>
