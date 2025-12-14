from typing import Dict, List, Optional

from pydantic import BaseModel


class WeatherItem(BaseModel):
    id: Optional[int] = None
    main: str
    description: str
    icon: str


class WeatherItemList(BaseModel):
    dt_txt: str
    weather: List[WeatherItem]
    main: Dict[str, float]
    wind: Dict[str, float]
    clouds: Dict[str, float]


class WeatherForecast(BaseModel):
    """Результат прогноза погоды"""
    name: str
    weather: List[WeatherItem]
    main: Dict[str, float]
    wind: Dict[str, float]
    clouds: Dict[str, float]


class WeatherForecastList(BaseModel):
    """Результат прогноза на 5 дней"""
    list_weather_forecast: List[WeatherItemList]
