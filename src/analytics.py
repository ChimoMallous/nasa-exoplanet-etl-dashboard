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
        SELECT discovery_method,
            COUNT(DISTINCT name) AS method_frequency,
            ROUND(COUNT(DISTINCT name) * 100.0 /
                    (SELECT COUNT(DISTINCT name) FROM exoplanets), 1) AS share_of_total
        FROM exoplanets
        GROUP BY discovery_method
        ORDER BY method_frequency DESC;
        """,
        "count_exoplanets_discovered_by_method",
    )

def sky_positions():
    """
    Queries the sky coordinates of every planet, grouped by the survey that found it.
    Right ascension and declination are populated for the entire catalog.
    -
    Returns:
        DataFrame: Rows with columns name, right_ascension, declination, discovery_year,
        discovery_facility, discovery_method, and survey.
    """
    return _query(
        """
        SELECT name, right_ascension, declination, discovery_year, discovery_facility, discovery_method,
               CASE
                   WHEN discovery_facility = 'Kepler' THEN 'Kepler'
                   WHEN discovery_facility LIKE '%TESS%' THEN 'TESS'
                   WHEN discovery_facility = 'K2' THEN 'K2'
                   ELSE 'All other facilities'
               END AS survey
        FROM exoplanets
        WHERE right_ascension IS NOT NULL AND declination IS NOT NULL;
        """,
        "sky_positions",
    )

def exoplanet_classifications():
    """
    Groups every planet into a size class, using mass where measured and falling back
    to radius otherwise. Mass takes precedence because it indicates composition more
    directly than radius, which cannot separate a dense super-Earth from an inflated
    mini-Neptune. Planets with neither measurement are returned as Unknown.
    -
    Returns:
        DataFrame: Rows with columns planet_count and exoplanet_bin.
    """
    return _query(
        """
        SELECT COUNT(DISTINCT name) AS planet_count,
               CASE
                   WHEN planet_mass IS NOT NULL THEN
                       CASE
                           WHEN planet_mass <= 2 THEN 'Terrestrial'
                           WHEN planet_mass <= 10  THEN 'Super Earth'
                           WHEN planet_mass <= 50  THEN 'Neptune-like'
                           ELSE 'Gas Giant'
                       END
                   WHEN planet_radius IS NOT NULL THEN
                       CASE
                           WHEN planet_radius <= 1.25 THEN 'Terrestrial'
                           WHEN planet_radius <= 2 THEN 'Super Earth'
                           WHEN planet_radius <= 6 THEN 'Neptune-like'
                           ELSE 'Gas Giant'
                       END
                   ELSE 'Unknown'
               END AS exoplanet_bin
        FROM exoplanets
        GROUP BY exoplanet_bin
        """,
        "exoplanet_classifications"
    )