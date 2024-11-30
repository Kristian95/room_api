# Features
Check Room Availability: Parse natural language queries to check for available rooms based on location and date.

Availability Visualization: Generates a bar chart showing the distribution of room availability over the past 7 days.

# Setup Instructions
1. Prerequisites
Before setting up the application, ensure the following prerequisites are met:

Python: Version 3.10 or higher is installed. You can verify your Python version by running:

# Clone the Repository
Clone this repository to your local machine:

git clone <git@github.com:Kristian95/room_api.git>

cd <room_api>

# Install Dependencies

fastapi: Web framework for building APIs.

uvicorn: ASGI server to run the FastAPI app.

langchain: For language model interactions.

openai: To interact with OpenAI's API.

matplotlib: For generating charts.

pydantic: For data validation.

# Setup API key
openai.api_key = "your_openai_api_key"

RUN: uvicorn app:app --reload

# Endpoints
1. Check Room Availability
   
URL: http://127.0.0.1:8000/availability/check-room

Method: POST

Request Body

{
    "query": "Are there any rooms available in the Main Office on 2024-11-18?"
}

Response

{
    "available_rooms": {
        "matches": [],
        "similar": [
            {
                "room_id": "102",
                "location": "Side Building",
                "description": "A quiet room in the Side Building, ideal for small meetings.",
                "available_from": "2024-11-15",
                "available_to": "2024-11-25"
            },
            {
                "room_id": "301",
                "location": "East Wing",
                "description": "A bright and modern room in the East Wing with great views.",
                "available_from": "2024-11-20",
                "available_to": "2024-11-30"
            },
            {
                "room_id": "101",
                "location": "Main Office",
                "description": "A spacious room located in the Main Office with modern facilities.",
                "available_from": "2024-11-10",
                "available_to": "2024-11-20"
            },
            {
                "room_id": "201",
                "location": "North Wing",
                "description": "A large conference room in the North Wing, suitable for group discussions.",
                "available_from": "2024-11-18",
                "available_to": "2024-11-28"
            },
            {
                "room_id": "401",
                "location": "West Building",
                "description": "A cozy room in the West Building, perfect for individual work.",
                "available_from": "2024-11-22",
                "available_to": "2024-12-02"
            }
        ]
    }
}

2.  Availability Visualization

URL: http://127.0.0.1:8000/visualization/availability-chart?query=Show+me+rooms+in+New+York

Method: GET

Response: Returns a .png file showing the room availability distribution over the past 7 days.
You can download or view the chart in your browser.
