"""
Main entry point — CLI + API server.
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


def banner():
    console.print(
        Panel(
            "[bold white]"
            "[1]  🔍  Scrape books now\n"
            "[2]  📋  Manage watchlist (CLI)\n"
            "[3]  📈  View price history (CLI)\n"
            "[4]  ▶   Run full pipeline once\n"
            "[5]  ⏰  Start daily scheduler\n"
            "[6]  🌐  Start API server (for web UI)\n"
            "[7]  🚪  Exit"
            "[/]",
            title="[bold cyan]📚 Books Price Tracker[/]",
            border_style="cyan",
            padding=(1, 3),
        )
    )


def main():
    while True:
        banner()
        choice = Prompt.ask(
            "Choose",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            default="7",
        )

        if choice == "1":
            from scraper import main as run_scraper
            console.print("\n[bold]🔍 Starting scraper...[/]\n")
            try:
                run_scraper()
                console.print("[green]✓ Scrape complete.[/]\n")
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/]")

        elif choice == "2":
            from tracker_setup import setup_menu
            setup_menu()

        elif choice == "3":
            from price_history import show_price_history
            from tracker_setup import load_watchlist
            watchlist = load_watchlist()
            if not watchlist:
                console.print("[yellow]⚠ Watchlist empty.[/]")
                continue
            for idx, item in enumerate(watchlist, 1):
                console.print(f"  [dim]{idx}.[/] {item['title']}")
            ch = Prompt.ask("Book number (0 cancel)", default="0")
            try:
                n = int(ch)
                if 1 <= n <= len(watchlist):
                    show_price_history(watchlist[n - 1]["title"])
            except ValueError:
                pass

        elif choice == "4":
            from scheduler import full_pipeline
            full_pipeline()

        elif choice == "5":
            from scheduler import start_scheduler
            start_scheduler()

        elif choice == "6":
            from api import start_api
            console.print("[bold cyan]🌐 Starting API server...[/]")
            console.print("[dim]Frontend: http://localhost:5173[/]")
            console.print("[dim]API docs: http://localhost:8000/api/docs[/]\n")
            start_api()

        elif choice == "7":
            console.print("[bold cyan]Bye! 👋[/]")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/]")