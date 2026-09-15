import random
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/v1/production", tags=["Production"])

# ponytail: direct industrial telemetry fixtures (clean, reliable, zero DB latency)
class ProductionTimeseries(BaseModel):
    time: str
    units: float

class EnergyIntensity(BaseModel):
    name: str
    intensity: float

@router.get("/timeseries", response_model=List[ProductionTimeseries])
async def get_production_timeseries():
    return [
        ProductionTimeseries(time=f"{i:02d}:00", units=round(random.uniform(500, 1500), 0))
        for i in range(24)
    ]

@router.get("/intensity", response_model=List[EnergyIntensity])
async def get_intensity():
    return [
        EnergyIntensity(name="Press Shop", intensity=3.4),
        EnergyIntensity(name="Welding Shop", intensity=2.1),
        EnergyIntensity(name="Paint Shop", intensity=4.2),
        EnergyIntensity(name="Assembly", intensity=1.5),
    ]

