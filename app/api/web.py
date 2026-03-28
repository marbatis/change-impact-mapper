from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.models import ChangeRequest
from app.services.impact_service import ImpactService

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def get_service(db: Session = Depends(get_db)) -> ImpactService:
    return ImpactService(db)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, service: ImpactService = Depends(get_service)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"samples": service.sample_ids(), "result": None},
    )


@router.post("/run", response_class=HTMLResponse)
def run_custom(
    request: Request,
    change_id: str = Form(...),
    target_node: str = Form(...),
    change_type: str = Form(...),
    rollout_window: str = Form(...),
    risk_level: str = Form(...),
    notes: str = Form(""),
    service: ImpactService = Depends(get_service),
) -> HTMLResponse:
    report = service.run_change(
        ChangeRequest(
            change_id=change_id,
            target_node=target_node,
            change_type=change_type,
            rollout_window=rollout_window,
            risk_level=risk_level,
            notes=notes,
        )
    )
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"samples": service.sample_ids(), "result": report},
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request, service: ImpactService = Depends(get_service)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"rows": service.history()},
    )


@router.get("/graph/{report_id}", response_class=HTMLResponse)
def graph_view(report_id: str, request: Request, service: ImpactService = Depends(get_service)) -> HTMLResponse:
    report = service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return templates.TemplateResponse(
        request=request,
        name="graph.html",
        context={"report": report},
    )
