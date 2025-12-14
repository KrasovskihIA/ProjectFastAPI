<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import WeatherCurrent from './components/WeatherCurrent.vue'
import WeatherForecast from './components/WeatherForecast.vue'

const city = ref('Moscow') // Default city, maybe user wants English 'Moscow' based on backend default
const currentData = ref(null)
const forecastData = ref(null)
const error = ref(null)
const loading = ref(false)

// Use proxy path locally, but full URL if needed/deployed differently
const API_BASE = '/api' 
// Actually, backend is at 8000. In vite config I set proxy.
// If user runs without vite proxy (e.g. direct file open), this won't work.
// But we assume "node installed" -> so `npm run dev` -> proxy works.

const fetchWeather = async () => {
    loading.value = true
    error.value = null
    try {
        const [currentRes, forecastRes] = await Promise.all([
            axios.get(`${API_BASE}/weather`, { params: { city: city.value } }),
            axios.get(`${API_BASE}/five_days`, { params: { city: city.value } })
        ])
        currentData.value = currentRes.data
        forecastData.value = forecastRes.data
    } catch (err) {
        console.error(err)
        error.value = "Failed to fetch weather data. Please check the city name."
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchWeather()
})
</script>

<template>
  <div class="container">
    <header class="header">
      <h1>Weather Dashboard</h1>
      <div class="search-bar">
        <input v-model="city" @keyup.enter="fetchWeather" placeholder="Enter city name..." />
        <button @click="fetchWeather">Search</button>
      </div>
    </header>

    <div v-if="error" class="error-msg glass">
        {{ error }}
    </div>

    <div v-if="loading" class="loading glass">
        Loading data...
    </div>

    <main v-if="currentData && !loading" class="dashboard-grid">
      <!-- Current Weather -->
      <section class="current-weather glass">
        <WeatherCurrent :data="currentData" />
      </section>

      <!-- Forecast -->
      <section class="forecast glass">
        <WeatherForecast :data="forecastData" />
      </section>
    </main>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-bar {
    display: flex;
    gap: 0.5rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
}

@media (min-width: 768px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.glass {
    padding: 1.5rem;
}

.error-msg {
    color: #f87171;
    text-align: center;
}

.loading {
    text-align: center;
    font-size: 1.2rem;
}
</style>
