def parse_query(query: str):
    """
    Simulate OpenAI GPT response for extracting location and date from a natural language query.
    """
    # Define simulated responses for test queries
    mock_responses = {
        'I need a room in the Main Office on 2024-11-17': 'Location: Main Office, Date: 2024-11-17',
        'Book a room in Side Building on 2024-11-18': 'Location: Side Building, Date: 2024-11-18',
        'Check availability in North Wing on 2024-11-19': 'Location: North Wing, Date: 2024-11-19',
    }

    try:
        # Simulate the behavior of the OpenAI API by returning pre-defined responses
        if query in mock_responses:
            result = mock_responses[query]
        else:
            # Default response for unrecognized queries
            result = 'Location: Unknown, Date: 1970-01-01'

        # Parse the result into location and date
        location, date = result.split(",")
        location = location.split(":")[1].strip()
        date = date.split(":")[1].strip()
        return location, date

    except Exception as e:
        raise ValueError(f"Error parsing query: {str(e)}")
