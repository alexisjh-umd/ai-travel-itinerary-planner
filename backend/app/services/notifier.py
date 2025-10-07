class NotifierService:
    async def send(self, channel: str, target: str, message: str) -> bool:
        # Stub for email/SMS/webhook integrations
        # Implement SendGrid/Twilio/webhook POST here
        print(f"[notify] {channel} -> {target}: {message}")
        return True
