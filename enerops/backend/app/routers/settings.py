import random
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/v1/settings", tags=["Settings"])

SETTINGS_DB = {
    "plant_name": "Plant 1 - Manufacturing Hub",
    "contract_demand_mw": 5.0,
    "timezone": "Asia/Kolkata (+05:30)",
    "target_baseline_mwh": "22,500 MWh",
    "tariff": {
        "peak_rate": 8.50,
        "off_peak_rate": 4.20,
        "demand_charge": 420.0,
        "fixed_charge": 120000.0,
    },
    "mqtt_status": "Connected (broker.plant1.enerops.local:1883)",
    "modbus_gateway": "192.168.1.100:502 (34 Connected Sub-meters)",
}

PLANTS_DB = [
    {
        "id": "plant-1",
        "name": "Plant 1 - Manufacturing Hub",
        "location": "Indore, MP (Central Hub)",
        "contract_demand_mw": 5.0,
        "current_demand_mw": 4.82,
        "active_machines": 18,
        "status": "Running (Optimal)",
        "shift": "Day Shift (06:00 - 14:00)",
        "timezone": "Asia/Kolkata (+05:30)",
    },
    {
        "id": "plant-2",
        "name": "Plant 2 - Assembly Facility",
        "location": "Pune, MH (Auto Corridor)",
        "contract_demand_mw": 3.5,
        "current_demand_mw": 2.91,
        "active_machines": 12,
        "status": "Running (Normal)",
        "shift": "Day Shift (06:00 - 14:00)",
        "timezone": "Asia/Kolkata (+05:30)",
    },
    {
        "id": "plant-3",
        "name": "Plant 3 - Solar & Battery Park",
        "location": "Kutch, GJ (Clean Energy)",
        "contract_demand_mw": 8.0,
        "current_demand_mw": 6.40,
        "active_machines": 24,
        "status": "Generating (Peak Solar)",
        "shift": "Continuous (24x7)",
        "timezone": "Asia/Kolkata (+05:30)",
    },
    {
        "id": "plant-4",
        "name": "Plant 4 - Precision Stamping",
        "location": "Chennai, TN (Coastal Plant)",
        "contract_demand_mw": 4.2,
        "current_demand_mw": 3.15,
        "active_machines": 14,
        "status": "Running (Normal)",
        "shift": "Day Shift (06:00 - 14:00)",
        "timezone": "Asia/Kolkata (+05:30)",
    },
]

USERS_DB = [
    {
        "id": "usr-01",
        "name": "Admin",
        "email": "admin@gmail.com",
        "role": "Energy Manager",
        "department": "Plant Engineering",
        "status": "Active",
        "last_login": "Today, 10:24 AM",
        "avatar_bg": "bg-emerald-500",
    },
    {
        "id": "usr-02",
        "name": "Vikram Malhotra",
        "email": "vikram.m@enerops.ai",
        "role": "Plant Admin",
        "department": "Operations",
        "status": "Active",
        "last_login": "Yesterday, 4:15 PM",
        "avatar_bg": "bg-blue-600",
    },
    {
        "id": "usr-03",
        "name": "Neha Sharma",
        "email": "neha.s@enerops.ai",
        "role": "ESG & Sustainability Lead",
        "department": "Corporate Sustainability",
        "status": "Active",
        "last_login": "12 Sep 2025",
        "avatar_bg": "bg-teal-500",
    },
    {
        "id": "usr-04",
        "name": "Rajesh Patel",
        "email": "rajesh.p@enerops.ai",
        "role": "Maintenance Engineer",
        "department": "Machine Maintenance",
        "status": "Active",
        "last_login": "Today, 8:00 AM",
        "avatar_bg": "bg-amber-500",
    },
    {
        "id": "usr-05",
        "name": "Amit Deshmukh",
        "email": "amit.d@enerops.ai",
        "role": "Shift Operator",
        "department": "Shop Floor 1",
        "status": "Active",
        "last_login": "Today, 6:00 AM",
        "avatar_bg": "bg-purple-500",
    },
]

