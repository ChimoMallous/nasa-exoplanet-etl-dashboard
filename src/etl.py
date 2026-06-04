import pandas as pd
import sqlite3
import requests


url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=select+pl_name,disc_year,discoverymethod,pl_rade,hostname+from+ps"

def extract(url):
    response = requests.get(url)
    if response.status_code == 200:
        r_data = response.json()
        print("Data extraction successful.")
        return r_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def transform(r_data):
    if not r_data:
        print("No data to transform.")
        return []
    else:
        t_data = []
        for p in r_data:
            t_data.append({
                "name": p.get("pl_name"),
                "discovery_year": p.get("disc_year"),  
                "discovery_method": p.get("discoverymethod"),
                "planet_radius": p.get("pl_rade"),
                "star_name": p.get("hostname")
            }) 
        print("Data transformation successful.")
        return t_data

def load_to_db(t_data):
    if t_data is None:
        print("No transformed data to load.")
    else:
        df = pd.DataFrame(t_data)
        conn = sqlite3.connect("exoplanet_db") # Create connection to database
        df.to_sql(
            "exoplanets", # Store dataframe as SQL table
            conn, # Make connection to database
            if_exists ="replace", # Delete old table and create new table 
            index=False # Prevents creation of index column
        )
        conn.close() # Close connection
        print("Data loading successful.")
        return df

