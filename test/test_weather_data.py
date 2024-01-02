import unittest
from datetime import datetime
from src.weatherData import WeatherData, DailyWeatherData, HourlyWeatherData, average_temperature, highest_pressure


class TestWeatherData(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.weather_data = WeatherData(
            date=datetime.now(),
            temperature=25.0,
            humidity=60,
            pressure=1010
        )

        self.daily_weather_data = DailyWeatherData(
            date=datetime.now(),
            temperature=25.0,
            humidity=60,
            pressure=1010,
            sunrise="06:00 AM",
            sunset="06:00 PM"
        )

        self.hourly_weather_data = HourlyWeatherData(
            date=datetime.now(),
            temperature=25.0,
            humidity=60,
            pressure=1010,
            time="12:00 PM"
        )

    def test_getters(self):
        self.assertEqual(self.weather_data.get_temperature(), 25.0)
        self.assertEqual(self.daily_weather_data.get_sunrise(), "06:00 AM")
        self.assertEqual(self.hourly_weather_data.get_time(), "12:00 PM")

    def test_average_temperature(self):
        daily_data_list = [self.daily_weather_data] * 5
        avg_temp = average_temperature(daily_data_list)
        expected_avg_temp = 25.0
        self.assertEqual(avg_temp, expected_avg_temp)

    def test_highest_pressure(self):
        hourly_data_list = [
            HourlyWeatherData(datetime.now(), 25.0, 60, 1015, "12:00 PM"),
            HourlyWeatherData(datetime.now(), 25.0, 60, 1020, "01:00 PM"),
            HourlyWeatherData(datetime.now(), 25.0, 60, 1012, "02:00 PM")
        ]
        highest_pressure_inst = highest_pressure(hourly_data_list)
        expected_highest_pressure = hourly_data_list[1]
        self.assertEqual(highest_pressure_inst, expected_highest_pressure)


if __name__ == '__main__':
    unittest.main()
