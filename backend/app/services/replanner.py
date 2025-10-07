from typing import List, Tuple
from ..schemas import TravelerPreferences, Itinerary, ItineraryItem, Signal
from .llm import LLMService

class ReplannerService:
    def __init__(self):
        self.llm = LLMService()

    async def replan(self, prefs: TravelerPreferences, itinerary: Itinerary, signals: List[Signal]) -> Tuple[bool, List[str], Itinerary]:
        changes: List[str] = []
        updated = False

        for s in signals:
            if s.type == "weather_alert":
                # Example: change outdoor activity to indoor museum
                for item in itinerary.items:
                    if item.category == "activity" and "outdoor" in item.details.get("tags", []):
                        item.title = "Switch to Indoor Museum (due to weather)"
                        item.details["note"] = s.message
                        changes.append(f"Day {item.day}: swapped outdoor activity for indoor museum")
                        updated = True
            if s.type == "closure_notice":
                for item in itinerary.items:
                    if item.details.get("id") == s.data.get("place_id"):
                        item.title = "Alternative Attraction (closure)"
                        item.details["note"] = s.message
                        changes.append(f"Day {item.day}: replaced closed venue with alternative")
                        updated = True
            if s.type == "transit_delay":
                for item in itinerary.items:
                    if item.category == "transit":
                        item.details["delay_minutes"] = s.data.get("delay", 15)
                        changes.append(f"Day {item.day}: accounted for transit delay of {s.data.get('delay', 15)} minutes")
                        updated = True

        # Provide a fresh summary if updates happened
        if updated:
            itinerary.summary = await self.llm.replan_summary(prefs, itinerary, signals)

        return updated, changes, itinerary
