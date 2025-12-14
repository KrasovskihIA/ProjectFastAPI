<script setup>
import { computed } from 'vue'

const props = defineProps({
    data: Object
})

const forecastList = computed(() => {
    // The API might return 3-hour intervals (40 items for 5 days).
    // Let's filter to show one per day (e.g. at 12:00) or just show next 5 items if desired.
    // The prompt says "Forecast for 5 days". Usually users want 12:00 forecast for each day.
    if (!props.data?.list_weather_forecast) return []
    
    // Simple filter: return items where dt_txt contains "12:00:00"
    // Or if not enough data, just take every 8th item (24h / 3h = 8)
    const filtered = props.data.list_weather_forecast.filter(item => item.dt_txt.includes("12:00:00"))
    
    // If empty (e.g. data loaded at night and 12:00 passed), fallback to first 5 items
    if (filtered.length === 0) {
        return props.data.list_weather_forecast.slice(0, 5)
    }
    return filtered
})

const getIconUrl = (icon) => `https://openweathermap.org/img/wn/${icon}.png`

const formatDate = (dt_txt) => {
    const date = new Date(dt_txt)
    return date.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric' })
}
</script>

<template>
  <div class="forecast-container">
    <h2>5-Day Forecast</h2>
    <div class="forecast-list">
        <div v-for="item in forecastList" :key="item.dt_txt" class="forecast-item glass">
            <span class="date">{{ formatDate(item.dt_txt) }}</span>
            <img :src="getIconUrl(item.weather[0].icon)" :alt="item.weather[0].description" />
            <span class="temp">{{ Math.round(item.main.temp) }}°C</span>
            <span class="desc">{{ item.weather[0].main }}</span>
        </div>
    </div>
  </div>
</template>

<style scoped>
.forecast-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.forecast-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 1rem;
}

.forecast-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 0.5rem;
    text-align: center;
}

.glass {
    /* reuse glass slightly adjusted for smaller cards if needed */
    border: 1px solid var(--glass-border);
}

.date {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.temp {
    font-weight: 700;
    margin-top: 0.25rem;
}

.desc {
    font-size: 0.8rem;
    color: #94a3b8;
}
</style>
