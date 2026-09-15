import random
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/machines", tags=["Machines"])

machines_state = [
    {"id": "CNC-101", "type": "CNC Milling", "area": "Shop 1", "status": "Running", "base_load": 84, "base_kw": 54.2, "energy": 284, "health": "98%"},
    {"id": "CNC-104", "type": "CNC Turning", "area": "Shop 1", "status": "Running", "base_load": 92, "base_kw": 68.5, "energy": 412, "health": "92%"},
    {"id": "PRS-201", "type": "Hydraulic Press", "area": "Press Shop", "status": "Running", "base_load": 78, "base_kw": 145.0, "energy": 890, "health": "95%"},
    {"id": "WLD-302", "type": "Robotic Welder", "area": "Welding", "status": "Running", "base_load": 65, "base_kw": 32.0, "energy": 198, "health": "91%"},
    {"id": "PNT-401", "type": "Curing Oven", "area": "Paint Shop", "status": "Idle", "base_load": 18, "base_kw": 12.4, "energy": 85, "health": "88%"},
    {"id": "CMP-01", "type": "Air Compressor", "area": "Utilities", "status": "Running", "base_load": 88, "base_kw": 92.0, "energy": 620, "health": "96%"},
    {"id": "CHL-02", "type": "Central Chiller", "area": "HVAC", "status": "Offline", "base_load": 0, "base_kw": 0.0, "energy": 0, "health": "74%"},
]

@router.get("/summary")
async def get_machines_summary():
    running = sum(1 for m in machines_state if m["status"] == "Running")
    idle = sum(1 for m in machines_state if m["status"] == "Idle")
    offline = sum(1 for m in machines_state if m["status"] == "Offline")
    return {
        "total_machines": 128,
        "running": 102,
        "idle": 18,
        "offline": 8,
        "total_energy_kwh": 18420,
        "avg_load_pct": round(72.4 + (random.random() - 0.5) * 1.5, 1),
        "alerts_count": 6,
    }

@router.get("/list")
async def get_machines_list():
    result = []
    for m in machines_state:
        jitter = (random.random() - 0.5) * 2 if m["status"] != "Offline" else 0
        current_kw = max(0, round(m["base_kw"] + jitter, 1))
        current_load = max(0, min(100, int(m["base_load"] + jitter)))
        result.append({
            "id": m["id"],
            "type": m["type"],
            "area": m["area"],
            "status": m["status"],
            "load": f"{current_load}%",
            "power": f"{current_kw} kW",
            "energy": f"{m['energy']} kWh",
            "health": m["health"],
        })
    return result

@router.get("/telemetry/{machine_id}")
async def get_machine_telemetry(machine_id: str):
    hours = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
    base_kw = 68.5 if machine_id == "CNC-104" else 50.0
    return {
        "machine_id": machine_id,
        "current_load": "92%",
        "temperature": f"{round(41.5 + random.random(), 1)}°C",
        "vibration": f"{round(1.75 + random.random() * 0.1, 1)} mm/s",
        "health_index": 92,
        "timeseries": [
            {
                "time": hr,
                "kw": round(base_kw * (0.6 + 0.4 * random.random()), 1),
                "temp": round(38 + random.random() * 8, 1),
            }
            for hr in hours
        ],
    }
