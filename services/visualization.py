import datetime
import matplotlib.pyplot as plt
from data.rooms import rooms

def generate_availability_chart(location=None, room_id=None):
    """
    Generate a bar chart for the availability of a specific room or location.
    """
    today = datetime.today().date()
    past_week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    availability_counts = {date: 0 for date in past_week_dates}

    # Filter rooms by location or room_id
    filtered_rooms = [
        room for room in rooms
        if (location and location.lower() in room["location"].lower()) or (room_id and room["room_id"] == room_id)
    ]

    if not filtered_rooms:
        raise ValueError(f"No data found for location '{location}' or room ID '{room_id}'.")

    # Calculate availability counts for the past week
    for room in filtered_rooms:
        room_available_from = datetime.strptime(room["available_from"], "%Y-%m-%d").date()
        room_available_to = datetime.strptime(room["available_to"], "%Y-%m-%d").date()

        for date in past_week_dates:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            if room_available_from <= date_obj <= room_available_to:
                availability_counts[date] += 1

    # Generate the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(availability_counts.keys(), availability_counts.values(), color='skyblue')
    plt.xlabel("Date")
    plt.ylabel("Number of Available Rooms")
    plt.title(f"Room Availability for {'Room ' + room_id if room_id else location} Over the Past Week")
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