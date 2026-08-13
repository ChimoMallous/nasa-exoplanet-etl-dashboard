import pandas as pd

from src.etl import transform, validate


# ---------------------------------------------------------------- transform

def test_transform_maps_api_fields_to_database_columns():
    raw = [{
        "pl_name": "Kepler-22 b",
        "hostname": "Kepler-22",
        "disc_year": 2011,
        "disc_pubdate": "2011-12",
        "discoverymethod": "Transit",
        "disc_facility": "Kepler",
        "ra": 285.679,
        "dec": 47.968,
    }]

    result = transform(raw)

    assert list(result.columns) == [
        "name",
        "host_name",
        "discovery_year",
        "discovery_pubdate",
        "discovery_method",
        "discovery_facility",
        "right_ascension",
        "declination",
    ]
    assert result.loc[0, "name"] == "Kepler-22 b"
    assert result.loc[0, "host_name"] == "Kepler-22"
    assert result.loc[0, "discovery_year"] == 2011
    assert result.loc[0, "right_ascension"] == 285.679
    assert result.loc[0, "declination"] == 47.968


def test_transform_strips_whitespace_and_converts_blanks_to_null():
    raw = [{
        "pl_name": "  Kepler-22 b  ",
        "hostname": "",
        "disc_year": 2011,
        "disc_pubdate": "2011-12",
        "discoverymethod": "Transit",
        "disc_facility": "Kepler",
    }]

    result = transform(raw)

    assert result.loc[0, "name"] == "Kepler-22 b"
    assert pd.isna(result.loc[0, "host_name"])


def test_transform_converts_unparseable_year_to_null():
    raw = [{
        "pl_name": "Kepler-22 b",
        "hostname": "Kepler-22",
        "disc_year": "not a year",
        "disc_pubdate": "2011-12",
        "discoverymethod": "Transit",
        "disc_facility": "Kepler",
    }]

    result = transform(raw)

    assert pd.isna(result.loc[0, "discovery_year"])


def test_transform_returns_none_for_empty_input():
    assert transform([]) is None
    assert transform(None) is None


# ----------------------------------------------------------------- validate

def test_validate_drops_rows_with_no_planet_name():
    df = pd.DataFrame({
        "name": ["Kepler-22 b", None, "TRAPPIST-1 e"],
        "discovery_year": pd.array([2011, 2015, 2017], dtype="Int64"),
    })

    result = validate(df)

    assert len(result) == 2
    assert "Kepler-22 b" in result["name"].values
    assert "TRAPPIST-1 e" in result["name"].values


def test_validate_keeps_records_with_unknown_discovery_year():
    df = pd.DataFrame({
        "name": ["Kepler-22 b", "Kepler-186 f"],
        "discovery_year": pd.array([2011, None], dtype="Int64"),
    })

    result = validate(df)

    assert len(result) == 2
    assert "Kepler-186 f" in result["name"].values


def test_validate_clears_implausible_year_but_keeps_the_record():
    df = pd.DataFrame({
        "name": ["Kepler-22 b", "TRAPPIST-1 e"],
        "discovery_year": pd.array([2011, 3035], dtype="Int64"),
    })

    result = validate(df)

    assert len(result) == 2
    assert "TRAPPIST-1 e" in result["name"].values

    cleared = result.loc[result["name"] == "TRAPPIST-1 e", "discovery_year"].iloc[0]
    assert pd.isna(cleared)


def test_validate_removes_duplicate_planet_names_keeping_first():
    df = pd.DataFrame({
        "name": ["Kepler-22 b", "Kepler-22 b", "TRAPPIST-1 e"],
        "discovery_year": pd.array([2011, 1999, 2017], dtype="Int64"),
    })

    result = validate(df)

    assert len(result) == 2

    kept = result.loc[result["name"] == "Kepler-22 b", "discovery_year"].iloc[0]
    assert kept == 2011


def test_validate_returns_none_for_empty_input():
    assert validate(None) is None
    assert validate(pd.DataFrame()) is None