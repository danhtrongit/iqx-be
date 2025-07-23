from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import logging

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with appropriate parameters
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Check connection before using from pool
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=10,        # Maximum number of connections in the pool
    max_overflow=20,     # Maximum number of connections that can be created beyond pool_size
    echo=False,          # Set to True to log all SQL queries (useful for debugging)
    connect_args={
        "options": f"-c search_path={settings.POSTGRES_SCHEMA}",
        "application_name": "iqx_backend",  # Helps identify the application in pg_stat_activity
    },
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Metadata object for migrations
metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def setup_timescale() -> None:
    """Configure TimescaleDB if enabled."""
    if not settings.TIMESCALEDB_ENABLED:
        return
    
    # Import here to avoid dependency issues when TimescaleDB is not used
    try:
        with engine.begin() as connection:
            # Check if the TimescaleDB extension is already installed
            result = connection.execute(
                text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'timescaledb')")
            ).scalar()
            
            if not result:
                logger.info("Creating TimescaleDB extension")
                # Create TimescaleDB extension
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE"))
    except Exception as e:
        logger.error(f"Failed to setup TimescaleDB: {e}")
        # We don't raise here since the application might work without TimescaleDB
        # Just with reduced functionality 