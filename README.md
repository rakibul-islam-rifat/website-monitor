# Website Change Monitor

A Python automation tool that monitors multiple websites for content changes and sends an email alert when a change is detected.

## What It Does

- Fetches a configurable list of URLs on a scheduled interval
- Hashes each page's content using MD5
- Compares against previously stored hashes in a local JSON file
- Sends an email alert with the changed URL and timestamp when a difference is found

## Project Structure

```
website-change-monitor/
├── fetch_urls.py       # HTTP requests with retry logic and exponential backoff
├── scrapper.py         # MD5 hashing of page content
├── storage.py          # JSON read/write for hash persistence
├── notifier.py         # Email alerts via Gmail + smtplib
├── logger_setup.py     # Rotating file + console logging
├── main.py             # Orchestration + APScheduler
├── .env                # Credentials (not committed)
├── .gitignore
└── requirements.txt
```

## Setup

**1. Clone the repo and install dependencies:**

```bash
git clone https://github.com/rifat_automate/website-change-monitor
cd website-change-monitor
uv pip install -r requirements.txt
```

**2. Create a `.env` file in the project root:**

```
EMAIL=your_gmail@gmail.com
APP_PASSWORD=your_gmail_app_password
```

To generate a Gmail App Password: go to your Google Account → Security → 2-Step Verification → App Passwords.

**3. Add the URLs you want to monitor in `main.py`:**

```python
URLS = [
    "https://example.com",
    "https://another-site.com",
]
```

**4. Run the monitor:**

```bash
python main.py
```

## How It Works

On each scheduled run, the monitor loads all previously stored hashes from `hashes.json`. For every URL in the list it fetches the page, hashes the response content, and compares it against the stored hash. If the hashes differ, an email alert is sent. The hash and timestamp are updated after every check regardless of whether a change was detected. On the very first run, hashes are saved silently with no alert.

## Email Alert Format

**Subject:** Website Changed!

**Body:**
```
Change detected on: https://example.com
Detected at: 2025-04-11 09:00:00
```

## Dependencies

- `requests` — HTTP fetching
- `python-dotenv` — loading credentials from `.env`
- `apscheduler` — scheduling periodic checks

## Notes

- `hashes.json` is excluded from version control — it is generated automatically on first run
- Logs are written to `WebMonitor.log` with rotation to prevent unbounded file growth
- The monitor runs every 1 minute by default — adjust the `minutes` parameter in `main.py`

## License

MIT