class WeatherProvider:
    async def get_forecast(self, city: str, dates: tuple[str, str]):
        # Replace with OpenWeather/NOAA/etc.
        return {
            "summary": "partly cloudy with mild temps",
            "daily": [
                {"date": dates[0], "condition": "cloudy", "high": 22, "low": 15},
                {"date": dates[1], "condition": "sunny", "high": 24, "low": 16},
            ]
        }
