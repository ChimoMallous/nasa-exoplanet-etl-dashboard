import pandas as pd
import sqlite3
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY = "SELECT pl_name,hostname,disc_year,releasedate,discoverymethod,disc_facility FROM ps"
DB_PATH = "exoplanet_db"

def extract():
    try:
        response = requests.post(
            BASE_URL,
            data={
                "REQUEST": "doQuery",
                "LANG": "ADQL",
                "FORMAT": "json",
                "QUERY": QUERY
            }, 
            timeout=30
        )
        response.raise_for_status()
        logger.info(f"Extraction successful. {len(response.json())} records retrieved.")
        return response.json()
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return None

def transform(r_data):
    if not r_data:
        logger.warning("No data to transform.")
        return None
    df = pd.DataFrame([{
        "name": p.get("pl_name"),
        "host_name": p.get("hostname"),
        "discovery_year": p.get("disc_year"),
        "discovery_date": p.get("releasedate"),
        "discovery_method": p.get("discoverymethod"),
        "discovery_facility": p.get("disc_facility")
    } for p in r_data])
    for col in ["name", "host_name", "discovery_year", "discovery_date", "discovery_method", "discovery_facility"]:
        df[col] = df[col].where(df[col].notnull(), None)
    for col in ["name", "host_name", "discovery_method", "discovery_facility"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)
    df["discovery_year"] = pd.to_numeric(df["discovery_year"], errors="coerce").astype("Int64")
    df["discovery_date"] = pd.to_datetime(df["discovery_date"], errors="coerce").dt.date
    logger.info(f"Transformation successful. {len(df)} records available")
    return df

def validate(df):
    if df is None or df.empty:
        logger.warning("No data to validate.")
        return None
    df = df.copy()
    initial_count = len(df)
    df = df.dropna(subset=["name"])
    df = df[(df["discovery_year"].isna()) | ((df["discovery_year"] >= 1900) & (df["discovery_year"] <= 2100))]
    df = df.drop_duplicates(subset=["name"])
    final_count = len(df)
    if final_count < initial_count:
        logger.info(f"Validation successful. Removed {initial_count - final_count} records.")
    else:
        logger.info("Validation successful. No records removed.")
    return df

def load_to_db(df):
    if df is None or df.empty:
        logger.warning("No data to load.")
        return
    try:
        df = validate(df)
        if df is None or df.empty:
            logger.warning("No valid data to load after validation.")
            return
        conn = sqlite3.connect(DB_PATH) # Create connection to database
        df.to_sql(
            "exoplanets", # Store dataframe as SQL table
            conn, # Make connection to database
            if_exists ="replace", # Delete old table and create new table 
            index=False # Prevents creation of index column
        )
        conn.close() # Close connection
        logger.info(f"Load successful. {len(df)} records saved to database.")
        return df
    except Exception as e:
        logger.error(f"Load failed: {e}")

