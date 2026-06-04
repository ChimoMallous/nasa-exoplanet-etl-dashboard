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
    ORDER BY year DESC;
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return result

def top_exoplanet_discovery_methods():

    conn = sqlite3.connect('exoplanet_db')

    query = """
    SELECT discovery_method, COUNT(DISTINCT name) AS method_frequency
    FROM exoplanets
    GROUP BY discovery_method
    ORDER BY method_frequency DESC;
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return result

def exoplanet_radius_by_discovery_method():

    conn = sqlite3.connect("exoplanet_db")

    query = """
    SELECT discovery_method, AVG(planet_radius) AS avg_radius, MIN(planet_radius) AS min_radius, MAX(planet_radius) AS max_radius
    FROM exoplanets
    WHERE planet_radius IS NOT NULL
    GROUP BY discovery_method
    ORDER BY avg_radius DESC;
    """ 

    result = pd.read_sql(query, conn)

    conn.close()

    return result

