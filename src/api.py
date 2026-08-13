"""
REST API backend — serves data to Vue frontend.
"""
import csv
import threading
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from config import BOOKS_CSV, API_HOST, API_PORT
from tracker_setup import load_watchlist, save_watchlist
from price_history import get_price_history, load_history
from price_monitor import load_current_prices, check_price_drops
from email_alert import send_all_alerts
from scraper import main as run_scraper

app = FastAPI(
    title="Books Price Tracker API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Track scraper status ──
scraper_status = {"running": False, "last_run": None}


# ── Pydantic Models ──
class WatchlistAdd(BaseModel):
    title: str
    target_price: float
    email: str


class WatchlistUpdate(BaseModel):
    target_price: Optional[float] = None
    email: Optional[str] = None


# ── Helpers ──
def parse_price(price_str: str) -> float:
    cleaned = price_str.replace("£", "").replace("Â", "").replace("\u00a3", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_books() -> list:
    """Load all books from CSV."""
    if not BOOKS_CSV.exists():
        return []
    books = []
    with open(BOOKS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            row["id"] = idx
            row["price_num"] = parse_price(row.get("price", "0"))
            books.append(row)
    return books


# ═══════════════════════════════════
#  BOOKS ENDPOINTS
# ═══════════════════════════════════

@app.get("/api/books")
def get_books(
    search: Optional[str] = Query(None),
    rating: Optional[int] = Query(None, ge=1, le=5),
    stock: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),       # price_asc, price_desc, rating, title
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Get all scraped books with filtering, sorting, pagination."""
    books = load_books()

    # ── Filter ──
    if search:
        q = search.lower()
        books = [b for b in books if q in b["title"].lower()]

    if rating:
        books = [b for b in books if int(b.get("rating", "0")) >= rating]

    if stock:
        books = [b for b in books if b.get("inStock", "").lower() == stock.lower()]

    # ── Sort ──
    if sort == "price_asc":
        books.sort(key=lambda b: b["price_num"])
    elif sort == "price_desc":
        books.sort(key=lambda b: b["price_num"], reverse=True)
    elif sort == "rating":
        books.sort(key=lambda b: int(b.get("rating", "0")), reverse=True)
    elif sort == "title":
        books.sort(key=lambda b: b["title"].lower())

    # ── Paginate ──
    total = len(books)
    start = (page - 1) * limit
    end = start + limit
    paginated = books[start:end]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "books": paginated,
    }


@app.get("/api/books/{book_id}")
def get_book(book_id: int):
    """Get single book by ID."""
    books = load_books()
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(404, "Book not found")
    return books[book_id]


# ═══════════════════════════════════
#  WATCHLIST ENDPOINTS
# ═══════════════════════════════════

@app.get("/api/watchlist")
def get_watchlist():
    """Get full watchlist."""
    watchlist = load_watchlist()
    return {"total": len(watchlist), "items": watchlist}


@app.post("/api/watchlist")
def add_to_watchlist(item: WatchlistAdd):
    """Add a book to watchlist."""
    watchlist = load_watchlist()

    # Check duplicate
    for existing in watchlist:
        if existing["title"] == item.title:
            raise HTTPException(409, "Book already in watchlist")

    # Get current price from CSV
    books = load_books()
    current_price = 0.0
    for book in books:
        if book["title"] == item.title:
            current_price = book["price_num"]
            break

    watchlist.append({
        "title": item.title,
        "target_price": item.target_price,
        "email": item.email,
        "last_price": current_price,
    })

    save_watchlist(watchlist)
    return {"message": "Added", "total": len(watchlist)}


@app.put("/api/watchlist/{index}")
def update_watchlist_item(index: int, update: WatchlistUpdate):
    """Update target price or email."""
    watchlist = load_watchlist()

    if index < 0 or index >= len(watchlist):
        raise HTTPException(404, "Item not found")

    if update.target_price is not None:
        watchlist[index]["target_price"] = update.target_price
    if update.email is not None:
        watchlist[index]["email"] = update.email

    save_watchlist(watchlist)
    return {"message": "Updated", "item": watchlist[index]}


@app.delete("/api/watchlist/{index}")
def remove_from_watchlist(index: int):
    """Remove a book from watchlist."""
    watchlist = load_watchlist()

    if index < 0 or index >= len(watchlist):
        raise HTTPException(404, "Item not found")

    removed = watchlist.pop(index)
    save_watchlist(watchlist)
    return {"message": "Removed", "removed": removed["title"]}


# ═══════════════════════════════════
#  PRICE HISTORY ENDPOINTS
# ═══════════════════════════════════

@app.get("/api/history/{title}")
def get_history(title: str):
    """Get price history for a book."""
    entries = get_price_history(title)
    return {"title": title, "entries": entries}


@app.get("/api/history")
def get_all_history():
    """Get all price history."""
    return load_history()


# ═══════════════════════════════════
#  PIPELINE / SCRAPER ENDPOINTS
# ═══════════════════════════════════

@app.post("/api/scrape")
def trigger_scrape():
    """Start a scrape in background."""
    if scraper_status["running"]:
        raise HTTPException(409, "Scraper already running")

    def run():
        scraper_status["running"] = True
        try:
            run_scraper()
            from datetime import datetime
            scraper_status["last_run"] = datetime.now().isoformat()
        finally:
            scraper_status["running"] = False

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return {"message": "Scrape started"}


@app.get("/api/scrape/status")
def get_scrape_status():
    """Check scraper status."""
    return scraper_status


@app.post("/api/pipeline")
def run_pipeline():
    """Run full pipeline: scrape → detect drops → send alerts."""
    if scraper_status["running"]:
        raise HTTPException(409, "Pipeline already running")

    def run():
        scraper_status["running"] = True
        try:
            # 1. Scrape
            run_scraper()

            # 2. Check drops
            watchlist = load_watchlist()
            if watchlist:
                prices = load_current_prices()
                alerts = check_price_drops(watchlist, prices)

                # 3. Send alerts
                if alerts:
                    send_all_alerts(alerts)

            from datetime import datetime
            scraper_status["last_run"] = datetime.now().isoformat()
        finally:
            scraper_status["running"] = False

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return {"message": "Pipeline started"}


# ═══════════════════════════════════
#  STATS ENDPOINT
# ═══════════════════════════════════

@app.get("/api/stats")
def get_stats():
    """Dashboard stats."""
    books = load_books()
    watchlist = load_watchlist()
    history = load_history()

    total_books = len(books)
    avg_price = (
        sum(b["price_num"] for b in books) / total_books
        if total_books > 0
        else 0
    )

    below_target = 0
    for item in watchlist:
        for book in books:
            if book["title"] == item["title"]:
                if book["price_num"] <= item["target_price"]:
                    below_target += 1
                break

    return {
        "total_books": total_books,
        "avg_price": round(avg_price, 2),
        "watchlist_count": len(watchlist),
        "tracked_books_history": len(history),
        "below_target": below_target,
        "scraper_running": scraper_status["running"],
        "last_scrape": scraper_status["last_run"],
    }


# ═══════════════════════════════════
#  RUN
# ═══════════════════════════════════

def start_api():
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    start_api()