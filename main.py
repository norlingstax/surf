import sys
import logging
import os
import pandas as pd
from surf_scrap import scrap

TARGET_URL = "https://www.surf-report.com/meteo-surf/moliets-plage-centrale-s102799.html"
OUTPUT_FILE = "data/surf_forecast.csv"

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)


def step_scraping():
    """Step 1: Uses the surf_scrap library to download data."""
    log.info(f"Target: {TARGET_URL}")
    try:
        # We call the function from your library directly
        scrap.get_forecast(TARGET_URL, OUTPUT_FILE)
    except Exception as e:
        log.error(f"Scraping failed: {e}")
        sys.exit(1)  # Stop the pipeline if scraping fails


def step_verification():
    """Step 2: Checks if the file was created and prints a preview."""
    if not os.path.exists(OUTPUT_FILE):
        log.error(f"File not found at {OUTPUT_FILE}")
        sys.exit(1)

    try:
        df = pd.read_csv(OUTPUT_FILE)
        log.info(f"Dataset successfully loaded. Shape: {df.shape}")
        log.info("Preview of data:")
        # We print a clean string representation of the first 3 rows
        log.info("\n" + df.head(3).to_string())
    except Exception as e:
        log.error(f"Failed to read CSV: {e}")
        sys.exit(1)


# --- Main Pipeline ---
if __name__ == "__main__":
    log.info("Starting Surf Scrap Pipeline")
    log.info("--------------------------------")

    # STEP 1
    log.info("Step 1/2: Scraping data")
    step_scraping()
    log.info("Completed successfully")

    # STEP 2
    log.info("Step 2/2: Verifying dataset")
    step_verification()
    log.info("Completed successfully")

    log.info("--------------------------------")
    log.info("Pipeline finished. Data is ready in 'data/' folder.")