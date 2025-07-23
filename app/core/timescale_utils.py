from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


def create_hypertable(
    db: Session,
    table_name: str,
    time_column: str = "created_at",
    chunk_time_interval: str = "7 days",
    if_not_exists: bool = True,
    schema: Optional[str] = None,
) -> bool:
    """
    Convert a regular PostgreSQL table to a TimescaleDB hypertable.
    
    Args:
        db: SQLAlchemy database session
        table_name: Name of the table to convert
        time_column: Name of the timestamp column to use as the time index
        chunk_time_interval: Interval for chunks (e.g., '7 days', '1 month')
        if_not_exists: Add IF NOT EXISTS clause to prevent errors if already a hypertable
        schema: Database schema name (optional)
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Construct the SQL query
        sql = f"""
        SELECT create_hypertable(
            '{schema + "." if schema else ""}{table_name}', 
            '{time_column}',
            chunk_time_interval => interval '{chunk_time_interval}',
            if_not_exists => {'TRUE' if if_not_exists else 'FALSE'}
        )
        """
        
        # Execute the query
        db.execute(text(sql))
        db.commit()
        
        logger.info(f"Successfully created hypertable for {table_name}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create hypertable for {table_name}: {e}")
        return False


def add_compression_policy(
    db: Session,
    table_name: str,
    compress_after: str = "30 days",
    schema: Optional[str] = None,
    segment_by: Optional[str] = None,
) -> bool:
    """
    Add automatic compression policy to a hypertable.
    
    Args:
        db: SQLAlchemy database session
        table_name: Name of the hypertable
        compress_after: When to compress data (e.g., '30 days')
        schema: Database schema name (optional)
        segment_by: Column to use for segmenting data (optional)
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Enable compression on the table first
        enable_sql = f"""
        ALTER TABLE {schema + "." if schema else ""}{table_name} 
        SET (timescaledb.compress = true
        {f", timescaledb.compress_segmentby = '{segment_by}'" if segment_by else ""}
        )
        """
        
        # Add compression policy
        policy_sql = f"""
        SELECT add_compression_policy(
            '{schema + "." if schema else ""}{table_name}', 
            INTERVAL '{compress_after}'
        )
        """
        
        # Execute the queries
        db.execute(text(enable_sql))
        db.execute(text(policy_sql))
        db.commit()
        
        logger.info(f"Successfully added compression policy to {table_name}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add compression policy to {table_name}: {e}")
        return False


def create_continuous_aggregate(
    db: Session,
    view_name: str,
    hypertable_name: str,
    time_bucket: str,
    aggregates: List[str],
    where_clause: Optional[str] = None,
    schema: Optional[str] = None,
    group_by_columns: Optional[List[str]] = None,
    refresh_policy_start: Optional[str] = None,
    refresh_policy_interval: Optional[str] = None,
) -> bool:
    """
    Create a continuous aggregate view for a hypertable.
    
    Args:
        db: SQLAlchemy database session
        view_name: Name of the continuous aggregate view to create
        hypertable_name: Name of the hypertable to aggregate
        time_bucket: Size of the time bucket (e.g., '1 hour', '1 day')
        aggregates: List of aggregate expressions (e.g., ['AVG(temperature)', 'MAX(humidity)'])
        where_clause: Optional WHERE clause to filter data
        schema: Database schema name (optional)
        group_by_columns: Additional columns to group by
        refresh_policy_start: Start offset for refresh policy (e.g., '1 day')
        refresh_policy_interval: Interval for refresh policy (e.g., '1 hour')
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Format schema names
        schema_prefix = f"{schema}." if schema else ""
        
        # Build the aggregate list
        agg_list = ", ".join(aggregates)
        
        # Build GROUP BY clause
        group_by = []
        group_by.append(f"time_bucket('{time_bucket}', time)")
        if group_by_columns:
            group_by.extend(group_by_columns)
        group_by_clause = ", ".join(group_by)
        
        # Build the WHERE clause
        where_sql = f"WHERE {where_clause}" if where_clause else ""
        
        # Construct the SQL for creating the continuous aggregate
        sql = f"""
        CREATE MATERIALIZED VIEW {schema_prefix}{view_name}
        WITH (timescaledb.continuous) AS
        SELECT 
            {group_by_clause},
            {agg_list}
        FROM {schema_prefix}{hypertable_name}
        {where_sql}
        GROUP BY {group_by_clause}
        """
        
        # Execute the query
        db.execute(text(sql))
        
        # Add refresh policy if specified
        if refresh_policy_start and refresh_policy_interval:
            policy_sql = f"""
            SELECT add_continuous_aggregate_policy('{schema_prefix}{view_name}',
                start_offset => INTERVAL '{refresh_policy_start}',
                end_offset => INTERVAL '1 minute',
                schedule_interval => INTERVAL '{refresh_policy_interval}'
            )
            """
            db.execute(text(policy_sql))
        
        db.commit()
        
        logger.info(f"Successfully created continuous aggregate {view_name}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create continuous aggregate {view_name}: {e}")
        return False 