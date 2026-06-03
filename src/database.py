import sqlite3
import pandas as pd

def save_to_db(df):

    conn = sqlite3.connect("exoplanet_db") # Create connection to database

    df.to_sql(
        "exoplanets", # Store dataframe as SQL table
        conn, # Make connection to database
        if_exists ="replace", # Delete old table and create new table 
        index=False # Prevents creation of index column
    )

    conn.close() # Close connection 