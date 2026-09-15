import random
from fastapi import APIRouter

router = APIRouter(prefix="/v1/renewable", tags=["Renewable"])

@router.get("/summary")
async def get_renewable_summary():
    jitter = (random.random() - 0.5) * 100
    solar_today = round(18420 + jitter, 1)
    bess_soc = max(10, min(100, int(78 + (random.random() - 0.5) * 3)))
    clean_mix = round(38.4 + (random.random() - 0.5) * 1.2, 1)
    export_kwh = round(2140 + jitter * 0.1, 1)
    offset_co2 = round(solar_today * 0.00077, 1)

    return {
        "solar_generation_kwh": solar_today,
        "battery_soc_pct": bess_soc,
        "battery_capacity_mwh": 1.2,
        "clean_energy_share_pct": clean_mix,
        "grid_exported_kwh": export_kwh,
        "export_credit_inr": round(export_kwh * 4.5, 2),
        "co2_offset_tco2e": offset_co2,
        "tree_equivalent": int(offset_co2 * 45),
    }

@router.get("/inverters")
async def get_inverter_status():
    return [
        {"id": "INV-ROOF-01", "zone": "Zone A (Main Hall)", "dc": f"{round(248 + random.random(), 1)} kW", "ac": f"{round(244 + random.random(), 1)} kW", "eff": "98.3%", "mppt": "740 V", "yield": "3,120 kWh", "status": "Optimal"},
        {"id": "INV-ROOF-02", "zone": "Zone B (Warehouse)", "dc": f"{round(250 + random.random(), 1)} kW", "ac": f"{round(246 + random.random(), 1)} kW", "eff": "98.3%", "mppt": "742 V", "yield": "3,180 kWh", "status": "Optimal"},
        {"id": "INV-ROOF-03", "zone": "Zone C (Assembly)", "dc": f"{round(235 + random.random(), 1)} kW", "ac": f"{round(230 + random.random(), 1)} kW", "eff": "98.0%", "mppt": "732 V", "yield": "2,980 kWh", "status": "Optimal"},
        {"id": "INV-FARM-01", "zone": "Ground Array West", "dc": f"{round(252 + random.random(), 1)} kW", "ac": f"{round(248 + random.random(), 1)} kW", "eff": "98.4%", "mppt": "750 V", "yield": "3,240 kWh", "status": "Optimal"},
        {"id": "INV-FARM-02", "zone": "Ground Array East", "dc": f"{round(251 + random.random(), 1)} kW", "ac": f"{round(247 + random.random(), 1)} kW", "eff": "98.3%", "mppt": "748 V", "yield": "3,220 kWh", "status": "Optimal"},
        {"id": "INV-BESS-01", "zone": "BESS Bi-directional", "dc": f"{round(180 + random.random(), 1)} kW", "ac": f"{round(176 + random.random(), 1)} kW", "eff": "98.2%", "mppt": "800 V", "yield": "2,680 kWh", "status": "Standby"},
    ]
