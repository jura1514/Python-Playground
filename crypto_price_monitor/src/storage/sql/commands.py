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
