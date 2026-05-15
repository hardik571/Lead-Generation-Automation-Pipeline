import sys
import time
import logging
import schedule
from datetime import datetime
from save_leads import save_leads_to_excel

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ── Pipeline ───────────────────────────────────────────────────────────────────

def run_pipeline():
    """
    Full lead generation pipeline:
      1. Scrape leads from the public directory
      2. Enrich with guessed emails
      3. Export to a timestamped Excel file
    """
    logger.info("=== run_pipeline() started at %s ===", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        filepath = save_leads_to_excel(output_dir=".", prefix="contact")
        if filepath:
            logger.info("Pipeline complete. File saved: %s", filepath)
        else:
            logger.warning("Pipeline ran but no leads were saved.")
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc, exc_info=True)
    logger.info("=== run_pipeline() finished ===\n")


# ── Scheduler ──────────────────────────────────────────────────────────────────

def start_scheduler(run_at: str = "08:00"):
    """
    Schedules run_pipeline() to execute once every day at the given time,
    then enters an infinite loop to keep the scheduler alive.

    Args:
        run_at: 24-hour time string for the daily run (default: "08:00").
    """
    schedule.every().day.at(run_at).do(run_pipeline)
    logger.info("Scheduler active — run_pipeline() will run daily at %s.", run_at)
    logger.info("Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)          # Poll every 30 seconds


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--schedule" in sys.argv:
        # Run immediately, then schedule daily at 08:00
        logger.info("--schedule flag detected. Running pipeline now, then scheduling daily at 08:00.")
        run_pipeline()
        start_scheduler(run_at="08:00")
    else:
        # Single one-shot run
        logger.info("No --schedule flag. Running pipeline once.")
        run_pipeline()
