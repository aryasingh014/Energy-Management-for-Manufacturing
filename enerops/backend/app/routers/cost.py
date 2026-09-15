import random
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1/cost", tags=["Cost"])

# In-memory applied opportunities state
applied_opportunities = set()

class OpportunityApply(BaseModel):
    opportunity_id: str

@router.get("/summary")
async def get_cost_summary():
    return {
        "total_cost": 866120,
        "cost_per_unit": 2.25,
        "peak_demand_cost": 420000,
        "off_peak_cost": 280000,
        "fixed_charges": 166120,
        "demand_utilization_pct": 96.0,
        "applied_opportunities": list(applied_opportunities),
    }

@router.get("/trend")
async def get_cost_trend():
    days = ["6 Sep", "7 Sep", "8 Sep", "9 Sep", "10 Sep", "11 Sep", "12 Sep"]
    costs = [3.5, 2.4, 1.9, 2.8, 2.3, 1.8, 2.5]
    rates = [2.35, 2.15, 2.10, 2.25, 2.05, 1.95, 2.25]
    return [
        {"day": d, "cost": costs[i], "costPerUnit": rates[i]}
        for i, d in enumerate(days)
    ]

@router.post("/apply-opportunity")
async def apply_opportunity(body: OpportunityApply):
    applied_opportunities.add(body.opportunity_id)
    return {
        "status": "success",
        "opportunity_id": body.opportunity_id,
        "message": f"Optimization action {body.opportunity_id} applied successfully.",
        "applied_count": len(applied_opportunities),
    }
