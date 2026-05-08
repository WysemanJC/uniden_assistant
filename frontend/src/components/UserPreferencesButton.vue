<template>
  <q-btn
    flat
    round
    dense
    icon="person"
    aria-label="User preferences"
    @click="preferences.openDialog()"
  >
    <q-tooltip>User preferences</q-tooltip>
  </q-btn>

  <q-dialog v-model="preferences.dialogOpen">
    <q-card style="min-width: 360px; max-width: 92vw;">
      <q-card-section class="row items-center">
        <div class="text-h6">User Preferences</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="preferences.closeDialog()" />
      </q-card-section>

      <q-card-section class="q-gutter-md">
        <div>
          <div class="text-subtitle2 q-mb-sm">Dark Mode</div>
          <q-btn-toggle
            :model-value="preferences.darkMode"
            :options="darkModeOptions"
            no-caps
            spread
            unelevated
            toggle-color="primary"
            :disable="preferences.loading"
            @update:model-value="handleDarkModeChange"
          />
        </div>
        <div class="text-caption text-grey-7">
          System Default follows your operating system theme.
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat color="primary" label="Close" @click="preferences.closeDialog()" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { useUserPreferencesStore } from '../stores/userPreferences'

const preferences = useUserPreferencesStore()

const darkModeOptions = [
  { label: 'System Default', value: 'system' },
  { label: 'On', value: 'on' },
  { label: 'Off', value: 'off' },
]

const handleDarkModeChange = async (value) => {
  if (value === preferences.darkMode) {
    return
  }

  await preferences.setDarkMode(value)
}
</script>