"""
V4 — Price history storage.
"""
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

from config import HISTORY_FILE

console = Console()


def load_history() -> dict:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def record_price(title: str, price: float):
    history = load_history()

    if title not in history:
        history[title] = []

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Skip if same day & same price
    if history[title]:
        last = history[title][-1]
        if last["date"][:10] == now[:10] and last["price"] == price:
            return

    history[title].append({"date": now, "price": price})
    save_history(history)


def get_price_history(title: str) -> list:
    return load_history().get(title, [])


def show_price_history(title: str):
    entries = get_price_history(title)

    if not entries:
        console.print(f"[yellow]⚠ No history for '{title}'[/]")
        return

    table = Table(title=f"📈 Price History: {title[:50]}", border_style="blue")
    table.add_column("Date", style="dim")
    table.add_column("Price", style="green", justify="center")

    for entry in entries[-15:]:
        table.add_row(entry["date"], f"£{entry['price']:.2f}")

    console.print(table)