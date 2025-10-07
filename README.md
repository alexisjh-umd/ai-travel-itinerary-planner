# Dynamic Travel Itinerary Planner

An end-to-end starter repo for a **Generative AI–powered, adaptive travel itinerary planner**.  
It ships with a **FastAPI** backend, a tiny vanilla JS frontend, and **Docker** support—perfect for development in VS Code and pushing to GitHub.

---

## What our team has included

- **FastAPI backend** with clean architecture:
  - `PlannerService` to compose Day-by-Day itineraries
  - `ReplannerService` to adapt plans when conditions change (weather/closures/transit)
  - **Adapters** for external data providers (Flights, Hotels, Events, Places, Weather, Transit) – currently mocked with safe placeholders
  - `LLMService` abstraction (drop-in for OpenAI/Anthropic/etc.) with a rule-based fallback
- **Minimal Frontend** (`frontend/`) powered by vanilla JS + Fetch for quick demos
- **Typed request/response schemas** via Pydantic
- **.env example** and `Config` loader
- **Dockerfile + docker-compose.yml** for one-command local dev
- **Tests** with pytest for critical flows
- **GitHub-friendly layout**

---

## Project Structure

```
dynamic-travel-itinerary-planner/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ schemas.py
│  │  └─ services/
│  │     ├─ planner.py
│  │     ├─ replanner.py
│  │     ├─ notifier.py
│  │     ├─ llm.py
│  │     └─ data_providers/
│  │        ├─ flights.py
│  │        ├─ hotels.py
│  │        ├─ events.py
│  │        ├─ places.py
│  │        ├─ weather.py
│  │        └─ transit.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
├─ frontend/
│  ├─ index.html
│  ├─ script.js
│  └─ styles.css
├─ tests/
│  └─ test_planner.py
├─ docker-compose.yml
└─ README.md
```

---

## Quickstart (Local)

**Prereqs:** Python 3.10+, Node (optional), Docker (optional).

### Option A — Python (no Docker)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then fill in any keys you have
uvicorn app.main:app --reload --port 8000
```

Open the demo frontend:
```bash
# in another terminal
cd ../frontend
python -m http.server 5173
# visit http://localhost:5173
```

### Option B — Docker
```bash
docker compose up --build
# backend at http://localhost:8000 ; frontend at http://localhost:5173
```

---

## Plugging In Real Providers (APIs)

Each provider in `backend/app/services/data_providers/` is an adapter with a simple interface and a mocked `fetch_*` method.  
Replace the mocks with real API calls (e.g., Skyscanner, Amadeus, Yelp, TripAdvisor, Ticketmaster, Rome2Rio, OpenWeather).

**Example shape to implement:**
- `FlightsProvider.search_flights(origin, dest, start_date, end_date, budget)`
- `HotelsProvider.search_hotels(city, dates, budget, party_size)`
- `EventsProvider.search_events(city, dates, tags)`
- `PlacesProvider.search_attractions(city, tags)`
- `WeatherProvider.get_forecast(city, dates)`
- `TransitProvider.get_routes(city, origin, dest, when)`

Add your API keys to `.env` and read them in `config.py`.

---

## LLM Integration

`LLMService` exposes `plan_itinerary_text()` and `explain_tradeoffs()` with a **rule-based fallback** that works offline.  
To use a provider (e.g., OpenAI):

1. Add your key to `.env` (`OPENAI_API_KEY=...`).
2. Implement `_call_openai()` in `llm.py` (left with a TODO).
3. Set `LLM_PROVIDER=openai` in `.env`.

---

##  Dynamic Re-Planning

`ReplannerService` ingests **signals** (weather changes, closures, transit delays) and returns **diffs** with rationale.  
Wire it to a scheduler/webhook (e.g., run every 15 minutes) and call `replan()` with the latest signals.

---

## Tests
```bash
pytest -q
```

---

## VS Code Tips

- Install extensions: **Python**, **Pylance**, **Black**, **isort**, **EditorConfig**, **Thunder Client** (or use curl)  
- Debug config: run `uvicorn app.main:app --reload`
- Use `/docs` (Swagger) at `http://localhost:8000/docs`

---

## Security & Privacy Notes

- Store API keys in `.env` (never commit real secrets).
- Rate-limit external calls. Cache responses where possible.
- Log **metadata only**. Avoid logging PII like passport numbers.
- Add consent flags for user data retention/export.

---

## Roadmap Ideas

- OAuth login + per-user profiles and preferences
- Calendar export (iCal) and email/SMS notifications
- Map tiles and route visualizations
- Multi-city itineraries and constraint solver for best fit
- A richer React (Next.js) frontend or mobile app

---

