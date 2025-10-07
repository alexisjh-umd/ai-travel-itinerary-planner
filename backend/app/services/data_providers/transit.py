class TransitProvider:
    async def get_routes(self, city: str, origin: str, dest: str, when: str):
        # Replace with Rome2Rio/City transit APIs
        return [{
            "mode": "metro",
            "duration_min": 22,
            "transfers": 1
        }]
