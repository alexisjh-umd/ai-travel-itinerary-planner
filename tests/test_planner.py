import pytest
from backend.app.services.planner import PlannerService
from backend.app.schemas import TravelerPreferences

import asyncio

@pytest.mark.asyncio
async def test_basic_plan():
    svc = PlannerService()
    prefs = TravelerPreferences(
        origin="IAD",
        destination="SFO",
        start_date="2025-11-10",
        end_date="2025-11-14",
        budget=1500,
        party_size=2,
        interests=["food", "museum"]
    )
    it = await svc.plan(prefs)
    assert len(it.items) >= 3
    assert "Itinerary for" in it.summary
