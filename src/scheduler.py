"""
V7 — Run automatically every day.
"""
import time
import logging
import schedule
from rich.console import Console

from config import DAILY_RUN_TIME, LOG_FILE
from scraper import main as run_scraper
from tracker_setup import load_watchlist
from price_monitor import load_current_prices, check_price_drops
from email_alert import send_all_alerts

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def full_pipeline():
    log.info("=" * 50)
    log.info("PIPELINE START")

    # 1 — Scrape
    log.info("[1/4] Scraping...")
    try:
        run_scraper()
        log.info("[1/4] Scrape done.")
    except Exception as e:
        log.error(f"[1/4] Scraper failed: {e}")
        return

    # 2 — Watchlist
    log.info("[2/4] Loading watchlist...")
    watchlist = load_watchlist()
    if not watchlist:
        log.info("[2/4] Empty watchlist. Done.")
        return
    log.info(f"[2/4] Tracking {len(watchlist)} book(s).")

    # 3 — Detect drops
    log.info("[3/4] Checking prices...")
    prices = load_current_prices()
    alerts = check_price_drops(watchlist, prices)
    log.info(f"[3/4] {len(alerts)} drop(s) found.")

    # 4 — Email
    log.info("[4/4] Sending alerts...")
    send_all_alerts(alerts)
    log.info("PIPELINE END")
    log.info("=" * 50)


def start_scheduler():
    console.print(
        f"[bold cyan]⏰ Scheduler started — runs daily at {DAILY_RUN_TIME}[/]"
    )
    console.print("[dim]Press CTRL+C to stop.[/]\n")

    schedule.every().day.at(DAILY_RUN_TIME).do(full_pipeline)

    # Initial run
    console.print("[bold]Running initial pipeline now...[/]\n")
    full_pipeline()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    try:
        start_scheduler()
    except KeyboardInterrupt:
        log.info("Scheduler stopped by user.")