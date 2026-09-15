from fastapi import APIRouter, Response
from typing import List

router = APIRouter(prefix="/v1/reports", tags=["Reports"])

REPORTS_CATALOG = [
    {
        "id": "rep-01",
        "name": "Monthly Plant 1 Energy Audit & Tariff Reconciliation",
        "type": "Cost & Energy",
        "freq": "Monthly",
        "date": "01 Sep 2025",
        "size": "3.4 MB",
    },
    {
        "id": "rep-02",
        "name": "Executive GHG Scope 1, 2 & 3 Emissions Statement",
        "type": "Sustainability",
        "freq": "Quarterly",
        "date": "31 Aug 2025",
        "size": "2.1 MB",
    },
    {
        "id": "rep-03",
        "name": "Machine SEC & OEE Benchmarking Performance Sheet",
        "type": "Production",
        "freq": "Weekly",
        "date": "08 Sep 2025",
        "size": "1.8 MB",
    },
    {
        "id": "rep-04",
        "name": "Solar PV Yield & BESS Dispatch Verification Log",
        "type": "Renewable",
        "freq": "Daily",
        "date": "12 Sep 2025",
        "size": "840 KB",
    },
]

@router.get("/list")
async def get_reports_list():
    return {
        "generated_count": 48,
        "compliance_status": "100% On-Track",
        "audit_readiness": "Grade A+",
        "reports": REPORTS_CATALOG,
    }

@router.get("/download/{report_id}")
async def download_report(report_id: str, format: str = "csv"):
    report_name = next((r["name"] for r in REPORTS_CATALOG if r["id"] == report_id), "EnerOps_Report")
    
    if format.lower() == "csv":
        csv_content = f"EnerOps Industrial Energy & Telemetry Report\nReport: {report_name}\nGenerated: 2025-09-12 10:24:00\n\nTimestamp,Asset,Metric,Value,Unit\n2025-09-12 08:00,Plant 1,Total Energy,4820,kW\n2025-09-12 09:00,Press Line 03,Power,842,kW\n2025-09-12 10:00,Solar Array A,Generation,450,kW\n2025-09-12 11:00,CNC-104,Load Ratio,92,%\n"
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{report_name.replace(" ", "_")}.csv"'}
        )
    else:
        content = f"EnerOps Automated Audit Document\n{report_name}\nAudited by Admin (Energy Manager)\nStatus: Approved"
        return Response(
            content=content,
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{report_name.replace(" ", "_")}.txt"'}
        )
