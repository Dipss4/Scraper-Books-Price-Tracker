"""
Centralized paths and environment config.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

# ── Paths ──
BOOKS_DIR      = ROOT_DIR / "books"
DATA_DIR       = ROOT_DIR / "data"
BOOKS_CSV      = BOOKS_DIR / "books.csv"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
HISTORY_FILE   = DATA_DIR / "price_history.json"
LOG_FILE       = ROOT_DIR / "tracker.log"

BOOKS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ── SMTP ──
SMTP_SERVER  = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASS  = os.getenv("SENDER_PASS", "")

# ── Scheduler ──
DAILY_RUN_TIME = os.getenv("DAILY_RUN_TIME", "09:00")

# ── Scraper ──
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))

# ── API ──
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))