WEBHOOKS_DB = [
    {
        "id": "wh-01",
        "name": "Slack Critical Incident Dispatch",
        "service": "Slack",
        "url": "https://hooks.slack.com/services/T04G.../B08X.../enerops-alerts",
        "events": ["Peak Demand > 4.8 MW", "Machine Critical Anomaly", "Power Factor < 0.90"],
        "active": True,
        "last_triggered": "5 mins ago (HTTP 200)",
        "success_rate": "100%",
    },
    {
        "id": "wh-02",
        "name": "Microsoft Teams ESG Operations",
        "service": "MS Teams",
        "url": "https://enerops.webhook.office.com/webhookb2/8942.../IncomingWebhook",
        "events": ["Daily GHG Scope 1/2 Report", "Solar Generation Target", "Net-Zero Milestone"],
        "active": True,
        "last_triggered": "Today, 6:00 AM (HTTP 200)",
        "success_rate": "99.8%",
    },
    {
        "id": "wh-03",
        "name": "WhatsApp Supervisor Dispatch",
        "service": "WhatsApp",
        "url": "https://api.twilio.com/2010-04-01/Accounts/AC89.../Messages.json",
        "events": ["Peak Demand > 4.8 MW", "Emergency Load Shedding"],
        "active": True,
        "last_triggered": "Yesterday, 2:14 PM (HTTP 200)",
        "success_rate": "100%",
    },
    {
        "id": "wh-04",
        "name": "SAP ERP Energy Cost Reconciliation",
        "service": "SAP ERP",
        "url": "https://erp.plant1.internal:8443/api/v2/cost-centers/energy-sync",
        "events": ["Monthly Tariff Reconciliation", "Shift-wise SEC Telemetry"],
        "active": True,
        "last_triggered": "01 Sep 2025 (HTTP 200)",
        "success_rate": "100%",
    },
    {
        "id": "wh-05",
        "name": "Kafka Telemetry Pipeline Stream",
        "service": "Apache Kafka",
        "url": "https://kafka-ingress.enerops.cloud:9092/topics/plant1-raw-meters",
        "events": ["Real-time 1s Meter Feeds", "Inverter Telemetry (All)"],
        "active": False,
        "last_triggered": "Paused by Admin",
        "success_rate": "99.4%",
    },
]

class UpdatePlantSettings(BaseModel):
    plant_name: str
    contract_demand_mw: float

class UpdateTariffSettings(BaseModel):
    peak_rate: float
    off_peak_rate: float
    demand_charge: float
    fixed_charge: float

class CreateUser(BaseModel):
    name: str
    email: str
    role: str
    department: str

class UpdateUserRole(BaseModel):
    role: str

class CreateWebhook(BaseModel):
    name: str
    service: str
    url: str
    events: List[str]

class SwitchPlant(BaseModel):
    plant_id: str

class CreatePlant(BaseModel):
    name: str
    location: str
    contract_demand_mw: float = 5.0
    protocol: Optional[str] = "MQTT Stream"
    endpoint: Optional[str] = "mqtt://broker.enerops.local:1883"
    timezone: Optional[str] = "Asia/Kolkata (+05:30)"

@router.get("/")
async def get_settings():
    return SETTINGS_DB

@router.get("/plants")
async def get_plants():
    return {
        "active_plant": SETTINGS_DB["plant_name"],
        "plants": PLANTS_DB,
    }

@router.post("/plants")
async def create_plant(body: CreatePlant):
    new_plant = {
        "id": f"plant-{len(PLANTS_DB) + 1}",
        "name": body.name,
        "location": body.location,
        "contract_demand_mw": body.contract_demand_mw,
        "current_demand_mw": round(body.contract_demand_mw * 0.72, 2),
        "active_machines": random.randint(10, 30),
        "status": "Running (Optimal)",
        "shift": "Day Shift (06:00 - 14:00)",
        "timezone": body.timezone or "Asia/Kolkata (+05:30)",
        "protocol": body.protocol,
        "endpoint": body.endpoint,
    }
    PLANTS_DB.append(new_plant)
    return {"status": "success", "plant": new_plant, "plants": PLANTS_DB}

@router.post("/plants/test-connection")
async def test_plant_connection(body: dict):
    # ponytail: rapid gateway verification simulation with latency response
    latency = random.randint(11, 24)
    tags_count = random.randint(18, 48)
    return {
        "status": "success",
        "latency_ms": latency,
        "tags_discovered": tags_count,
        "message": f"Connection verified ({latency}ms latency). Discovered {tags_count} live telemetry tags."
    }

@router.post("/plants/switch")
async def switch_plant(body: SwitchPlant):
    for p in PLANTS_DB:
        if p["id"] == body.plant_id:
            SETTINGS_DB["plant_name"] = p["name"]
            SETTINGS_DB["contract_demand_mw"] = p["contract_demand_mw"]
            return {"status": "success", "active_plant": p, "settings": SETTINGS_DB}
    raise HTTPException(status_code=404, detail="Plant not found")


