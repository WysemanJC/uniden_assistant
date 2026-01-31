import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/uniden_manager'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const profileAPI = {
  list() {
    return api.get('/usersettings/profiles/')
  },
  get(id) {
    return api.get(`/usersettings/profiles/${id}/`)
  },
  create(data) {
    return api.post('/usersettings/profiles/', data)
  },
  update(id, data) {
    return api.put(`/usersettings/profiles/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/usersettings/profiles/${id}/`)
  },
  uploadFile(id, file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/usersettings/profiles/${id}/upload_file/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  export(id) {
    return api.get(`/usersettings/profiles/${id}/export/`)
  }
}

export const frequencyAPI = {
  list(profileId = null) {
    const params = profileId ? { profile: profileId } : {}
    return api.get('/usersettings/frequencies/', { params })
  },
  get(id) {
    return api.get(`/usersettings/frequencies/${id}/`)
  },
  create(data) {
    return api.post('/usersettings/frequencies/', data)
  },
  update(id, data) {
    return api.put(`/usersettings/frequencies/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/usersettings/frequencies/${id}/`)
  }
}

export const sdAPI = {
  exportToSd() {
    return api.post('/usersettings/sd/export/')
  }
}

export const channelGroupAPI = {
  list(profileId = null) {
    const params = profileId ? { profile: profileId } : {}
    return api.get('/usersettings/channel-groups/', { params })
  },
  get(id) {
    return api.get(`/usersettings/channel-groups/${id}/`)
  },
  create(data) {
    return api.post('/usersettings/channel-groups/', data)
  },
  update(id, data) {
    return api.put(`/usersettings/channel-groups/${id}/`)
  },
  delete(id) {
    return api.delete(`/usersettings/channel-groups/${id}/`)
  }
}

export const agencyAPI = {
  list() {
    return api.get('/usersettings/agencies/')
  }
}

export default api
