import sqlite3
import pandas as pd

def count_exoplanet_discoveries(): 

    conn = sqlite3.connect("exoplanet_db") # Create connection to database

    query = """
    SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered
    FROM exoplanets;
    """ # Create query to count the total amount of exoplanet records

    result = pd.read_sql(query, conn) # Execute query and store results in DataFrame

    conn.close() # Close connection
    
    return result

def count_stars_with_exoplanets():

    conn = sqlite3.connect("exoplanet_db")

    query = """
    SELECT COUNT(DISTINCT star_name) AS total_stars_with_exoplanets
    FROM exoplanets;
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return result

def count_planets_discovered_by_year():

    conn = sqlite3.connect("exoplanet_db")

    query = """
    SELECT discovery_year AS year, COUNT(DISTINCT name) AS total_exoplanets_discovered
    FROM exoplanets
    GROUP BY discovery_year
    ORDER BY year DESC
    LIMIT 20;
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return result

def top_stars_by_planet_count():

    conn = sqlite3.connect('exoplanet_db')

    query = """
    SELECT star_name, COUNT(DISTINCT name) AS exoplanet_count
    FROM exoplanets
    GROUP BY star_name
    ORDER BY exoplanet_count DESC
    LIMIT 20;
    """
    
    result = pd.read_sql(query, conn)

    conn.close()

    return result

#print(count_exoplanet_discoveries())
#print(count_stars_with_exoplanets())
#print(count_planets_discovered_by_year())
#print(top_stars_by_planet_count())

