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
        raise

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
        raise

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
        raise

def count_exoplanets_discovered_by_method():
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
        raise

def count_exoplanets_discovered_by_facility():
    try:
        conn = sqlite3.connect("exoplanet_db")
        query = """
        SELECT discovery_facility, COUNT(DISTINCT name) AS exoplanets_discovered
        FROM exoplanets
        GROUP BY discovery_facility
        ORDER BY exoplanets_discovered DESC
        LIMIT 10;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logging.error(f"count_exoplanets_discovered_by_facility failed: {e}")
        raise