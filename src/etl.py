import pandas as pd
import sqlite3
import requests
import logging

logger = logging.getLogger(__name__)

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=select+pl_name,disc_year,discoverymethod,disc_facility+from+ps"

def extract(url):
    try:
        response = requests.get(url, timeout=30)
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
        "discovery_year": p.get("disc_year"),  
        "discovery_method": p.get("discoverymethod"),
        "discovery_facility": p.get("disc_facility")
    } for p in r_data])
    for col in ["name", "discovery_year", "discovery_method", "discovery_facility"]:
        df[col] = df[col].where(df[col].notnull(), None)
    for col in ["name", "discovery_method", "discovery_facility"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)
    df["discovery_year"] = pd.to_numeric(df["discovery_year"], errors="coerce").astype("Int64")
    logger.info(f"Transformation successful. {len(df)} records available")
    return df

def validate(df):
    if df is None or df.empty:
        logger.warning("No data to validate.")
        return None
    df = df.copy()
    initial_count = len(df)
    df = df.dropna(subset=["name", "discovery_year"])
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
        conn = sqlite3.connect("exoplanet_db") # Create connection to database
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

