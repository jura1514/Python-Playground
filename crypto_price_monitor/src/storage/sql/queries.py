from typing import List, Optional

from requests import Session
from sqlalchemy import Engine

from storage.sql.alert_db import AlertDB


def get_alerts(session: Session, is_notified=False) -> List[AlertDB]:
    """
    Fetch all not notified alerts.

    :param Session session: SQLAlchemy database session.

    :return: List[AlertDB]
    """
    return session.query(AlertDB).filter(AlertDB.is_notified == is_notified).all()
