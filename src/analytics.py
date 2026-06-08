import sqlite3
import pandas as pd
import logging

try:
    from src.etl import DB_PATH
except ImportError:
    from etl import DB_PATH

logger = logging.getLogger(__name__)

def count_exoplanets_discovered(): 
    try:
        conn = sqlite3.connect(DB_PATH) # Create connection to database

        query = """
        SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets;
        """ # Create query to count the total amount of exoplanet records

        result = pd.read_sql(query, conn) # Execute query and store results in DataFrame

        conn.close() # Close connection
        
        return result
    except Exception as e:
        logger.error(f"count_exoplanets_discovered failed: {e}")
        raise

def count_confirmed_hosts():
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
        SELECT COUNT(DISTINCT host_name) AS total_confirmed_hosts
        FROM exoplanets;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logger.error(f"count_confirmed_hosts failed: {e}")
        raise

def newest_exoplanet_discovered():
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
        SELECT name AS exoplanet_name, discovery_date, discovery_method
        FROM exoplanets
        WHERE discovery_year = (SELECT MAX(discovery_year) FROM exoplanets)
        GROUP BY name
        ORDER BY discovery_date DESC, name ASC
        LIMIT 1;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logger.error(f"newest_exoplanet_discovered failed: {e}")
        raise

def count_exoplanets_discovered_by_year():
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
        SELECT discovery_year AS year, COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets
        GROUP BY discovery_year
        ORDER BY year ASC;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logger.error(f"count_exoplanets_discovered_by_year failed: {e}")
        raise

def count_exoplanets_discovered_by_method():
    try:
        conn = sqlite3.connect(DB_PATH)

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
        logger.error(f"top_exoplanet_discovery_methods failed: {e}")
        raise

def count_exoplanets_discovered_by_facility():
    try:
        conn = sqlite3.connect(DB_PATH)
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
        logger.error(f"count_exoplanets_discovered_by_facility failed: {e}")
        raise