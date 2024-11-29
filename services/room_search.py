import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from data.rooms import rooms

# Prepare TF-IDF and FAISS index
def prepare_faiss_index():
    descriptions = [
        f"Room {room['room_id']} in {room['location']} available from {room['available_from']} to {room['available_to']}"
        for room in rooms
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(descriptions).toarray()
    index = faiss.IndexFlatL2(tfidf_matrix.shape[1])
    index.add(np.array(tfidf_matrix, dtype=np.float32))
    return vectorizer, index, descriptions

vectorizer, index, room_descriptions = prepare_faiss_index()

def search_rooms(location: str, date: str):
    # Convert date string to datetime
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Filter rooms for availability
    available_rooms = [
        room for room in rooms
        if location.lower() in room["location"].lower()
        and datetime.strptime(room["available_from"], "%Y-%m-%d").date() <= date_obj <= datetime.strptime(room["available_to"], "%Y-%m-%d").date()
    ]
    if available_rooms:
        return available_rooms

    # If no exact match, find similar rooms
    query = f"Room in {location}"
    query_vector = vectorizer.transform([query]).toarray()
    distances, indices = index.search(query_vector.astype(np.float32), k=5)
    similar_rooms = [rooms[i] for i in indices[0] if i < len(rooms)]

    return similar_rooms
