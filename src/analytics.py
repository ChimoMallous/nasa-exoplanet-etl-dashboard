import sqlite3
import pandas as pd
import logging

try:
    from src.etl import DB_PATH
except ImportError:
    from etl import DB_PATH

logger = logging.getLogger(__name__)

def count_exoplanets_discovered(): 
    """
    Queries the database for the total number of unique confirmed exoplanets.
    -
    Returns:
        DataFrame: Single row with column total_exoplanets_discovered.
    """
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
        SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets;
        """ 

        result = pd.read_sql(query, conn)

        conn.close() 
        
        return result
    except Exception as e:
        logger.error(f"count_exoplanets_discovered failed: {e}")
        raise

def count_confirmed_hosts():
    """
    Queries the database for the total number of unique confirmed host stars.
    -
    Returns:
        DataFrame: Single row with column total_confirmed_hosts.
    """
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

def recent_exoplanet_discovered():
    """
    Queries the database for a recently discovered unique exoplanet,
    ranked by discovery year then by the publication date of the discovery paper (YYYY-MM).
    Many planets share a publication month; ties are broken alphabetically,
    so this returns one recent discovery.
    -
    Returns:
        DataFrame: Single row with columns exoplanet_name, discovery_pubdate, and discovery_method.
    """
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
        SELECT name AS exoplanet_name, discovery_pubdate, discovery_method
        FROM exoplanets
        ORDER BY discovery_year DESC, discovery_pubdate DESC, name ASC
        LIMIT 1;
        """

        result = pd.read_sql(query, conn)

        conn.close()

        return result
    except Exception as e:
        logger.error(f"recent_exoplanet_discovered failed: {e}")
        raise

def count_exoplanets_discovered_by_year():
    """
    Queries the database for the number of unique exoplanets discovered per year,
    ordered chronologically.
    -
    Returns:
        DataFrame: Rows with columns year and total_exoplanets_discovered, ordered by year ascending.
    """
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
    """
    Queries the database for the number of unique exoplanet discovered per detection method,
    ordered by frequency descending.
    -
    Returns:
        DataFrame: Rows with columns discovery_method and method_frequency, ordered by method_frequency descending.
    """
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
        logger.error(f"count_exoplanets_discovered_by_method failed: {e}")
        raise

def count_exoplanets_discovered_by_facility():
    """
    Queries the database for the top 10 discovery facilities by number of unique exoplanets confirmed.
    -
    Returns:
        DataFrame: Rows with columns discovery_facility and exoplanets_discovered, ordered by exoplanets_discovered descending.
    """
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