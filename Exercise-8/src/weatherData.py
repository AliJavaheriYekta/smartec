import math
from typing import List, Optional


class WeatherData:
    def __init__(self, date, temperature, humidity, pressure):
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def get_date(self):
        return self.date

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure


class DailyWeatherData(WeatherData):
    def __init__(self, date, temperature, humidity, pressure, sunrise, sunset):
        super().__init__(date, temperature, humidity, pressure)
        self.sunrise = sunrise
        self.sunset = sunset

    def get_sunrise(self):
        return self.sunrise

    def get_sunset(self):
        return self.sunset


class HourlyWeatherData(WeatherData):
    def __init__(self, date, temperature, humidity, pressure, time):
        super().__init__(date, temperature, humidity, pressure)
        self.time = time

    def get_time(self):
        return self.time


def average_temperature(daily_weather_data_list: List[WeatherData]) -> float:
    total_temperature = sum(data.get_temperature() for data in daily_weather_data_list)
    avg_temperature = total_temperature / len(daily_weather_data_list)
    return avg_temperature


def highest_pressure(hourly_weather_data_list: List[HourlyWeatherData]) -> Optional[HourlyWeatherData]:
    highest_pressure_inst: Optional[HourlyWeatherData] = None
    highest_pressure_value = 0

    for hourly_weather_data in hourly_weather_data_list:
        current_pressure = hourly_weather_data.get_pressure()
        if current_pressure > highest_pressure_value:
            highest_pressure_value = current_pressure
            highest_pressure_inst = hourly_weather_data
    return highest_pressure_inst
