import random
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/energy", tags=["Energy"])

@router.get("/metrics")
async def get_metrics():
    # Dynamic live variation based on current time
    now = datetime.now()
    jitter = (random.random() - 0.5) * 200
    base_kwh = 57739.0 + jitter
    rate = 2.25
    cost = base_kwh * rate
    prod_units = int(38420 + (random.random() - 0.5) * 150)
    intensity = round(base_kwh / prod_units, 2)
    co2 = round(base_kwh * 0.0004, 1)
    solar_share = round(38.4 + (random.random() - 0.5) * 1.5, 1)

    return {
        "total_energy_consumption_kwh": round(base_kwh, 1),
        "energy_cost_currency": round(cost, 2),
        "production_output_units": prod_units,
        "energy_intensity_kwh_per_unit": intensity,
        "co2_emissions_tco2e": co2,
        "renewable_contribution_pct": solar_share,
        "current_demand_mw": round(4.75 + random.random() * 0.15, 2),
        "electricity_mw": round(4.75 + random.random() * 0.15, 2),
        "natural_gas_m3h": int(1230 + random.random() * 25),
        "compressed_air_bar": round(6.25 + random.random() * 0.1, 1),
        "steam_tonh": round(2.55 + random.random() * 0.1, 1),
        "water_m3h": round(18.2 + random.random() * 0.4, 1),
        "total_primary_mw": round(5.90 + random.random() * 0.08, 2),
        "timestamp": now.isoformat(),
    }

@router.get("/timeseries")
async def get_timeseries():
    hours = ["12 AM", "2 AM", "4 AM", "6 AM", "8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM", "8 PM", "10 PM"]
    base_vals = [3100, 3200, 3000, 4500, 6200, 7400, 6842, 7100, 5800, 6300, 5200, 4100]
    return [
        {
            "time": hr,
            "kwh": int(base_vals[i] + (random.random() - 0.5) * 180),
            "baseline": int(base_vals[i] * 0.95),
        }
        for i, hr in enumerate(hours)
    ]

@router.get("/live-meters")
async def get_live_meters():
    return [
        {
            "id": "MTR-TX1-MAIN",
            "location": "Incomer Transformer 1",
            "voltage": f"{round(414.5 + random.random() * 1.5, 1)} V",
            "current": f"{int(1230 + random.random() * 20)} A",
            "power": f"{round(815 + random.random() * 10, 1)} kW",
            "powerFactor": "0.98",
            "status": "Normal",
        },
        {
            "id": "MTR-TX2-MAIN",
            "location": "Incomer Transformer 2",
            "voltage": f"{round(414.0 + random.random() * 1.5, 1)} V",
            "current": f"{int(1105 + random.random() * 15)} A",
            "power": f"{round(738 + random.random() * 8, 1)} kW",
            "powerFactor": "0.97",
            "status": "Normal",
        },
        {
            "id": "MTR-SOLAR-01",
            "location": "Rooftop Solar Array A",
            "voltage": f"{round(415.8 + random.random() * 1.0, 1)} V",
            "current": f"{int(675 + random.random() * 15)} A",
            "power": f"{round(448 + random.random() * 12, 1)} kW",
            "powerFactor": "0.99",
            "status": "Generating",
        },
        {
            "id": "MTR-HVAC-CHL",
            "location": "Chiller Plant MCC",
            "voltage": f"{round(412.0 + random.random() * 1.5, 1)} V",
            "current": f"{int(475 + random.random() * 12)} A",
            "power": f"{round(308 + random.random() * 6, 1)} kW",
            "powerFactor": "0.94",
            "status": "Normal",
        },
    ]
