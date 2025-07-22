# Marcet-Society-Curated-Calendar-of-Events
Curated Calendar of Events in Major U.S. Cities with Google Calendar Integration

## Setup

Install Python dependencies used by the scraper utilities:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file currently lists `selenium` and
`webdriver-manager` which are required for running the Selenium based
scripts under `old_unused_files/`.

When deploying events, the integration scripts look for
`cultural_events.json` first and fall back to `csv_based_events.json`
if present.
