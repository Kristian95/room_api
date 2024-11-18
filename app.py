from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


# COMMENT-1: A single app.py file is not ideal for scalability and maintainability. Suggested refactoring: 
#       main.py: Entrypoint for FastAPI.
#       routes/: Define route-specific logic (e.g., availability.py, visualization.py).
#       services/: Include reusable logic such as LangChain integrations or room availability checks.
#       models/: Define data models like RoomQuery.
#       utils/: Helper functions like parse_query(). #


import openai
openai.api_key = "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"

app = FastAPI()


# COMMENT-5: No plase for hardcoded data here 
# #

rooms = [
    {"id": 1, "location": "Main Office", "available_from": "2024-11-17", "available_to": "2024-11-20"},
    {"id": 2, "location": "Side Building", "available_from": "2024-11-18", "available_to": "2024-11-21"},
    {"id": 3, "location": "North Wing", "available_from": "2024-11-16", "available_to": "2024-11-19"},
]

class RoomQuery(BaseModel):
    query: str

prompt_template = """
You are a helpful assistant for room availability queries. A user might ask about rooms in various locations and dates.
Extract the date and location from the following query: "{query}"
"""
prompt = PromptTemplate(input_variables=["query"], template=prompt_template)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key="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")
llm_chain = LLMChain(prompt=prompt, llm=llm)

#COMMENT-3: The parse_query() function assumes a specific format ("Location: [location], Date: [date]") from the LLM. 
# Use a more robust approach, such as extracting structured data with LangChain tools or regex.
# #

# COMMENT-4: Parsing logic in parse_query() raises generic exceptions, which could lead to vague responses. 
# Validate user input more robustly (e.g., handle invalid dates or locations gracefully).
# #

def parse_query(query: str):
    """
    Use LangChain to parse a natural language query and extract location and date.
    """
    response = llm_chain.run(query)
    location = None
    date = None
    try:
        # Assuming the response is a simple "Location: [location], Date: [date]" string
        location, date = response.split(",")
        location = location.split(":")[1].strip()
        date = date.split(":")[1].strip()
    except Exception as e:
        raise ValueError("Could not extract location or date.")
    return location, date

@app.post("/check-room-availability")
async def check_room_availability(room_query: RoomQuery):
    """
    Check the availability of rooms based on the location and date specified.
    If no exact match is found, suggest nearby rooms.
    """
    try:
        # Parse location and date from the natural language query
        location, date = parse_query(room_query.query)
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        # Filter rooms based on the provided location and date
        available_rooms = []
        for room in rooms:
            room_available_from = datetime.datetime.strptime(room["available_from"], "%Y-%m-%d").date()
            room_available_to = datetime.datetime.strptime(room["available_to"], "%Y-%m-%d").date()

            # Check if the room is available on the given date
            if location.lower() in room["location"].lower() and room_available_from <= date_obj <= room_available_to:
                available_rooms.append(room)

        # If no rooms found, suggest nearby rooms
        if not available_rooms:
            available_rooms = [
                room for room in rooms if location.lower() in room["location"].lower()
            ]
            if not available_rooms:
                raise HTTPException(status_code=404, detail="No rooms found nearby.")

        return {"available_rooms": available_rooms}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Visualization Logic


# COMMENT-2: The visualization logic generates a bar chart but doesn't link it directly to room data queries. 
# Align visualization with room queries for a more cohesive experience. Example:
#   Show a bar chart for a specific room or location based on query.
#   Embed the chart in the API response as base64, allowing easier rendering in front-end.
# #

#COMMENT-6: Proximity-Based Suggestions: No logic to suggest nearby rooms based on proximity if an exact match isn’t found. (Could include mock geospatial data and a proximity calculation.)

def get_booking_distribution():
    """
    Create a bar chart for the distribution of room availability over the past week.
    """
    today = datetime.date.today()
    past_week_dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    availability_counts = {date: 0 for date in past_week_dates}

    for room in rooms:
        room_available_from = datetime.datetime.strptime(room["available_from"], "%Y-%m-%d").date()
        room_available_to = datetime.datetime.strptime(room["available_to"], "%Y-%m-%d").date()

        for date in past_week_dates:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if room_available_from <= date_obj <= room_available_to:
                availability_counts[date] += 1

    # Generate the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(availability_counts.keys(), availability_counts.values(), color='skyblue')
    plt.xlabel("Date")
    plt.ylabel("Number of Available Rooms")
    plt.title("Room Availability Distribution Over the Past Week")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart as an image
    chart_path = "availability_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path

@app.get("/availability-visualization")
async def availability_visualization():
    """
    Endpoint to serve the room availability visualization as a chart image.
    """
    try:
        chart_path = get_booking_distribution()
        return FileResponse(chart_path, media_type="image/png", filename="availability_chart.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

