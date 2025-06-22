from typing import Any
from fastapi import APIRouter
from models.models import AlertCreate, AlertCreated
from api.deps import SessionDep
from storage.sql.alert_db import AlertDB
from storage.sql.commands import create_alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/", response_model=AlertCreated, status_code=201)
def create_item(*, session: SessionDep, alert_create: AlertCreate) -> Any:
    """
    Create new alert.
    """
    new_alert = AlertDB(
        symbol=alert_create.symbol,
        condition=alert_create.condition,
        target_price=alert_create.target_price,
        convert=alert_create.convert,
    )
    create_alert(session, new_alert)
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
