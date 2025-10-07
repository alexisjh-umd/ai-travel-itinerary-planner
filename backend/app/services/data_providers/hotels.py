class HotelsProvider:
    async def search_hotels(self, city: str, dates: tuple[str, str], budget: float, party_size: int):
        # Replace with real API
        return {
            "id": "hot_456",
            "name": "Sample Suites Downtown",
            "check_in": f"{dates[0]}",
            "check_out": f"{dates[1]}",
            "nightly_rate": min(budget * 0.1, 120),
            "rating": 4.2,
            "address": f"Center, {city}"
        }
