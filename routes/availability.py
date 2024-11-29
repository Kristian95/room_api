from fastapi import APIRouter, HTTPException
from models.room_query import RoomQuery
from services.query_parser import parse_query
from services.room_search import search_rooms

router = APIRouter()

@router.post("/check-room")
async def check_room_availability(room_query: RoomQuery):
    try:
        # Parse query using OpenAI
        location, date = parse_query(room_query.query)

        # Search for rooms
        rooms = search_rooms(location, date)

        if not rooms:
            raise HTTPException(status_code=404, detail="No rooms found.")

        return {"available_rooms": rooms}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
