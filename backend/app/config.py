from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    llm_provider: str = os.getenv("LLM_PROVIDER", "rule_based")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

    # Example external providers
    skyscanner_api_key: str | None = os.getenv("SKYSCANNER_API_KEY")
    amadeus_api_key: str | None = os.getenv("AMADEUS_API_KEY")
    yelp_api_key: str | None = os.getenv("YELP_API_KEY")
    tripadvisor_api_key: str | None = os.getenv("TRIPADVISOR_API_KEY")
    ticketmaster_api_key: str | None = os.getenv("TICKETMASTER_API_KEY")
    openweather_api_key: str | None = os.getenv("OPENWEATHER_API_KEY")
    rome2rio_api_key: str | None = os.getenv("ROME2RIO_API_KEY")

    # Notifications
    sendgrid_api_key: str | None = os.getenv("SENDGRID_API_KEY")
    twilio_sid: str | None = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token: str | None = os.getenv("TWILIO_AUTH_TOKEN")

settings = Settings()
