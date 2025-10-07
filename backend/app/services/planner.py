from typing import List
from ..schemas import TravelerPreferences, Itinerary, ItineraryItem
from .data_providers.flights import FlightsProvider
from .data_providers.hotels import HotelsProvider
from .data_providers.events import EventsProvider
from .data_providers.places import PlacesProvider
from .data_providers.weather import WeatherProvider
from .data_providers.transit import TransitProvider
from .llm import LLMService

class PlannerService:
    def __init__(self):
        self.flights = FlightsProvider()
        self.hotels = HotelsProvider()
        self.events = EventsProvider()
        self.places = PlacesProvider()
        self.weather = WeatherProvider()
        self.transit = TransitProvider()
        self.llm = LLMService()

    async def plan(self, prefs: TravelerPreferences) -> Itinerary:
        # Fetch baseline data (mocked adapters for now)
        flights = await self.flights.search_flights(prefs.origin, prefs.destination, prefs.start_date, prefs.end_date, prefs.budget)
        hotel = await self.hotels.search_hotels(prefs.destination, (prefs.start_date, prefs.end_date), prefs.budget, prefs.party_size)
        forecast = await self.weather.get_forecast(prefs.destination, (prefs.start_date, prefs.end_date))
        activities = await self.places.search_attractions(prefs.destination, prefs.interests)
        events = await self.events.search_events(prefs.destination, (prefs.start_date, prefs.end_date), prefs.interests)

        # Create a simple day-by-day skeleton (rule-based for starter)
        items: List[ItineraryItem] = []
        day = 1
        items.append(ItineraryItem(day=day, title="Flight to Destination", time="08:00", category="flight", details=flights[0] if flights else {}))
        items.append(ItineraryItem(day=day, title="Hotel Check-in", time="15:00", category="hotel", details=hotel or {}))

        # Fill remaining days with attractions/events considering weather tag
        # (In production, you'd build a proper scheduler/optimizer here.)
        items.append(ItineraryItem(day=day, title="Welcome Dinner", time="19:00", category="meal", details={"suggestion": "Ask LLM for local cuisine near hotel"}))

        day += 1
        if events:
            items.append(ItineraryItem(day=day, title=f"Attend: {events[0]['name']}", time="13:00", category="activity", details=events[0]))
        if activities:
            items.append(ItineraryItem(day=day, title=f"Explore: {activities[0]['name']}", time="10:00", category="activity", details=activities[0]))

        # Summarize via LLM abstraction (rule-based fallback)
        summary = await self.llm.plan_itinerary_text(prefs, items, forecast)

        return Itinerary(summary=summary, items=items)
