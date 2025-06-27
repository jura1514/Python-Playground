from sqlalchemy.orm import Session
from storage.sql.alert_db import AlertDB
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def create_alert(session: Session, alert: AlertDB) -> AlertDB:
    """
    Create a new alert if id isn't already taken.

    :param Session session: SQLAlchemy database session.
    :param AlertDB alert: New alert record to create.

    :return: Optional[AlertDB]
    """
    try:
        existing_alert = session.query(AlertDB).filter(AlertDB.id == alert.id).first()
        if existing_alert is None:
            session.add(alert)
            session.commit()
            print(f"Created alert: {alert}")
        else:
            print(f"Alert already exists in database: {existing_alert}")
        return session.query(AlertDB).filter(AlertDB.id == alert.id).first()
    except IntegrityError as e:
        print(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        print(f"Unexpected error when creating alert: {e}")
        raise e
    except Exception as e:
        print(f"Unexpected error when creating alert: {e}")
        raise e


def delete_alert(session: Session, alert_id: int) -> bool:
    """
    Delete an alert by its ID.

    :param Session session: SQLAlchemy database session.
    :param int alert_id: ID of the alert to delete.

    :return: bool
    """
    alert = session.query(AlertDB).filter_by(id=alert_id).first()
    if alert:
        session.delete(alert)
        session.commit()
        print(f"Deleted alert with ID: {alert_id}")
        return True
    print(f"Alert with ID {alert_id} not found")
    return False


def update_alert(session: Session, alert_id: int, target_price: float = None, symbol: str = None, convert: str = None) -> AlertDB:
    """
    Update an existing alert's target_price, symbol, and convert by id.

    :param Session session: SQLAlchemy database session.
    :param int alert_id: ID of the alert to update.
    :param float target_price: New target price for the alert.
    :param str symbol: New symbol for the alert.
    :param str convert: New convert value for the alert.

    :return: Optional[AlertDB]
    """
    alert = session.query(AlertDB).filter_by(id=alert_id).first()
    if not alert:
        print(f"Alert with ID {alert_id} not found")
        return None
    if target_price is not None:
        alert.target_price = target_price
    if symbol is not None:
        alert.symbol = symbol
    if convert is not None:
        alert.convert = convert
    session.commit()
    session.refresh(alert)
    print(f"Updated alert: {alert}")
    return alert
