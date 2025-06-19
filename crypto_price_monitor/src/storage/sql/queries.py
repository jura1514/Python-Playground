from typing import List, Optional

from requests import Session
from sqlalchemy import Engine

from storage.sql.alert_db import AlertDB


def get_not_notified_alerts(session: Session) -> List[AlertDB]:
    """
    Fetch all not notified alerts.

    :param Session session: SQLAlchemy database session.

    :return: List[AlertDB]
    """
    return (
        session.query(AlertDB)
        .filter(AlertDB.is_notified == False)
        .all()
    )
