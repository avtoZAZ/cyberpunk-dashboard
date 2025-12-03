"""Weather display widget"""
from textual.widgets import Static
from textual.reactive import reactive
from dashboard.api.weather_api import WeatherAPI
from typing import Optional, Dict, Any


class WeatherWidget(Static):
    """Widget to display current weather"""
    
    weather_data = reactive(None)
    
    def __init__(self, city: str = "Kyiv"):
        super().__init__()
        self.api = WeatherAPI(city)
        self.city = city
    
    def on_mount(self) -> None:
        """Set up update interval when mounted"""
        self.update_interval = self.set_interval(300.0, self.update_weather)  # Update every 5 minutes
        self.call_later(self.update_weather)  # Immediate first update
    
    async def update_weather(self) -> None:
        """Fetch and update weather data"""
        self.weather_data = await self.api.get_weather()
        self.refresh()
    
    def render(self) -> str:
        """Render the weather display"""
        if not self.weather_data:
            return self._render_loading()
        
        data = self.weather_data
        icon = WeatherAPI.get_weather_icon(data.get("weather_code", "113"))
        temp_c = data.get("temp_c", "N/A")
        temp_f = data.get("temp_f", "N/A")
        feels_like = data.get("feels_like_c", "N/A")
        condition = data.get("condition", "N/A")
        humidity = data.get("humidity", "N/A")
        wind_kph = data.get("wind_kph", "N/A")
        city = data.get("city", self.city)
        
        # Truncate condition if too long
        if len(condition) > 20:
            condition = condition[:17] + "..."
        
        output = f"""╔═══════════════════════════════╗
║ 🌍 WEATHER                    ║
╠═══════════════════════════════╣
║                               ║
║      {icon}  {city:^20s}       ║
║                               ║
║  Temperature: {temp_c:>5s}°C        ║
║  Feels Like:  {feels_like:>5s}°C        ║
║  {condition:^29s} ║
║                               ║
║  Humidity: {humidity:>5s}%            ║
║  Wind: {wind_kph:>6s} km/h          ║
║                               ║
╚═══════════════════════════════╝"""
        
        return output
    
    def _render_loading(self) -> str:
        """Render loading state"""
        return f"""╔═══════════════════════════════╗
║ 🌍 WEATHER                    ║
╠═══════════════════════════════╣
║                               ║
║      Loading weather...       ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
╚═══════════════════════════════╝"""
