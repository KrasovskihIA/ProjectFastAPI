import os
from fastapi.responses import Response
import httpx


class WeatherApiClient:
    def __init__(self, city: str):
        self.city = city
        self.params = {
            "q": f"{city}",
            "units": "metric",
            "lang": "ru",
            "appid": os.getenv('API_KEY')
        }

    async def _get_coordinates(self) -> list:
        """Координаты по местоположению"""
        api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=5&appid={os.getenv('API_KEY')}"

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            data = response.json()
            coordinates = [data[0]['lat'], data[0]['lon']]
            return coordinates

    async def get_current_forecast(self) -> dict:
        """Получение текущий погоды"""
        api_url = f"https://api.openweathermap.org/data/2.5/weather"

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=self.params)
            return response.json()

    async def get_current_forecast_five_days(self) -> dict:
        """Получение прогноза на 5 дней"""
        api_url = f"https://api.openweathermap.org/data/2.5/forecast?"

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=self.params)
            return response.json()
