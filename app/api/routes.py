from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.models import ChangeRequest, ImpactReport
from app.services.impact_service import ImpactService

router = APIRouter(prefix="/api", tags=["api"])


def get_service(db: Session = Depends(get_db)) -> ImpactService:
    return ImpactService(db)


@router.post("/impact/sample/{sample_id}", response_model=ImpactReport, status_code=status.HTTP_201_CREATED)
def run_sample(sample_id: str, service: ImpactService = Depends(get_service)) -> ImpactReport:
    try:
        return service.run_sample(sample_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Sample not found") from exc


@router.post("/impact/upload", response_model=ImpactReport, status_code=status.HTTP_201_CREATED)
async def run_upload(file: UploadFile = File(...), service: ImpactService = Depends(get_service)) -> ImpactReport:
    payload = await file.read()
    try:
        import json

        data = json.loads(payload.decode("utf-8"))
        change = ChangeRequest.model_validate(data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid change request JSON") from exc
    return service.run_change(change)


@router.get("/impact/{report_id}", response_model=ImpactReport)
def get_report(report_id: str, service: ImpactService = Depends(get_service)) -> ImpactReport:
    report = service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
