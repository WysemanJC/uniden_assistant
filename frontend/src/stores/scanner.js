import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { profileAPI, frequencyAPI, channelGroupAPI } from '../api'

export const useScannerStore = defineStore('scanner', () => {
  const profiles = ref([])
  const currentProfile = ref(null)
  const frequencies = ref([])
  const channelGroups = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchProfiles = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.list()
      profiles.value = data.results || data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchProfile = async (id) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.get(id)
      currentProfile.value = data
      frequencies.value = data.frequencies || []
      channelGroups.value = data.channel_groups || []
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createProfile = async (profileData) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.create(profileData)
      profiles.value.push(data)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (id, profileData) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.update(id, profileData)
      const index = profiles.value.findIndex(p => p.id === id)
      if (index > -1) {
        profiles.value[index] = data
      }
      if (currentProfile.value?.id === id) {
        currentProfile.value = data
      }
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProfile = async (id) => {
    loading.value = true
    error.value = null
    try {
      await profileAPI.delete(id)
      profiles.value = profiles.value.filter(p => p.id !== id)
      if (currentProfile.value?.id === id) {
        currentProfile.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const uploadFile = async (profileId, file) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.uploadFile(profileId, file)
      currentProfile.value = data
      frequencies.value = data.frequencies || []
      channelGroups.value = data.channel_groups || []
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const exportProfile = async (profileId) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await profileAPI.export(profileId)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    profiles,
    currentProfile,
    frequencies,
    channelGroups,
    loading,
    error,
    fetchProfiles,
    fetchProfile,
    createProfile,
    updateProfile,
    deleteProfile,
    uploadFile,
    exportProfile
  }
})
