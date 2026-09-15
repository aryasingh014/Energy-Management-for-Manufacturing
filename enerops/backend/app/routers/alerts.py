from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/alerts", tags=["Alerts"])

class AlertItem(BaseModel):
    id: str
    title: str
    area: str
    time: str
    severity: str
    desc: str
    status: str # "Active", "Acknowledged", "Resolved"

# In-memory alerts store
ALERTS_DB = [
    {
        "id": "ALT-1001",
        "title": "Peak Demand Limit Approaching 4.82 MW (96.4%)",
        "area": "Substation Incomer 1",
        "time": "5 min ago",
        "severity": "Critical",
        "desc": "Current draw is 4.82 MW against 5.0 MW contracted limit. Penalty threshold starts at 4.90 MW.",
        "status": "Active",
    },
    {
        "id": "ALT-1002",
        "title": "Press Line 03 Power Draw Exceeded Baseline (+38%)",
        "area": "Shop Floor 2 • Press Shop",
        "time": "32 min ago",
        "severity": "Warning",
        "desc": "Energy consumption spiked unexpectedly during tooling changeover.",
        "status": "Active",
    },
    {
        "id": "ALT-1003",
        "title": "CNC-104 Standby Coolant Pump Continuous Run",
        "area": "Shop Floor 1 • CNC Cell",
        "time": "1 hour ago",
        "severity": "Warning",
        "desc": "Machine is idle but drawing 8.2 kW auxiliary load continuously.",
        "status": "Active",
    },
]

@router.get("/list")
async def get_alerts():
    active_count = sum(1 for a in ALERTS_DB if a["status"] != "Resolved")
    critical_count = sum(1 for a in ALERTS_DB if a["status"] != "Resolved" and a["severity"] == "Critical")
    warning_count = sum(1 for a in ALERTS_DB if a["status"] != "Resolved" and a["severity"] == "Warning")
    return {
        "active_count": active_count,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "avg_resolution_time_mins": 14.2,
        "alerts": ALERTS_DB,
    }

@router.post("/acknowledge/{alert_id}")
async def acknowledge_alert(alert_id: str):
    for a in ALERTS_DB:
        if a["id"] == alert_id:
            a["status"] = "Acknowledged"
            return {"status": "success", "alert": a}
    return {"status": "not_found"}

@router.post("/resolve/{alert_id}")
async def resolve_alert(alert_id: str):
    for a in ALERTS_DB:
        if a["id"] == alert_id:
            a["status"] = "Resolved"
            return {"status": "success", "alert": a}
    return {"status": "not_found"}
