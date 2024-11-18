from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.visualization import generate_availability_chart

router = APIRouter()

@router.get("/availability-chart")
async def availability_visualization(query: str):
    """
    Endpoint to serve the room availability visualization as a chart image.
    """
    try:
        location, _ = parse_query(query) 
        chart_path = generate_availability_chart(location=location)
        return FileResponse(chart_path, media_type="image/png", filename="availability_chart.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
