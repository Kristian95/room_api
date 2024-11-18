from pydantic import BaseModel

class RoomQuery(BaseModel):
    query: str