from collections.abc import Generator
from typing import Annotated
from storage.sql.db import SessionLocal
from sqlalchemy.orm import Session

from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
