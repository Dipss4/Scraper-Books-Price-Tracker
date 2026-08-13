"""
V3 — Watchlist management with target price.
"""
import json
import csv
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt, Confirm
from rich.panel import Panel

from config import WATCHLIST_FILE, BOOKS_CSV

console = Console()


def load_watchlist() -> list:
    if WATCHLIST_FILE.exists():
        with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []


def save_watchlist(watchlist: list):
    WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(watchlist, f, indent=4, ensure_ascii=False)


def parse_price(price_str: str) -> float:
    cleaned = price_str.replace("£", "").replace("Â", "").replace("\u00a3", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_books_from_csv() -> list:
    if not BOOKS_CSV.exists():
        return []
    books = []
    with open(BOOKS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books


def show_watchlist(watchlist: list):
    if not watchlist:
        console.print("\n[bold yellow]⚠ Watchlist is empty.[/]\n")
        return

    table = Table(
        title="📋 Your Watchlist",
        show_lines=True,
        border_style="cyan",
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Title", style="bold white", max_width=50)
    table.add_column("Target", style="green", justify="center")
    table.add_column("Last Price", style="yellow", justify="center")
    table.add_column("Email", style="dim cyan")

    for idx, item in enumerate(watchlist, 1):
        last = item.get("last_price", 0.0)
        table.add_row(
            str(idx),
            item["title"],
            f"£{item['target_price']:.2f}",
            f"£{last:.2f}" if last else "—",
            item["email"],
        )

    console.print()
    console.print(table)
    console.print()


def add_to_watchlist(watchlist: list) -> list:
    books = load_books_from_csv()

    if not books:
        console.print("[bold red]✗ books.csv not found or empty. Run scraper first.[/]")
        return watchlist

    # ── Show books in a table ──
    table = Table(
        title="📚 Available Books",
        show_lines=False,
        border_style="blue",
    )
    table.add_column("#", style="dim", width=5, justify="right")
    table.add_column("Title", style="white", max_width=55)
    table.add_column("Price", style="green", justify="center", width=10)
    table.add_column("Rating", style="yellow", justify="center", width=8)
    table.add_column("Stock", style="cyan", justify="center", width=12)

    for idx, book in enumerate(books, 1):
        table.add_row(
            str(idx),
            book["title"],
            book["price"],
            f"{'★' * int(book.get('rating', '0'))}",
            book["inStock"],
        )

    console.print()
    console.print(table)

    # ── Select book ──
    choice = IntPrompt.ask(
        "\nEnter book number to track (0 to cancel)",
        default=0,
    )

    if choice == 0 or choice < 1 or choice > len(books):
        return watchlist

    selected = books[choice - 1]
    current_price = parse_price(selected["price"])

    console.print(
        Panel(
            f"[bold]{selected['title']}[/]\n"
            f"Current price: [green]£{current_price:.2f}[/]",
            title="Selected Book",
            border_style="green",
        )
    )

    # ── Target price ──
    target = FloatPrompt.ask("Set your target price (£)")
    while target <= 0:
        console.print("[red]Target must be positive.[/]")
        target = FloatPrompt.ask("Set your target price (£)")

    # ── Email ──
    email = Prompt.ask("Your alert email")
    while "@" not in email or "." not in email:
        console.print("[red]Invalid email.[/]")
        email = Prompt.ask("Your alert email")

    # ── Check duplicate ──
    for item in watchlist:
        if item["title"] == selected["title"]:
            if Confirm.ask(f"'{selected['title']}' already tracked. Update?"):
                item["target_price"] = target
                item["email"] = email
                console.print("[green]✓ Updated.[/]")
            return watchlist

    watchlist.append({
        "title": selected["title"],
        "target_price": target,
        "email": email,
        "last_price": current_price,
    })

    console.print(
        f"\n[bold green]✓[/] Added '[bold]{selected['title']}[/]' "
        f"— alert when ≤ [green]£{target:.2f}[/]"
    )

    return watchlist


def remove_from_watchlist(watchlist: list) -> list:
    if not watchlist:
        console.print("[yellow]⚠ Watchlist is empty.[/]")
        return watchlist

    show_watchlist(watchlist)

    choice = IntPrompt.ask("Enter number to remove (0 to cancel)", default=0)

    if choice == 0 or choice < 1 or choice > len(watchlist):
        return watchlist

    removed = watchlist.pop(choice - 1)
    console.print(f"[green]✓[/] Removed '[bold]{removed['title']}[/]'")
    return watchlist


def setup_menu():
    watchlist = load_watchlist()

    while True:
        console.print(
            Panel(
                "[1] View watchlist\n"
                "[2] Add book\n"
                "[3] Remove book\n"
                "[4] Back",
                title="📋 Watchlist Manager",
                border_style="cyan",
            )
        )

        choice = Prompt.ask("Choose", choices=["1", "2", "3", "4"], default="4")

        if choice == "1":
            show_watchlist(watchlist)

        elif choice == "2":
            watchlist = add_to_watchlist(watchlist)
            save_watchlist(watchlist)

        elif choice == "3":
            watchlist = remove_from_watchlist(watchlist)
            save_watchlist(watchlist)

        elif choice == "4":
            break