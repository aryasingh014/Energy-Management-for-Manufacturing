from fastapi import APIRouter
from typing import List, Optional

router = APIRouter(prefix="/v1/hierarchy", tags=["Hierarchy"])

# ponytail: static industrial hierarchy fixtures (no DB overhead)
PLANTS = [
    {"id": "plt-01", "name": "Detroit Assembly & Stamping Plant 01", "location": "Detroit, MI", "timezone": "America/Detroit", "currency": "USD"},
    {"id": "plt-02", "name": "Stuttgart Precision Powertrain Facility", "location": "Stuttgart, Germany", "timezone": "Europe/Berlin", "currency": "EUR"},
]

AREAS = [
    {"id": "area-01", "plant_id": "plt-01", "name": "Body & Stamping Shop", "area_type": "Press & Weld"},
    {"id": "area-02", "plant_id": "plt-01", "name": "Paint & Thermal Coating", "area_type": "Surface Treatment"},
    {"id": "area-03", "plant_id": "plt-01", "name": "Final Assembly & Testing", "area_type": "Assembly"},
]

LINES = [
    {"id": "line-01", "area_id": "area-01", "name": "High-Tonnage Hydraulic Press Line 01", "product_family": "Chassis"},
    {"id": "line-02", "area_id": "area-01", "name": "Robotic Spot Welding Cell Line 03", "product_family": "BIW"},
    {"id": "line-03", "area_id": "area-02", "name": "Thermal Curing Oven Line 02", "product_family": "Coating"},
]

MACHINES = [
    {"id": "mch-01", "line_id": "line-01", "name": "Hydraulic Press HP-2500", "rated_power_kw": 450.0, "status": "Running"},
    {"id": "mch-02", "line_id": "line-01", "name": "Sheet Feeder SF-12", "rated_power_kw": 75.0, "status": "Running"},
    {"id": "mch-03", "line_id": "line-02", "name": "KUKA Spot Welding Robot R1", "rated_power_kw": 120.0, "status": "Running"},
    {"id": "mch-04", "line_id": "line-03", "name": "Infrared Oven Zone A", "rated_power_kw": 320.0, "status": "Running"},
]

@router.get("/plants")
async def get_plants():
    return PLANTS

@router.get("/areas")
async def get_areas(plant_id: Optional[str] = None):
    if plant_id:
        return [a for a in AREAS if a["plant_id"] == plant_id]
    return AREAS

@router.get("/lines")
async def get_lines(area_id: Optional[str] = None):
    if area_id:
        return [l for l in LINES if l["area_id"] == area_id]
    return LINES

@router.get("/machines")
async def get_machines(line_id: Optional[str] = None):
    if line_id:
        return [m for m in MACHINES if m["line_id"] == line_id]
    return MACHINES

