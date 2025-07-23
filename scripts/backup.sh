#!/bin/bash

# This script performs a backup of the PostgreSQL database.
# It reads database connection details from a .env file in the project root.

# Set the path to the .env file
ENV_FILE="$(dirname "$0")/../.env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Load environment variables from .env file
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Check for required environment variables
if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_SERVER" ] || [ -z "$POSTGRES_PORT" ]; then
    echo "Error: One or more required environment variables are not set in .env file."
    echo "Please set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_SERVER, and POSTGRES_PORT."
    exit 1
fi

# Set backup directory and filename
BACKUP_DIR="$(dirname "$0")/../backups"
mkdir -p "$BACKUP_DIR"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/${POSTGRES_DB}_${DATE}.sql"

# Run pg_dump
echo "Backing up database '$POSTGRES_DB' to $BACKUP_FILE..."
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h $POSTGRES_SERVER -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -f "$BACKUP_FILE" --schema=public --no-owner --no-privileges

# Check if pg_dump was successful
if [ $? -eq 0 ]; then
  echo "Backup successful!"
else
  echo "Error: Backup failed."
  exit 1
fi

echo "Backup file is located at: $BACKUP_FILE" 