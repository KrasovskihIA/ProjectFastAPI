<script setup>
import { computed } from 'vue'

const props = defineProps({
    data: Object
})

const weatherIconUrl = computed(() => {
    // OpenWeatherMap icon URL
    if (props.data?.weather?.[0]?.icon) {
        return `https://openweathermap.org/img/wn/${props.data.weather[0].icon}@4x.png`
    }
    return ''
})
</script>

<template>
  <div class="weather-card">
    <div class="header-row">
        <h2>{{ data.name }}</h2>
        <span class="temp">{{ Math.round(data.main.temp) }}°C</span>
    </div>
    
    <div class="weather-main">
        <img :src="weatherIconUrl" :alt="data.weather[0].description" class="icon" />
        <p class="description">{{ data.weather[0].description }}</p>
    </div>

    <div class="details-grid">
        <div class="detail-item">
            <span class="label">Feels Like</span>
            <span class="value">{{ Math.round(data.main.feels_like) }}°C</span>
        </div>
         <div class="detail-item">
            <span class="label">Humidity</span>
            <span class="value">{{ data.main.humidity }}%</span>
        </div>
         <div class="detail-item">
            <span class="label">Wind</span>
            <span class="value">{{ data.wind.speed }} m/s</span>
        </div>
         <div class="detail-item">
            <span class="label">Pressure</span>
            <span class="value">{{ data.main.pressure }} hPa</span>
        </div>
    </div>
  </div>
</template>

<style scoped>
.weather-card {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.temp {
    font-size: 3rem;
    font-weight: 700;
}

.weather-main {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.icon {
    width: 100px;
    height: 100px;
}

.description {
    text-transform: capitalize;
    font-size: 1.2rem;
    color: var(--accent-color);
    margin-top: -10px;
}

.details-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

.detail-item {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    padding: 0.75rem;
    border-radius: 0.5rem;
}

.label {
    font-size: 0.8rem;
    color: #94a3b8; /* slate-400 */
}

.value {
    font-weight: 600;
    font-size: 1.1rem;
}
</style>
