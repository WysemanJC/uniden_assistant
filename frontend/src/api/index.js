import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

const api = axios.create({
  baseURL: API_BASE_URL + '/uniden_manager',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const profileAPI = {
  list() {
    return api.get('/favourites/profiles/')
  },
  get(id) {
    return api.get(`/favourites/profiles/${id}/`)
  },
  create(data) {
    return api.post('/favourites/profiles/', data)
  },
  update(id, data) {
    return api.put(`/favourites/profiles/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/favourites/profiles/${id}/`)
  },
  uploadFile(id, file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/favourites/profiles/${id}/upload_file/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  export(id) {
    return api.get(`/favourites/profiles/${id}/export/`)
  }
}

export const frequencyAPI = {
  list(profileId = null) {
    const params = profileId ? { profile: profileId } : {}
    return api.get('/favourites/frequencies/', { params })
  },
  get(id) {
    return api.get(`/favourites/frequencies/${id}/`)
  },
  create(data) {
    return api.post('/favourites/frequencies/', data)
  },
  update(id, data) {
    return api.put(`/favourites/frequencies/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/favourites/frequencies/${id}/`)
  }
}

export const sdAPI = {
  exportToSd() {
    return api.post('/favourites/sd/export/')
  }
}

export const channelGroupAPI = {
  list(profileId = null) {
    const params = profileId ? { profile: profileId } : {}
    return api.get('/favourites/channel-groups/', { params })
  },
  get(id) {
    return api.get(`/favourites/channel-groups/${id}/`)
  },
  create(data) {
    return api.post('/favourites/channel-groups/', data)
  },
  update(id, data) {
    return api.put(`/favourites/channel-groups/${id}/`)
  },
  delete(id) {
    return api.delete(`/favourites/channel-groups/${id}/`)
  }
}

export const agencyAPI = {
  list() {
    return api.get('/favourites/agencies/')
  }
}

export default api