@router.post("/plant")
async def save_plant_settings(body: UpdatePlantSettings):
    SETTINGS_DB["plant_name"] = body.plant_name
    SETTINGS_DB["contract_demand_mw"] = body.contract_demand_mw
    return {"status": "success", "settings": SETTINGS_DB}

@router.post("/tariff")
async def save_tariff_settings(body: UpdateTariffSettings):
    SETTINGS_DB["tariff"]["peak_rate"] = body.peak_rate
    SETTINGS_DB["tariff"]["off_peak_rate"] = body.off_peak_rate
    SETTINGS_DB["tariff"]["demand_charge"] = body.demand_charge
    SETTINGS_DB["tariff"]["fixed_charge"] = body.fixed_charge
    return {"status": "success", "settings": SETTINGS_DB}

# ----------------- USERS & ROLES ENDPOINTS -----------------
@router.get("/users")
async def get_users():
    return {
        "total_users": len(USERS_DB),
        "active_users": sum(1 for u in USERS_DB if u["status"] == "Active"),
        "roles_distribution": {
            "Plant Admin": sum(1 for u in USERS_DB if u["role"] == "Plant Admin"),
            "Energy Manager": sum(1 for u in USERS_DB if u["role"] == "Energy Manager"),
            "ESG Lead": sum(1 for u in USERS_DB if "ESG" in u["role"]),
            "Maintenance & Operator": sum(1 for u in USERS_DB if u["role"] in ["Maintenance Engineer", "Shift Operator"]),
        },
        "users": USERS_DB,
    }

@router.post("/users")
async def create_user(body: CreateUser):
    colors = ["bg-emerald-500", "bg-blue-600", "bg-indigo-600", "bg-teal-500", "bg-purple-600", "bg-rose-500"]
    new_user = {
        "id": f"usr-{random.randint(100, 999)}",
        "name": body.name,
        "email": body.email,
        "role": body.role,
        "department": body.department,
        "status": "Active",
        "last_login": "Invited (Pending First Login)",
        "avatar_bg": random.choice(colors),
    }
    USERS_DB.append(new_user)
    return {"status": "success", "user": new_user}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    global USERS_DB
    USERS_DB = [u for u in USERS_DB if u["id"] != user_id]
    return {"status": "success", "deleted_id": user_id}

@router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, body: UpdateUserRole):
    for u in USERS_DB:
        if u["id"] == user_id:
            u["role"] = body.role
            return {"status": "success", "user": u}
    raise HTTPException(status_code=404, detail="User not found")

# ----------------- WEBHOOKS ENDPOINTS -----------------
@router.get("/webhooks")
async def get_webhooks():
    return {
        "total_webhooks": len(WEBHOOKS_DB),
        "active_webhooks": sum(1 for w in WEBHOOKS_DB if w["active"]),
        "avg_latency_ms": 18.4,
        "delivery_rate": "99.9%",
        "webhooks": WEBHOOKS_DB,
    }

@router.post("/webhooks")
async def create_webhook(body: CreateWebhook):
    new_webhook = {
        "id": f"wh-{random.randint(10, 99)}",
        "name": body.name,
        "service": body.service,
        "url": body.url,
        "events": body.events,
        "active": True,
        "last_triggered": "Never (New Endpoint)",
        "success_rate": "100%",
    }
    WEBHOOKS_DB.append(new_webhook)
    return {"status": "success", "webhook": new_webhook}

@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: str):
    global WEBHOOKS_DB
    WEBHOOKS_DB = [w for w in WEBHOOKS_DB if w["id"] != webhook_id]
    return {"status": "success", "deleted_id": webhook_id}

@router.put("/webhooks/{webhook_id}/toggle")
async def toggle_webhook(webhook_id: str):
    for w in WEBHOOKS_DB:
        if w["id"] == webhook_id:
            w["active"] = not w["active"]
            return {"status": "success", "active": w["active"], "webhook": w}
    raise HTTPException(status_code=404, detail="Webhook not found")

@router.post("/webhooks/{webhook_id}/test")
async def test_webhook(webhook_id: str):
    for w in WEBHOOKS_DB:
        if w["id"] == webhook_id:
            latency = round(random.uniform(12.5, 28.0), 1)
            w["last_triggered"] = f"Just now (HTTP 200 • {latency}ms)"
            return {
                "status": "success",
                "http_status": 200,
                "latency_ms": latency,
                "payload_delivered": {
                    "event": "TEST_NOTIFICATION_PING",
                    "plant": "Plant 1 - Manufacturing Hub",
                    "message": "EnerOps telemetry webhook test successful.",
                },
            }
    raise HTTPException(status_code=404, detail="Webhook not found")
