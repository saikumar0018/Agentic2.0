import requests
from langchain.tools import tool

class WeatherForecast: 

    @classmethod
    def get_coordinates(cls, city: str):
        """
        Get latitude, longitude, state, and country for a given city using Nominatim.
        """
        url = f"https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q={city}"
        headers = {"User-Agent": "weather-langchain-agent"}  # required
        response = requests.get(url, headers=headers)

        if response.status_code != 200 or not response.json():
            return None

        data = response.json()[0]
        lat = float(data["lat"])
        lon = float(data["lon"])
        address = data.get("address", {})
        state = address.get("state", "Unknown state")
        country = address.get("country", "Unknown country")

        return {
            "latitude": lat,
            "longitude": lon,
            "state": state,
            "country": country
        }

    @classmethod
    def get_weather(cls, city: str) -> str:
        """
        Get current weather and 3-day forecast using Open-Meteo for a given city.
        """
        location = WeatherForecast.get_coordinates(city)
        if not location:
            return f"Could not find coordinates for '{city}'."

        lat = location["latitude"]
        lon = location["longitude"]
        state = location["state"]
        country = location["country"]

        # Combined URL for current weather and forecast
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
            f"&timezone=auto"
        )

        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to fetch weather data."

        data = response.json()

        # Current weather
        current = data.get("current_weather", {})
        temp = current.get("temperature", "N/A")
        wind = current.get("windspeed", "N/A")

        weather_info = (
            f"📍 {city.title()}, {state}, {country}\n"
            f"🌤️ Current Weather:\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"💨 Wind Speed: {wind} km/h\n\n"
        )

        # Forecast weather
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        wind_speeds = daily.get("windspeed_10m_max", [])
        precip = daily.get("precipitation_sum", [])

        forecast = "📅 3-Day Forecast:\n"
        for i in range(min(3, len(dates))):
            forecast += (
                f"{dates[i]}: 🌡️ {temps_min[i]}°C - {temps_max[i]}°C, "
                f"💨 {wind_speeds[i]} km/h, ☔ {precip[i]} mm\n"
            )

        return weather_info + forecast

# Test call
if __name__ == "__main__": 
    print(WeatherForecast.get_weather("Hyderabad"))
