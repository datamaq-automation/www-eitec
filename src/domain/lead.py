from pydantic import BaseModel
from typing import Protocol

class Lead(BaseModel):
    nombre: str
    email: str
    telefono: str
    mensaje: str

class LeadNotifier(Protocol):
    async def notify(self, lead: Lead) -> None:
        ...
