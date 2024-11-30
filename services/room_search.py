import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from data.rooms import rooms

# Prepare TF-IDF vectors and FAISS index
def prepare_faiss_index():
    """
    Prepares a FAISS index and corresponding TF-IDF vectorization for room descriptions.
    """
    descriptions = [
        f"Room {room['room_id']} in {room['location']} available from {room['available_from']} to {room['available_to']}"
        for room in rooms
    ]
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(descriptions).toarray()

    # Initialize and populate FAISS index
    index = faiss.IndexFlatL2(tfidf_matrix.shape[1])  # L2 distance metric
    index.add(np.array(tfidf_matrix, dtype=np.float32))
    
    return vectorizer, index, descriptions

# Prepare the FAISS index and vectorizer
vectorizer, index, room_descriptions = prepare_faiss_index()

# Room search function
def search_rooms(location: str, date: str):
    """
    Search for available rooms by location and date. If no exact match is found,
    similar rooms are suggested using vector search.
    """
    # Convert date string to a datetime object
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Filter rooms based on availability
    available_rooms = [
        room for room in rooms
        if location.lower() in room["location"].lower()
        and datetime.strptime(room["available_from"], "%Y-%m-%d").date() <= date_obj <= datetime.strptime(room["available_to"], "%Y-%m-%d").date()
    ]

    # Return exact matches if available
    if available_rooms:
        return {"matches": available_rooms, "similar": []}

    # If no exact match, find similar rooms using vector search
    query = f"Room in {location}"
    query_vector = vectorizer.transform([query]).toarray()

    # Perform FAISS search
    distances, indices = index.search(query_vector.astype(np.float32), k=5)  # Get top 5 similar results
    similar_rooms = [rooms[i] for i in indices[0] if i < len(rooms)]  # Ensure indices are within range

    return {"matches": [], "similar": similar_rooms}
