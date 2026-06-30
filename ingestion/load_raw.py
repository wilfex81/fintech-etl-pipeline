import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

RAW_DATA_PATH ='data/transactions.json'



def create_raw_schema():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conn.commit()
    logging.info("Raw schema created successfully.")

def create_raw_table():
    with engine.connect() as conn:
        conn.execute(text("""CREATE TABLE IF NOT EXISTS raw.events (
            event_id            TEXT,
            event_timestamp_utc TIMESTAMP,
            event_type          TEXT,
            payload              JSONB,
            loaded_at            TIMESTAMP DEFAULT now()
        )"""))
        conn.commit()
    logging.info("Raw table created successfully.")

def load_raw_data():
    # Load the JSON data into a pandas DataFrame
    df = pd.read_json(RAW_DATA_PATH)

    # Insert the data into the raw.events table
    try:
        with engine.connect() as conn:
            for _, row in df.iterrows():
                conn.execute(text("""
                    INSERT INTO raw.events (event_id, event_timestamp_utc, event_type, payload)
                    VALUES (:EventId, :EventTimestampUtc, :EventType, :Payload)
                """), {
                    "EventId": row['EventId'],
                    "EventTimestampUtc": row['EventTimestampUtc'],
                    "EventType": row['EventType'],
                    "Payload": row['Payload']
                })
            conn.commit()
        logging.info(f"Raw data loaded successfully. Total records inserted: {len(df)}")
    except Exception as e:
        logging.error(f"Error loading raw data: {e}")
        

if __name__ == "__main__":
    create_raw_schema()
    create_raw_table()
    load_raw_data()

    logging.info("Raw data ingestion completed successfully.")