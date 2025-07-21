# Selenium Scraper

This folder contains scripts that use **Selenium** and **webdriver-manager** to automatically gather event information from supported institutions.

## Setup

Install the Python dependencies (if you haven't already):

```bash
pip install -r ../requirements.txt
```

## Usage

Run the example scraper which fetches events from a list of institutions:

```bash
python scrape_events.py
```

The script currently prints the page title for each institution as a placeholder. You can extend the `parse_events` function to extract specific event data.
