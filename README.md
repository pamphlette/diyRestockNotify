# DIY Restock Notifier (Raspberry Pi Automation)

This is a *WIP automation tool* designed to run on a Raspberry Pi and monitor the availability of in-demand species from online retailers with no native restock notifications. When a plant of interest is back in stock, it sends a push notification to your phone:

- Automatically scrape selected plant store websites
- Collect + store data for store inventory for every scrape
- Notify the user via Pushover with a message and link
- (optional) Display the historical data on a dashboard

Notifications are sent via the Pushover API with the plant name and a direct link to the restocked item. The current setup is specific to one vendor, but can be easily extended by creating new scraper/parser pairs.

---

## Project Structure

- `mainPie.py`: Master script that coordinates scraping and notifications
- `notifications/`: Sends alerts via Pushover using `.env` credentials
- `scrapers/`: Handles webpage access, captcha solving, and raw HTML capture
- `scrapers/soupParsers/`: Store-specific parsers to collect data from saved HTML
- `scrapers/scrapes/`: Repository for raw HTML files (git-ignored)

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/{repo}

# 2. Navigate to the project folder
cd plantScraper

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
cp .env.example .env
```

Then edit `.env` and fill in your [Pushover API](https://pushover.net/apps) credentials:

```env
PUSHOVER_API=your_api_key
PUSHOVER_USER=your_user_key
```

```bash
# 5. Run the main script manually (for testing)
python mainPie.py
```

For automated use, schedule this script to run on your Raspberry Pi.

---

## Future Improvements

- [ ] Run it on the Pi
- [ ] Add support for multiple plant stores as needed
- [ ] Store scrape results in structured JSON or CSV
- [ ] Publish parsed data to a Plotly dashboard for other plant folks

---

## Contributions / Contact

This is a personal project to make grabbing the hot ticket species easier — feel free to fork or reach out. Built to grow out when I'm ready to expand inventory 😄