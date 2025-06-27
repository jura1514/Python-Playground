from typing import Any
from fastapi import APIRouter, Query, HTTPException, status
from models.models import AlertCreate, AlertCreated, AlertItem, AlertUpdate
from api.deps import SessionDep
from storage.sql.alert_db import AlertDB
from storage.sql.queries import get_alerts as db_get_alerts
from storage.sql.commands import create_alert as db_create_alert, delete_alert as db_delete_alert, update_alert as db_update_alert
from pydantic import BaseModel

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/", response_model=AlertCreated, status_code=201)
def create_alert(*, session: SessionDep, alert_create: AlertCreate) -> Any:
    """
    Create new alert.
    """
    new_alert = AlertDB(
        symbol=alert_create.symbol,
        condition=alert_create.condition,
        target_price=alert_create.target_price,
        convert=alert_create.convert,
    )
    db_create_alert(session, new_alert)
    session.refresh(new_alert)

    alert_created = AlertCreated(
        id=str(new_alert.id),
        target_price=new_alert.target_price,
        condition=new_alert.condition,
        symbol=new_alert.symbol,
        convert=new_alert.convert,
        is_notified=new_alert.is_notified,
    )
    return alert_created


@router.get("/", response_model=list[AlertItem])
def get_alerts(
    session: SessionDep,
    is_notified: bool = Query(False, description="Filter by is_notified status")
):
    """
    Get all alerts, optionally filter by is_notified.
    """
    alerts = db_get_alerts(session, is_notified=is_notified)
    return [
        AlertItem(
            id=str(a.id),
            target_price=a.target_price,
            condition=a.condition.name,
            symbol=a.symbol,
            convert=a.convert,
            is_notified=a.is_notified,
        )
        for a in alerts
    ]


@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: str, session: SessionDep):
    """
    Delete an alert by id.
    """
    deleted = db_delete_alert(session, alert_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return None


@router.put("/{alert_id}", response_model=AlertItem)
def update_alert(alert_id: str, alert_update: AlertUpdate, session: SessionDep):
    """
    Update an alert's target_price, symbol, or convert.
    """
    updated = db_update_alert(
        session,
        alert_id,
        target_price=alert_update.target_price,
        symbol=alert_update.symbol,
        convert=alert_update.convert,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return AlertItem(
        id=str(updated.id),
        target_price=updated.target_price,
        condition=updated.condition.name,
        symbol=updated.symbol,
        convert=updated.convert,
        is_notified=updated.is_notified,
    )
