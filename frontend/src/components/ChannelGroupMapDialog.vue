<template>
  <q-dialog v-model="showDialog" maximized>
    <q-card class="full-width">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ channelGroup?.name_tag }}</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="showDialog = false" />
      </q-card-section>

      <q-card-section class="q-pa-none" style="height: calc(100vh - 80px);">
        <div ref="mapContainer" style="width: 100%; height: 100%;"></div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  modelValue: Boolean,
  channelGroup: Object
})

const emit = defineEmits(['update:modelValue'])

const showDialog = ref(props.modelValue)
const mapContainer = ref(null)
let map = null

watch(() => props.modelValue, (newVal) => {
  showDialog.value = newVal
})

watch(() => showDialog.value, (newVal) => {
  emit('update:modelValue', newVal)
})

const initializeMap = () => {
  if (!mapContainer.value || !props.channelGroup) return
  
  // Remove old map if exists
  if (map) {
    map.remove()
    map = null
  }

  const lat = parseFloat(props.channelGroup.latitude)
  const lon = parseFloat(props.channelGroup.longitude)

  if (isNaN(lat) || isNaN(lon)) {
    console.error('Invalid latitude or longitude')
    return
  }

  // Create map centered on the location
  map = L.map(mapContainer.value).setView([lat, lon], 10)

  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  // Add marker at the location
  L.circleMarker([lat, lon], {
    radius: 8,
    fillColor: '#3f51b5',
    color: '#000',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.8
  })
    .addTo(map)
    .bindPopup(`<strong>${props.channelGroup.name_tag}</strong><br/>
      Lat: ${lat.toFixed(6)}<br/>
      Lon: ${lon.toFixed(6)}`)

  // Add range circle if range_miles is provided
  if (props.channelGroup.range_miles) {
    const radiusMeters = parseFloat(props.channelGroup.range_miles) * 1609.34 // Convert miles to meters
    L.circle([lat, lon], {
      radius: radiusMeters,
      color: '#ff7043',
      weight: 2,
      opacity: 0.6,
      fill: true,
      fillColor: '#ff7043',
      fillOpacity: 0.1
    }).addTo(map)
  }

  // Fit map to bounds if circle exists
  if (map && props.channelGroup.range_miles) {
    const radiusMeters = parseFloat(props.channelGroup.range_miles) * 1609.34
    const bounds = new L.LatLngBounds(
      [lat - radiusMeters / 111000, lon - radiusMeters / (111000 * Math.cos(lat * Math.PI / 180))],
      [lat + radiusMeters / 111000, lon + radiusMeters / (111000 * Math.cos(lat * Math.PI / 180))]
    )
    map.fitBounds(bounds, { padding: [50, 50] })
  }
}

watch(
  () => props.channelGroup,
  () => {
    if (showDialog.value) {
      setTimeout(initializeMap, 100)
    }
  }
)

watch(
  () => showDialog.value,
  (newVal) => {
    if (newVal) {
      setTimeout(initializeMap, 100)
    }
  }
)

onMounted(() => {
  if (showDialog.value && props.channelGroup) {
    setTimeout(initializeMap, 100)
  }
})
</script>

<style scoped>
:deep(.leaflet-container) {
  z-index: 0;
}

:deep(.leaflet-control) {
  z-index: 1;
}
</style>
