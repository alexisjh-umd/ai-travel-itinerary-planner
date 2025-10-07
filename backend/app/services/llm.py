from typing import List, Tuple, Optional
from ..schemas import TravelerPreferences, ItineraryItem, Itinerary, Signal
from ..config import settings

class LLMService:
    async def plan_itinerary_text(self, prefs: TravelerPreferences, items: List[ItineraryItem], forecast: dict) -> str:
        if settings.llm_provider == "openai":
            return await self._call_openai(self._build_prompt(prefs, items, forecast))
        # Rule-based fallback
        days = sorted({i.day for i in items})
        return (
            f"Itinerary for {prefs.destination} from {prefs.start_date} to {prefs.end_date} "
            f"for {prefs.party_size} traveler(s), budget ${prefs.budget:.0f}. "
            f"Weather looks {forecast.get('summary','mixed')}. "
            f"Planned {len(items)} activities across {len(days)} day(s)."
        )

    async def replan_summary(self, prefs: TravelerPreferences, itinerary: Itinerary, signals: List[Signal]) -> str:
        if settings.llm_provider == "openai":
            return await self._call_openai(self._build_replan_prompt(prefs, itinerary, signals))
        kinds = ", ".join({s.type for s in signals})
        return f"Replanned itinerary due to signals: {kinds}. Adjustments applied where needed."

    async def explain_tradeoffs(self, prefs: TravelerPreferences, itinerary: Optional[Itinerary], user_req: str) -> Tuple[str, List[str]]:
        # Simple heuristic explainer for demo
        suggestions: List[str] = []
        explanation = f"You asked: '{user_req}'. "
        if "budget" in user_req.lower():
            suggestions.append("Prefer 2-3 star hotels with high reviews to save cost")
            suggestions.append("Choose morning/weekday flights for cheaper fares")
            suggestions.append("Bundle attractions with city passes")
            explanation += "We identified cost-saving levers across hotels, flights, and attractions."
        elif "family" in user_req.lower():
            suggestions.append("Swap late-night events for kid-friendly daytime activities")
            suggestions.append("Add indoor options in case of weather")
            suggestions.append("Ensure attractions are stroller-accessible")
            explanation += "We prioritized family-friendly, accessible activities."
        elif "museum" in user_req.lower():
            suggestions.append("Allocate a full morning block for a museum, with timed tickets")
            suggestions.append("Add nearby lunch spots to reduce transit time")
            explanation += "We added a culture-focused block with time-boxing."
        else:
            suggestions.append("Balance must-see spots with buffer time")
            explanation += "We proposed general improvements to pacing and variety."
        return explanation, suggestions

    def _build_prompt(self, prefs: TravelerPreferences, items: List[ItineraryItem], forecast: dict) -> str:
        return f"""Create a concise itinerary summary for:
Destination: {prefs.destination}
Dates: {prefs.start_date} to {prefs.end_date}
Party Size: {prefs.party_size}
Budget: {prefs.budget}
Interests: {', '.join(prefs.interests) if prefs.interests else 'general'}
Weather: {forecast}
Items: {[i.model_dump() for i in items]}
"""

    def _build_replan_prompt(self, prefs: TravelerPreferences, itinerary: Itinerary, signals: List[Signal]) -> str:
        return f"""Summarize changes after re-planning.
Signals: {[s.model_dump() for s in signals]}
Itinerary: {itinerary.model_dump()}
"""

    async def _call_openai(self, prompt: str) -> str:
        # TODO: integrate with OpenAI Chat Completions or Responses API
        # Keep this placeholder to avoid external calls in the starter.
        return "LLM summary placeholder (replace with real provider call)."
