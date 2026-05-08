import { defineStore } from 'pinia'
import { ref } from 'vue'
import { Dark } from 'quasar'
import { preferencesAPI } from '../api'

const DARK_MODE_VALUES = {
  system: 'system',
  on: 'on',
  off: 'off'
}

export const useUserPreferencesStore = defineStore('userPreferences', () => {
  const darkMode = ref(DARK_MODE_VALUES.system)
  const dialogOpen = ref(false)
  const loading = ref(false)
  const initialized = ref(false)

  let mediaQuery = null
  let mediaQueryListener = null

  const resolveDarkMode = (mode) => {
    if (mode === DARK_MODE_VALUES.on) {
      return true
    }

    if (mode === DARK_MODE_VALUES.off) {
      return false
    }

    if (typeof window === 'undefined' || !window.matchMedia) {
      return false
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  const applyDarkMode = (mode) => {
    Dark.set(resolveDarkMode(mode))
  }

  const syncWithSystem = () => {
    if (darkMode.value !== DARK_MODE_VALUES.system || !mediaQuery) {
      return
    }

    Dark.set(mediaQuery.matches)
  }

  const attachSystemListener = () => {
    if (typeof window === 'undefined' || !window.matchMedia || mediaQuery) {
      syncWithSystem()
      return
    }

    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQueryListener = () => syncWithSystem()

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', mediaQueryListener)
    } else if (mediaQuery.addListener) {
      mediaQuery.addListener(mediaQueryListener)
    }

    syncWithSystem()
  }

  const initialize = async () => {
    if (initialized.value) {
      attachSystemListener()
      applyDarkMode(darkMode.value)
      return
    }

    loading.value = true
    try {
      const { data } = await preferencesAPI.get()
      darkMode.value = data.dark_mode || DARK_MODE_VALUES.system
    } catch {
      darkMode.value = DARK_MODE_VALUES.system
    } finally {
      initialized.value = true
      applyDarkMode(darkMode.value)
      attachSystemListener()
      loading.value = false
    }
  }

  const setDarkMode = async (mode) => {
    const nextMode = DARK_MODE_VALUES[mode] || DARK_MODE_VALUES.system
    darkMode.value = nextMode
    applyDarkMode(nextMode)

    loading.value = true
    try {
      const { data } = await preferencesAPI.update({ dark_mode: nextMode })
      darkMode.value = data.dark_mode || nextMode
      applyDarkMode(darkMode.value)
      return data
    } finally {
      loading.value = false
    }
  }

  const openDialog = () => {
    dialogOpen.value = true
  }

  const closeDialog = () => {
    dialogOpen.value = false
  }

  return {
    darkMode,
    dialogOpen,
    loading,
    initialize,
    setDarkMode,
    openDialog,
    closeDialog,
  }
})