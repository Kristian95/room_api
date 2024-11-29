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
    "available_rooms": [
        {
            "id": 1,
            "location": "Main Office",
            "available_from": "2024-11-17",
            "available_to": "2024-11-20"
        }
    ]
}

2.  Availability Visualization

URL: http://127.0.0.1:8000/visualization/availability-chart

Method: GET

Response: Returns a .png file showing the room availability distribution over the past 7 days.
You can download or view the chart in your browser.
