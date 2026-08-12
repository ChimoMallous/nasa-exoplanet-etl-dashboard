import sqlite3
import pandas as pd
import logging
from contextlib import closing

from src.etl import DB_PATH

logger = logging.getLogger(__name__)


def _query(sql, description):
    """
    Runs a read-only query against the exoplanet database and returns the result.
    The connection is closed even if the query raises.
    -
    Args:
        sql (str): SQL statement to execute.
        description (str): Caller name, used to identify failures in the log.
    -
    Returns:
        DataFrame: The query result.
    """
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            return pd.read_sql(sql, conn)
    except Exception as e:
        logger.error(f"{description} failed: {e}")
        raise


def count_exoplanets_discovered():
    """
    Queries the database for the total number of unique confirmed exoplanets.
    -
    Returns:
        DataFrame: Single row with column total_exoplanets_discovered.
    """
    return _query(
        """
        SELECT COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets;
        """,
        "count_exoplanets_discovered",
    )


def count_confirmed_hosts():
    """
    Queries the database for the total number of unique confirmed host stars.
    -
    Returns:
        DataFrame: Single row with column total_confirmed_hosts.
    """
    return _query(
        """
        SELECT COUNT(DISTINCT host_name) AS total_confirmed_hosts
        FROM exoplanets;
        """,
        "count_confirmed_hosts",
    )


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
    return _query(
        """
        SELECT name AS exoplanet_name, discovery_pubdate, discovery_method
        FROM exoplanets
        ORDER BY discovery_year DESC, discovery_pubdate DESC, name ASC
        LIMIT 1;
        """,
        "recent_exoplanet_discovered",
    )


def count_exoplanets_discovered_by_year():
    """
    Queries the database for the number of unique exoplanets discovered per year,
    ordered chronologically. Records with an unknown discovery year are excluded
    here rather than dropped during validation, so they still count toward totals.
    -
    Returns:
        DataFrame: Rows with columns year and total_exoplanets_discovered, ordered by year ascending.
    """
    return _query(
        """
        SELECT discovery_year AS year, COUNT(DISTINCT name) AS total_exoplanets_discovered
        FROM exoplanets
        WHERE discovery_year IS NOT NULL
        GROUP BY discovery_year
        ORDER BY year ASC;
        """,
        "count_exoplanets_discovered_by_year",
    )


def count_exoplanets_discovered_by_method():
    """
    Queries the database for the number of unique exoplanets discovered per detection method,
    ordered by frequency descending.
    -
    Returns:
        DataFrame: Rows with columns discovery_method and method_frequency, ordered by method_frequency descending.
    """
    return _query(
        """
        SELECT discovery_method, COUNT(DISTINCT name) AS method_frequency
        FROM exoplanets
        GROUP BY discovery_method
        ORDER BY method_frequency DESC;
        """,
        "count_exoplanets_discovered_by_method",
    )


def count_exoplanets_discovered_by_facility():
    """
    Queries the database for the top 10 discovery facilities by number of unique exoplanets confirmed.
    -
    Returns:
        DataFrame: Rows with columns discovery_facility and exoplanets_discovered, ordered by exoplanets_discovered descending.
    """
    return _query(
        """
        SELECT discovery_facility, COUNT(DISTINCT name) AS exoplanets_discovered
        FROM exoplanets
        GROUP BY discovery_facility
        ORDER BY exoplanets_discovered DESC
        LIMIT 10;
        """,
        "count_exoplanets_discovered_by_facility",
    )