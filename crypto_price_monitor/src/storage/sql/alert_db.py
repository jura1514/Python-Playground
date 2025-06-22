from sqlalchemy import Boolean, Column, Float, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from models.models import TargetPriceCondition, Symbol, Convert

Base = declarative_base()


class AlertDB(Base):
    __tablename__ = "alert"
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_price = Column(Float, nullable=False)
    condition = Column(SAEnum(TargetPriceCondition), nullable=False)
    symbol = Column(SAEnum(Symbol), nullable=False)
    convert = Column(SAEnum(Convert), nullable=False)
    is_notified = Column(Boolean, default=False)
