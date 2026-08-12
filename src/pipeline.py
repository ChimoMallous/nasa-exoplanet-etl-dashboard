import logging

from src.etl import extract, transform, validate, load_to_db, PROJECT_ROOT


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run():
    """
    Orchestrates the ETL pipeline by running extract, transform, and load functions in sequence.
    Logs pipeline status at each stage.
    -
    Returns:
        bool: True if records were loaded, False if the pipeline failed for any reason.
    """
    logger.info("Pipeline started.")
    try:
        r_data = extract()
        df = transform(r_data)
        df = validate(df)
        if df is not None and not df.empty:
            load_to_db(df)
            logger.info("Pipeline completed successfully.")
            return True
    except Exception as e:
        logger.error(f"Pipeline failed with an unexpected error: {e}")
        return False
    logger.error("Pipeline failed. No data loaded.")
    return False

if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)