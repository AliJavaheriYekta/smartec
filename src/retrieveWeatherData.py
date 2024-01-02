import requests
import json
import pandas as pd


def get_openweathermap_data(lat, lon, api_key, day):
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&cnt=24"

    current_date = f"2023-10-{day + 1}"
    current_url = base_url.format(lat=lat, lon=lon, api_key=api_key)

    response = requests.get(current_url)
    weather_data_json = json.loads(response.text)

    return current_date, weather_data_json


def get_sunrise_sunset_data(lat, lon, current_date):
    sun_set_rise_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={current_date}"
    response = requests.get(sun_set_rise_url)
    sun_state_response_json = json.loads(response.text)

    sunrise_time = sun_state_response_json["results"]["sunrise"]
    sunset_time = sun_state_response_json["results"]["sunset"]

    return sunrise_time, sunset_time


def main():
    # Replace with your latitude and longitude
    lat = "35.785675"
    lon = "51.5156200"

    # Replace with your API key from OpenWeatherMap
    api_key = "ed6f1d38af67b89850fd7d6e7f7bc9f7"

    weather_data = []

    # Collect weather data for the next 30 days
    for day in range(30):
        current_date, weather_data_json = get_openweathermap_data(lat, lon, api_key, day)
        sunrise_time, sunset_time = get_sunrise_sunset_data(lat, lon, current_date)

        # Extract weather data for each hour of the current day
        weather_data_hourly = []

        for hour in range(24):
            current_hour_data = weather_data_json["hourly"][hour]
            current_data = {
                "date": current_date,
                "hour": hour,
                "temp": current_hour_data["temp"],
                "humidity": current_hour_data["humidity"],
                "pressure": current_hour_data["pressure"],
                "sunset": sunset_time,
                "sunrise": sunrise_time
            }
            weather_data_hourly.append(current_data)

        # Append hourly weather data for the current day to the overall data list
        weather_data.extend(weather_data_hourly)

    # Convert the weather data list into a DataFrame
    df = pd.DataFrame(weather_data)

    # Save the DataFrame to a CSV file
    df.to_csv("./complete_weather_data.csv")


if __name__ == "__main__":
    main()
