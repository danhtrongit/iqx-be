from typing import Generator
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI routes to get a database session.
    
    Usage in FastAPI route:
    ```
    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        items = crud.get_items(db)
        return items
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 