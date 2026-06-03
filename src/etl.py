import requests
import pandas as pd
from database import save_to_db


url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=select+pl_name,disc_year,pl_rade,hostname+from+ps"

def extract(url):
    response = requests.get(url)
    if response.status_code == 200:
        r_data = response.json()
        print("Data extraction successful.")
        return r_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def transform(data):
    if not data:
        print("No data to transform.")
        return []
    else: 
        t_data = [{
            "name": p.get("pl_name"),
            "discovery_year": p.get("disc_year"),  # changed from pl_disc
            "planet_radius": p.get("pl_rade"),
            "star_name": p.get("hostname")
        }
        for p in data
        ]
        print("Data transformation successful.")
        return t_data

def load(t_data):
    if t_data is None:
        print("No transformed data to load.")
    else:
        df = pd.DataFrame(t_data)
        print("Data loading successful.")
        return df

r_data = extract(url)
t_data = transform(r_data)
df = load(t_data)

try:
    save_to_db(df)
    print("Dataframe saved to Database")
except Exception as e:
    print(f"Error: {e}")
