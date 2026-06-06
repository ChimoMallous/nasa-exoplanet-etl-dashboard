try: 
    from src.etl import extract, transform, load_to_db, url
except ImportError:
    from etl import extract, transform, load_to_db, url
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run():
    logger.info("Pipeline started.")
    r_data = extract(url)
    df = transform(r_data)
    if df is not None and not df.empty:
        load_to_db(df)
        logger.info("Pipeline completed successfully.")
    else:
        logger.error("Pipeline failed. No data loaded.")

if __name__ == "__main__":
    run()