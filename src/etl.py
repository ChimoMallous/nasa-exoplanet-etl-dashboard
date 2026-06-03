import requests
import pandas as pd
from src.database import save_to_db


url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=select+pl_name,disc_year,discoverymethod,hostname+from+ps"

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
                "star_name": p.get("hostname")
            })
        print("Data transformation successful.")
        return t_data

def load(t_data):
    if t_data is None:
        print("No transformed data to load.")
    else:
        df = pd.DataFrame(t_data)
        print("Data loading successful.")
        return df

