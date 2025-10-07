class PlacesProvider:
    async def search_attractions(self, city: str, tags: list[str]):
        # Replace with Yelp/TripAdvisor/Google Places
        return [{
            "id": "poi_001",
            "name": "Old Town Walking District",
            "tags": ["outdoor", "food", "historic"]
        },{
            "id": "poi_002",
            "name": "National History Museum",
            "tags": ["indoor", "museum", "family"]
        }]
