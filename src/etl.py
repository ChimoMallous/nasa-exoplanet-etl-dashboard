import pandas as pd
import sqlite3
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=select+pl_name,disc_year,discoverymethod,pl_rade,hostname+from+ps"

def extract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Extraction successful. {len(response.json())} records retrieved.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Extraction failed: {e}")
        return None

def transform(r_data):
    if not r_data:
        logger.warning("No data to transform")
        return []
    t_data = []
    for p in r_data:
        t_data.append({
            "name": p.get("pl_name"),
            "discovery_year": p.get("disc_year"),  
            "discovery_method": p.get("discoverymethod"),
            "planet_radius": p.get("pl_rade"),
            "star_name": p.get("hostname")
        }) 
    logger.info(f"Transformation successful. {len(t_data)} records transformed.")
    return t_data

def load_to_db(t_data):
    if not t_data:
        logger.warning("No data to load.")
        return
    try:
        df = pd.DataFrame(t_data)
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

