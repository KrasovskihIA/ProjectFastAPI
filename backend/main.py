import os
from typing import Annotated
from fastapi import FastAPI, Query, Path, HTTPException
import httpx
from dotenv import load_dotenv
from fastapi.openapi.models import Response
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from backend.schemas import WeatherForecast, WeatherForecastList
from backend.services import WeatherApiClient

app = FastAPI(debug=True)
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Получить текущую погоду
@app.get("/weather", response_model=WeatherForecast, status_code=status.HTTP_201_CREATED,
         summary="Текущие данные о погоде")
async def get_weather(city: Annotated[str, Query(max_length=20)] = 'Москва') -> WeatherForecast:
    weather_json = await WeatherApiClient(city).get_current_forecast()

    result_weather_forecast = WeatherForecast(name=weather_json["name"], weather=weather_json["weather"],
                                              main=weather_json["main"], wind=weather_json["wind"],
                                              clouds=weather_json["clouds"])
    return result_weather_forecast


# Прогноз на 5 дней
@app.get("/five_days", response_model=WeatherForecastList, status_code=status.HTTP_201_CREATED,
         summary="Прогноз на 5 дней")
async def get_weather_five_days(city: Annotated[str, Query(max_length=20)] = 'Москва') -> WeatherForecastList:
    weather_json = await WeatherApiClient(city).get_current_forecast_five_days()

    result_weather_forecast = WeatherForecastList(list_weather_forecast=weather_json["list"])

    return result_weather_forecast
