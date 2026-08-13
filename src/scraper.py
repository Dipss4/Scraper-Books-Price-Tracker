import requests
import csv
from queue import Queue
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor

from config import BOOKS_CSV, MAX_WORKERS

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.6",
    "Accept-Encoding": "gzip, deflate",
    "Referer": BASE_URL,
}


def convert_rating(rating_str: str) -> str:
    rating_map = {
        "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5",
    }
    if not rating_str:
        return "0"
    return rating_map.get(rating_str.strip().lower(), rating_str)


def build_image_url(src: str) -> str:
    """Convert relative image path to absolute URL."""
    cleaned = src.replace("../", "")
    return f"{BASE_URL}{cleaned}"


def build_book_url(href: str) -> str:
    """Convert relative book link to absolute URL."""
    cleaned = href.replace("../", "")
    return f"{BASE_URL}catalogue/{cleaned}"


def start_scan(url_base: int, session: requests.Session, data_queue: Queue):
    for i in range(url_base, url_base + 5):
        url = f"{BASE_URL}catalogue/page-{i}.html"
        r = session.get(url)

        if r.status_code != 200:
            return 0

        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        table = soup.select_one("ol.row")

        for t in table.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):
            rating = t.select_one(".star-rating")["class"][1]

            link = t.select_one("h3 a")
            title = link.get("title") if link else None
            href = link.get("href", "") if link else ""

            img_tag = t.select_one("div.image_container img")
            img_src = img_tag.get("src", "") if img_tag else ""

            price = t.select_one("div.product_price p.price_color").text

            in_stock_el = t.select_one("div.product_price p.instock")
            in_stock = (
                "Available"
                if in_stock_el and in_stock_el.get_text(strip=True)
                else "Unavailable"
            )

            rating = convert_rating(rating)

            book_info = {
                "title": title,
                "rating": rating,
                "price": price,
                "inStock": in_stock,
                "image": build_image_url(img_src),
                "url": build_book_url(href),
            }
            data_queue.put(book_info)

    return 1


def csv_writer_consumer(data_queue: Queue, filename: str):
    fieldnames = ["title", "rating", "price", "inStock", "image", "url"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            item = data_queue.get()
            if item is None:
                data_queue.task_done()
                break
            writer.writerow(item)
            data_queue.task_done()


def main():
    data_queue = Queue()
    session = requests.Session()
    session.headers.update(HEADERS)

    adapter = requests.adapters.HTTPAdapter(
        pool_connections=MAX_WORKERS,
        pool_maxsize=MAX_WORKERS,
        max_retries=3,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    csv_path = str(BOOKS_CSV)

    with ThreadPoolExecutor(max_workers=1) as writer_executor:
        writer_executor.submit(csv_writer_consumer, data_queue, csv_path)

        support_n = 0
        base_url_num = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as scraper_executor:
            keep_going = True
            while keep_going:
                if base_url_num:
                    support_n = int((base_url_num[-1] - 1) / 5)
                base_url_num = [i * 5 + 1 for i in range(support_n, support_n + MAX_WORKERS)]

                futures = [
                    scraper_executor.submit(start_scan, u, session, data_queue)
                    for u in base_url_num
                ]

                for future in futures:
                    if future.result() == 0:
                        keep_going = False
                        break

                data_queue.join()

        data_queue.put(None)


if __name__ == "__main__":
    main()