import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from fetch_urls import fetch_url
from logger_setup import setup_logging
from notifier import send_alert
from scrapper import get_page_hash
from storage import has_changed, load_hashes, save_hashes

setup_logging("WebsiteMonitor.log")
logger: logging.Logger = logging.getLogger(__name__)


URLS: list[str] = [
    "https://books.toscrape.com",
    "https://quotes.toscrape.com",
]


def monitor_website():
    logger.info("Monitoring the Website to look for Changes ...")
    hashes: dict = load_hashes()

    for url in URLS:
        try:
            response = fetch_url(url)
            new_hash: str = get_page_hash(response)
            old_hash: str = hashes.get(url, {}).get("hash")
            timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if old_hash and has_changed(old_hash, new_hash):
                subject: str = "Website Changed!"
                plain_body: str = f"Change detected on: {url}\nDetected at: {timestamp}"
                html_body: str = f"<p>Change detected on: <a href='{url}'>{url}</a></p><p>Detected at: {timestamp}</p>"
                send_alert(subject, plain_body, html_body)
            hashes[url] = {"hash": new_hash, "timestamp": timestamp}

        except Exception:
            logger.exception("Something went wrong")
            continue

    save_hashes(hashes)
    logger.info("Finished Saving the json file.")


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        func=monitor_website,
        trigger="interval",
        minutes=1,
        args=[],
        next_run_time=datetime.now(),
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.warning("Stopped the function, was checking every 1 minute ...")


if __name__ == "__main__":
    main()
