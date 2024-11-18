from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.room_query import RoomQuery
from services.query_parser import parse_query
from data.rooms import rooms

router = APIRouter()

@router.post("/check-room")
async def check_room_availability(room_query: RoomQuery):
    """
    Check the availability of rooms based on the location and date specified.
    If no exact match is found, suggest nearby rooms.
    """
    try:
        # Parse location and date from the query
        location, date = parse_query(room_query.query)
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # Filter rooms based on location and date
        available_rooms = [
            room for room in rooms
            if location.lower() in room["location"].lower()
            and datetime.strptime(room["available_from"], "%Y-%m-%d").date() <= date_obj <= datetime.strptime(room["available_to"], "%Y-%m-%d").date()
        ]

        # If no exact matches, suggest nearby rooms
        if not available_rooms:
            nearby_rooms = [
                room for room in rooms
                if location.lower() in room["location"].lower()
            ]
            if not nearby_rooms:
                raise HTTPException(status_code=404, detail="No rooms found nearby.")
            return {"available_rooms": nearby_rooms}

        return {"available_rooms": available_rooms}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
