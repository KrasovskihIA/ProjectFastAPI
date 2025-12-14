<script setup>
import { onMounted, ref } from 'vue'
import L from 'leaflet'

const mapContainer = ref(null)

onMounted(() => {
    if (!mapContainer.value) return

    const map = L.map(mapContainer.value).setView([55.75, 37.61], 3) // Default center (Moscow roughly)

    // Base Layer (Standard OSM)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Precipitation Layer from OpenWeatherMap
    // URL: https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid={API_KEY}
    // We expect the API_KEY to be available via environment variables.
    // Configure Vite to load this from the root .env file and expose vars starting with API_.
    const API_KEY = import.meta.env.API_KEY; 
    
    if (!API_KEY || API_KEY.includes('YOUR_OPENWEATHERMAP_API_KEY')) {
         console.warn("API_KEY is missing or invalid.");
    }

    const precipitationLayer = L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${API_KEY}`, {
        opacity: 0.7,
        attribution: '&copy; OpenWeatherMap'
    });

    precipitationLayer.addTo(map);
})
</script>

<template>
  <div class="map-wrapper">
    <div ref="mapContainer" class="map-view"></div>
    <div class="note">
        <small>Note: Map precipitation layer requires a valid API key in source code.</small>
    </div>
  </div>
</template>

<style scoped>
.map-wrapper {
    width: 100%;
    height: 400px;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    border-radius: 1rem;
    overflow: hidden;
}

.map-view {
    width: 100%;
    height: 100%;
}

.note {
    text-align: center;
    color: #fca5a5;
}
</style>
