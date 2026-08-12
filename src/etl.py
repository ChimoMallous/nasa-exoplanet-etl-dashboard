import pandas as pd
import sqlite3
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY = (
        "SELECT pl_name,hostname,disc_year,disc_pubdate,discoverymethod,disc_facility "
        "FROM ps WHERE default_flag = 1"
)
DB_PATH = str(PROJECT_ROOT / "exoplanet_db")

def extract():
    """
    Sends a POST request to the NASA Exoplanet Archive TAP API
    and retrieves confirmed exoplanet data in JSON format.
    -
    Returns:
        list: Raw JSON response as a list of dicts, or None if the request fails.
    """
    try:
        response = requests.post(
            BASE_URL,
            data={
                "REQUEST": "doQuery",
                "LANG": "ADQL",
                "FORMAT": "json",
                "QUERY": QUERY
            }, timeout=30
        )
        response.raise_for_status()
        logger.info(f"Extraction successful. {len(response.json())} records retrieved.")
        return response.json()
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return None

def transform(r_data):
    """
    Converts raw JSON data into a cleaned, typed Pandas DataFrame.
    -
    Args:
        r_data (list): Raw JSON response from extract().
    -
    Returns:
        DataFrame: Cleaned exoplanet records, or None if input is empty.
    """
    if not r_data:
        logger.warning("No data to transform.")
        return None
    df = pd.DataFrame([{
        "name": p.get("pl_name"),
        "host_name": p.get("hostname"),
        "discovery_year": p.get("disc_year"),
        "discovery_pubdate": p.get("disc_pubdate"),
        "discovery_method": p.get("discoverymethod"),
        "discovery_facility": p.get("disc_facility")
    } for p in r_data])
    for col in ["name", "host_name", "discovery_pubdate", "discovery_method", "discovery_facility"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)
    df["discovery_year"] = pd.to_numeric(df["discovery_year"], errors="coerce").astype("Int64")
    logger.info(f"Transformation successful. {len(df)} records available")
    return df

def validate(df):
    """
    Cleans and validates exoplanet records. Records missing a planet name are dropped
    because a nameless record cannot be counted, deduplicated, or displayed. 
    Implausible discovery years are cleared to null rather than dropped, since a 
    bad year is a bad field, not a bad planet - the record still represents a
    confirmed discovery. Uniqueness is enforced upstream by the `default_flag = 1`
    filter in QUERY; the duplicate check here is a regression guard.
    -
    Args:
        df (DataFrame): Transformed exoplanet records from transform().
    -
    Returns:
        DataFrame: Validated exoplanet records, or None if input is empty.
    """
    if df is None or df.empty:
        logger.warning("No data to validate.")
        return None
    df = df.copy()
    initial_count = len(df)

    df = df.dropna(subset=["name"])

    implausible = df["discovery_year"].notna() & ((df["discovery_year"] < 1900) | (df["discovery_year"] > 2100))

    if implausible.any():
        logger.warning(f"{int(implausible.sum())} records had an implausible discovery year - year cleared, records kept.")
        df.loc[implausible, "discovery_year"] = pd.NA

    dupes = int(df["name"].duplicated().sum())
    if dupes:
        logger.warning(f"{dupes} duplicate planet names found after extraction - check default_flag in QUERY")
        df = df.drop_duplicates(subset=["name"], keep="first")

    final_count = len(df)
    if final_count < initial_count:
        logger.info(f"Validation successful. Removed {initial_count - final_count} records.")
    else:
        logger.info("Validation successful. No records removed.")
    return df

def load_to_db(df): 
    """
    Loads a transformed and validated DataFrame into a SQLite database.
    Replaces the existing table on each run to keep data current with API.
    -
    Args:
        df (DataFrame): Validated exoplanet records from transform().
    -
    Returns:
        DataFrame: The validated exoplanet records that were loaded, or None if load fails.
    """
    if df is None or df.empty:
        logger.warning("No data to load.")
        return None
    try:
        conn = sqlite3.connect(DB_PATH) 
        try:
            df.to_sql(
                "exoplanets", 
                conn, 
                if_exists = "replace", # Replace table on each run to stay current with the API
                index=False 
            )
        finally:
            conn.close() 
        logger.info(f"Load successful. {len(df)} records saved to database.")
        return df
    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise

