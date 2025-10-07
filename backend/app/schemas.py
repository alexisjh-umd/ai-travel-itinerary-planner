from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any

class TravelerPreferences(BaseModel):
    origin: str
    destination: str
    start_date: str  # ISO
    end_date: str    # ISO
    budget: float
    party_size: int = 1
    interests: List[str] = []
    mobility_needs: Optional[str] = None

class ItineraryItem(BaseModel):
    day: int
    title: str
    time: str
    category: str   # flight, hotel, activity, meal, transit
    details: Dict[str, Any] = {}

class Itinerary(BaseModel):
    summary: str
    items: List[ItineraryItem]

class PlanRequest(BaseModel):
    preferences: TravelerPreferences

class PlanResponse(BaseModel):
    itinerary: Itinerary

class Signal(BaseModel):
    type: str   # weather_alert, closure_notice, transit_delay
    message: str
    data: Dict[str, Any] = {}

class ReplanRequest(BaseModel):
    preferences: TravelerPreferences
    current_itinerary: Itinerary
    signals: List[Signal]

class ReplanResponse(BaseModel):
    updated: bool
    changes: List[str]
    itinerary: Itinerary

class NotifyRequest(BaseModel):
    channel: str  # email, sms, webhook
    target: str
    message: str

class ExplainRequest(BaseModel):
    preferences: TravelerPreferences
    current_itinerary: Optional[Itinerary] = None
    request: str = Field(..., description="e.g., 'Reduce the budget by 15%' or 'Make it family-friendly'")

class ExplainResponse(BaseModel):
    explanation: str
    suggested_changes: List[str] = []
