"""Weather API client using wttr.in"""
import httpx
from typing import Optional, Dict, Any


class WeatherAPI:
    """Fetches weather data from wttr.in"""
    
    def __init__(self, city: str = "Kyiv"):
        self.city = city
        self.base_url = "https://wttr.in"
    
    async def get_weather(self) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data
        
        Returns:
            Dict with weather information or None on error
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Use format=j1 for JSON response
                response = await client.get(
                    f"{self.base_url}/{self.city}?format=j1"
                )
                response.raise_for_status()
                data = response.json()
                
                # Parse the response
                current = data.get("current_condition", [{}])[0]
                
                return {
                    "temp_c": current.get("temp_C", "N/A"),
                    "temp_f": current.get("temp_F", "N/A"),
                    "condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                    "humidity": current.get("humidity", "N/A"),
                    "wind_kph": current.get("windspeedKmph", "N/A"),
                    "wind_mph": current.get("windspeedMiles", "N/A"),
                    "city": self.city,
                    "feels_like_c": current.get("FeelsLikeC", "N/A"),
                    "weather_code": current.get("weatherCode", "113"),
                }
        except Exception as e:
            return {
                "temp_c": "N/A",
                "temp_f": "N/A",
                "condition": f"Error: {str(e)[:30]}",
                "humidity": "N/A",
                "wind_kph": "N/A",
                "wind_mph": "N/A",
                "city": self.city,
                "feels_like_c": "N/A",
                "weather_code": "113",
            }
    
    @staticmethod
    def get_weather_icon(weather_code: str) -> str:
        """
        Get ASCII weather icon based on weather code
        
        Args:
            weather_code: Weather condition code
            
        Returns:
            ASCII art weather icon
        """
        # Weather codes from wttr.in
        code_map = {
            "113": "☀",  # Clear/Sunny
            "116": "⛅",  # Partly cloudy
            "119": "☁",  # Cloudy
            "122": "☁",  # Overcast
            "143": "🌫",  # Mist
            "176": "🌦",  # Patchy rain possible
            "179": "🌨",  # Patchy snow possible
            "182": "🌧",  # Patchy sleet possible
            "185": "🌧",  # Patchy freezing drizzle
            "200": "⛈",  # Thundery outbreaks
            "227": "🌨",  # Blowing snow
            "230": "❄",  # Blizzard
            "248": "🌫",  # Fog
            "260": "🌫",  # Freezing fog
            "263": "🌦",  # Patchy light drizzle
            "266": "🌧",  # Light drizzle
            "281": "🌧",  # Freezing drizzle
            "284": "🌧",  # Heavy freezing drizzle
            "293": "🌦",  # Patchy light rain
            "296": "🌧",  # Light rain
            "299": "🌧",  # Moderate rain at times
            "302": "🌧",  # Moderate rain
            "305": "🌧",  # Heavy rain at times
            "308": "🌧",  # Heavy rain
            "311": "🌧",  # Light freezing rain
            "314": "🌧",  # Moderate or heavy freezing rain
            "317": "🌨",  # Light sleet
            "320": "🌨",  # Moderate or heavy sleet
            "323": "🌨",  # Patchy light snow
            "326": "❄",  # Light snow
            "329": "❄",  # Patchy moderate snow
            "332": "❄",  # Moderate snow
            "335": "❄",  # Patchy heavy snow
            "338": "❄",  # Heavy snow
            "350": "🌧",  # Ice pellets
            "353": "🌦",  # Light rain shower
            "356": "🌧",  # Moderate or heavy rain shower
            "359": "🌧",  # Torrential rain shower
            "362": "🌨",  # Light sleet showers
            "365": "🌨",  # Moderate or heavy sleet showers
            "368": "🌨",  # Light snow showers
            "371": "❄",  # Moderate or heavy snow showers
            "374": "🌧",  # Light showers of ice pellets
            "377": "🌧",  # Moderate or heavy showers of ice pellets
            "386": "⛈",  # Patchy light rain with thunder
            "389": "⛈",  # Moderate or heavy rain with thunder
            "392": "⛈",  # Patchy light snow with thunder
            "395": "⛈",  # Moderate or heavy snow with thunder
        }
        return code_map.get(weather_code, "☁")
