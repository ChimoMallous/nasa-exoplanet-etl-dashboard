import sqlite3
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def count_exoplanets_discovered(): 
    try:
        conn = sqlite3.connect("exoplanet_db") # Create connection to database

        query = """
        SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets;
        """ # Create query to count the total amount of exoplanet records

        result = pd.read_sql(query, conn) # Execute query and store results in DataFrame

        conn.close() # Close connection
        
        return result
    except Exception as e:
        logging.error(f"count_exoplanets_discovered failed: {e}")

def count_exoplanets_discovered_2026():
    try:
        conn = sqlite3.connect("exoplanet_db")

        query = """
        SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered_2026
        FROM exoplanets
        WHERE discovery_year = 2026;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logging.error(f"count_exoplanets_discovered_2026 failed: {e}")

def count_exoplanets_discovered_by_year():
    try:
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
    except Exception as e:
        logging.error(f"count_exoplanets_discovered_by_year failed: {e}")

def top_exoplanet_discovery_methods():
    try:
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
    except Exception as e:
        logging.error(f"top_exoplanet_discovery_methods failed: {e}")

def exoplanet_radius_by_discovery_method():
    try:
        conn = sqlite3.connect("exoplanet_db")

        query = """
        SELECT 
            discovery_method, 
            CASE
                WHEN planet_radius < 2 THEN 'Small (<2 Earth Radius)'
                WHEN planet_radius < 6 THEN 'Medium (2-6 Earth Radius)'
                WHEN planet_radius < 15 THEN 'Large (6-15 Earth Radius)'
                ELSE 'Giant (>15 Earth Radius)'
            END AS size_category,
            COUNT(DISTINCT name) AS planet_count
        FROM exoplanets
        WHERE planet_radius IS NOT NULL
        GROUP BY discovery_method, size_category
        ORDER BY discovery_method;
        """ 

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logging.error(f"exoplanet_radius_by_discovery_method failed: {e}")

