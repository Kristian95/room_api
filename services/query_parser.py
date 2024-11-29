import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPEN_API_KEY")

def parse_query(query: str):
    """
    Use OpenAI GPT to extract location and date from a natural language query.
    """
    prompt = f"""
    You are a helpful assistant for room availability queries.
    Extract the location and date from the following query: "{query}".
    Respond in this format: "Location: <location>, Date: <YYYY-MM-DD>".
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-3.5-turbo" if you're using that model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the assistant's response
        result = response['choices'][0]['message']['content'].strip()
        
        # Parse the result into location and date
        location, date = result.split(",")
        location = location.split(":")[1].strip()
        date = date.split(":")[1].strip()
        return location, date
    except Exception as e:
        raise ValueError(f"Error parsing query: {str(e)}")
