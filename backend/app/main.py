from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    PlanRequest, PlanResponse, ReplanRequest, ReplanResponse,
    NotifyRequest, ExplainRequest, ExplainResponse
)
from .services.planner import PlannerService
from .services.replanner import ReplannerService
from .services.notifier import NotifierService
from .services.llm import LLMService

app = FastAPI(title="Dynamic Travel Itinerary Planner", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = PlannerService()
replanner = ReplannerService()
notifier = NotifierService()
llm = LLMService()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/itinerary", response_model=PlanResponse)
async def plan_itinerary(req: PlanRequest):
    itinerary = await planner.plan(req.preferences)
    return PlanResponse(itinerary=itinerary)

@app.post("/replan", response_model=ReplanResponse)
async def replan_itinerary(req: ReplanRequest):
    updated, changes, itinerary = await replanner.replan(req.preferences, req.current_itinerary, req.signals)
    return ReplanResponse(updated=updated, changes=changes, itinerary=itinerary)

@app.post("/notify")
async def notify(req: NotifyRequest):
    ok = await notifier.send(req.channel, req.target, req.message)
    return {"ok": ok}

@app.post("/explain", response_model=ExplainResponse)
async def explain(req: ExplainRequest):
    text, suggestions = await llm.explain_tradeoffs(req.preferences, req.current_itinerary, req.request)
    return ExplainResponse(explanation=text, suggested_changes=suggestions)
