import logging
from sqlalchemy.orm import Session
from app.core.timescale_utils import create_hypertable, add_compression_policy
from app.core.config import settings

logger = logging.getLogger(__name__)

def initialize_timescaledb(db: Session) -> None:
    """
    Initialize TimescaleDB features for the application.
    This should be run after initial database migration.
    
    Args:
        db: SQLAlchemy database session
    """
    if not settings.TIMESCALEDB_ENABLED:
        logger.info("TimescaleDB features are disabled. Skipping initialization.")
        return
    
    logger.info("Initializing TimescaleDB features...")
    
    # Convert sensor_data table to hypertable
    create_hypertable(
        db=db,
        table_name="sensor_data",
        time_column="created_at",
        chunk_time_interval="1 day",  # Adjust based on expected data volume
        schema=settings.POSTGRES_SCHEMA
    )
    
    # Add compression policy for sensor data (compress data older than 30 days)
    add_compression_policy(
        db=db,
        table_name="sensor_data",
        compress_after="30 days",
        schema=settings.POSTGRES_SCHEMA,
        segment_by="sensor_id"  # Segment compression by sensor for better compression ratios
    )
    
    logger.info("TimescaleDB initialization completed successfully") 