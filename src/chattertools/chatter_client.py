from .chatter_requestor import ChatterRequestor
from .services.machine_service import MachineService

class ChatterClient:
    def __init__(self, key: str, baseUrl: str = "https://apiv2.chatter.dev"):
        if key is None:
            raise ValueError("An API key is required")
        self.key = key
        self.baseUrl = baseUrl
        self._requestor = ChatterRequestor(key, baseUrl)

        # Services
        self.machine = MachineService(self._requestor)