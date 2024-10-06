from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="NASA Earth Observation API")

NASA_EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

@app.get("/")
async def root():
    return {"message": "Welcome to the NASA Earth Observation API"}

@app.get("/events")
async def get_events(limit: int = 10, days: int = 20):
    async with httpx.AsyncClient() as client:
        response = await client.get(NASA_EONET_URL, params={"limit": limit, "days": days})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from NASA EONET")
    
    data = response.json()
    return data["events"]

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NASA_EONET_URL}/{event_id}")
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch event data from NASA EONET")
    
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)