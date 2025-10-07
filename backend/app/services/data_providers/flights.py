class FlightsProvider:
    async def search_flights(self, origin: str, dest: str, start_date: str, end_date: str, budget: float):
        # Replace with real API
        return [{
            "id": "flt_123",
            "origin": origin,
            "destination": dest,
            "depart": f"{start_date}T08:00",
            "return": f"{end_date}T18:00",
            "price": min(budget * 0.4, 450),
            "carrier": "Demo Air"
        }]
