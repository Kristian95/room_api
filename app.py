from fastapi import FastAPI
from routes.availability import router as availability_router
from routes.visualization import router as visualization_router

app = FastAPI(title="Room Availability API", version="1.0")

# Register routers
app.include_router(availability_router, prefix="/availability", tags=["Availability"])
app.include_router(visualization_router, prefix="/visualization", tags=["Visualization"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Room Availability API!"}
