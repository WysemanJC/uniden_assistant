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
  const hasLatLon = !isNaN(lat) && !isNaN(lon)

  const rectangles = Array.isArray(props.channelGroup.rectangles)
    ? props.channelGroup.rectangles
    : []

  // Create map (default view will be updated once shapes are added)
  map = L.map(mapContainer.value).setView([0, 0], 2)

  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  const featureGroup = L.featureGroup().addTo(map)

  // Add rectangle bounds if provided
  if (rectangles.length > 0) {
    rectangles.forEach((rect) => {
      const minLat = parseFloat(rect.min_latitude ?? Math.min(rect.latitude_1, rect.latitude_2))
      const maxLat = parseFloat(rect.max_latitude ?? Math.max(rect.latitude_1, rect.latitude_2))
      const minLon = parseFloat(rect.min_longitude ?? Math.min(rect.longitude_1, rect.longitude_2))
      const maxLon = parseFloat(rect.max_longitude ?? Math.max(rect.longitude_1, rect.longitude_2))

      if ([minLat, maxLat, minLon, maxLon].some((v) => isNaN(v))) {
        return
      }

      const bounds = [
        [minLat, minLon],
        [maxLat, maxLon]
      ]

      L.rectangle(bounds, {
        color: '#26a69a',
        weight: 2,
        opacity: 0.7,
        fill: true,
        fillOpacity: 0.08
      }).addTo(featureGroup)
    })
  }

  // Add marker at the location (if available)
  if (hasLatLon) {
    L.circleMarker([lat, lon], {
      radius: 8,
      fillColor: '#3f51b5',
      color: '#000',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    })
      .addTo(featureGroup)
      .bindPopup(`<strong>${props.channelGroup.name_tag}</strong><br/>
        Lat: ${lat.toFixed(6)}<br/>
        Lon: ${lon.toFixed(6)}`)

    // Add range circle if range_miles is provided
    if (props.channelGroup.range_miles) {
      const radiusMiles = parseFloat(props.channelGroup.range_miles)
      if (!isNaN(radiusMiles)) {
        const radiusMeters = radiusMiles * 1609.34
        L.circle([lat, lon], {
          radius: radiusMeters,
          color: '#ff7043',
          weight: 2,
          opacity: 0.6,
          fill: true,
          fillColor: '#ff7043',
          fillOpacity: 0.1
        }).addTo(featureGroup)
      }
    }
  }

  // Fit map to bounds if we added any shapes
  if (featureGroup.getLayers().length > 0) {
    map.fitBounds(featureGroup.getBounds(), { padding: [50, 50] })
  } else if (hasLatLon) {
    map.setView([lat, lon], 10)
  } else {
    console.warn('No valid geometry to display for this channel group')
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
