import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from optimizer.kiwi_client import KiwiClient
from optimizer.flight_optimizer import find_best_flight_per_km

# Load environment variables from .env file (for local development)
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptimizeRequest(BaseModel):
    """Request model for flight optimization."""
    from_city: str
    to_cities: list[str]


class OptimizeResponse(BaseModel):
    """Response model for flight optimization."""
    destination: str
    price_per_km: float
    price_usd: float | None = None
    distance_km: float | None = None
    airport_from: str | None = None
    airport_to: str | None = None


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_flight(request: OptimizeRequest):
    """
    Find the best flight destination by price per kilometer.
    
    Args:
        request: OptimizeRequest with from_city and to_cities

    Returns:
        OptimizeResponse with best destination and metrics
    """
    try:
        api_key = os.environ.get("KIWI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="API key not configured"
            )
        
        # Create Kiwi client
        kiwi_client = KiwiClient(api_key)
        
        result = find_best_flight_per_km(
            request.from_city,
            request.to_cities,
            kiwi_client
        )
        
        return OptimizeResponse(**result)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Flight Optimizer API"}
