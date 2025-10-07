class EventsProvider:
    async def search_events(self, city: str, dates: tuple[str, str], tags: list[str]):
        # Replace with Ticketmaster/Eventbrite/etc.
        return [{
            "id": "evt_789",
            "name": "City Jazz Festival",
            "date": f"{dates[0]}",
            "tags": ["music", "culture"],
            "price": 35
        }]
