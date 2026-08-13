"""
V5 — Detect price drops.
"""
import csv
from rich.console import Console

from config import BOOKS_CSV
from price_history import record_price
from tracker_setup import load_watchlist, save_watchlist

console = Console()


def parse_price(price_str: str) -> float:
    cleaned = price_str.replace("£", "").replace("Â", "").replace("\u00a3", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_current_prices() -> dict:
    prices = {}
    if not BOOKS_CSV.exists():
        console.print("[red]✗ books.csv not found.[/]")
        return prices

    with open(BOOKS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices[row["title"]] = parse_price(row["price"])

    return prices


def check_price_drops(watchlist: list, current_prices: dict) -> list:
    alerts = []

    for item in watchlist:
        title = item["title"]
        target = item["target_price"]
        last = item.get("last_price", 0.0)
        email = item["email"]

        if title not in current_prices:
            console.print(f"[dim]⊘ '{title[:40]}' not in scrape, skipping.[/]")
            continue

        current = current_prices[title]
        record_price(title, current)

        hit_target = current <= target
        dropped = current < last if last > 0 else False

        if hit_target or dropped:
            drop = last - current if last > 0 else 0
            pct = (drop / last * 100) if last > 0 else 0

            console.print(
                f"[bold red]🔔 DROP:[/] {title[:45]}\n"
                f"   Was: £{last:.2f} → Now: [green]£{current:.2f}[/] "
                f"({pct:.1f}% off) | Target: £{target:.2f}"
            )

            alerts.append({
                "title": title,
                "email": email,
                "old_price": last,
                "new_price": current,
                "target_price": target,
                "drop": drop,
                "drop_pct": pct,
            })

            item["last_price"] = current
        else:
            console.print(
                f"[dim]✓ {title[:45]}: £{current:.2f} (target: £{target:.2f})[/]"
            )

    save_watchlist(watchlist)
    return alerts