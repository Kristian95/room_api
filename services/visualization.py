import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
import base64
from data.rooms import rooms

def find_similar_rooms(query, threshold=0.5):
    """
    Finds similar rooms based on the given query using TfidfVectorizer and cosine similarity.
    """
    room_descriptions = [room["description"] for room in rooms]
    room_ids = [room["room_id"] for room in rooms]

    # Initialize the TfidfVectorizer and transform room descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(room_descriptions)

    # Transform the query into the vector space
    query_vector = vectorizer.transform([query])

    # Compute cosine similarity between query and room descriptions
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Find rooms with similarity above the threshold
    similar_room_ids = [
        room_ids[i] for i in range(len(similarities)) if similarities[i] >= threshold
    ]

    return similar_room_ids


def generate_availability_chart(location=None, room_id=None, query=None):
    """
    Generate a bar chart for the availability of rooms based on location, room_id, or a text query.
    """
    today = datetime.datetime.today().date()
    past_week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    availability_counts = {date: 0 for date in past_week_dates}

    filtered_rooms = []

    #Use location or room_id to filter rooms
    if location or room_id:
        filtered_rooms = [
            room for room in rooms
            if (location and location.lower() in room["location"].lower()) or (room_id and room["room_id"] == room_id)
        ]
    #Use the query with TfidfVectorizer for vector-based search
    elif query:
        similar_room_ids = find_similar_rooms(query)
        filtered_rooms = [room for room in rooms if room["room_id"] in similar_room_ids]

    if not filtered_rooms:
        raise ValueError(f"No data found for location '{location}', room ID '{room_id}', or query '{query}'.")

    # Calculate availability counts for the past week
    for room in filtered_rooms:
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
    plt.title(f"Room Availability for {'Room ' + room_id if room_id else location or 'Query: ' + query} Over the Past Week")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Encode the image as Base64
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return img_base64
