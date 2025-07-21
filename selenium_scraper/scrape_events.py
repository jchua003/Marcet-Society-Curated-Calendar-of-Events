"""Example Selenium scraper for cultural institutions."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    # Basic flags for running in Docker/CI environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def parse_events(driver: webdriver.Chrome, url: str) -> None:
    """Placeholder parser that prints the page title."""
    driver.get(url)
    print(f"Fetched {driver.title} from {url}")
    # TODO: Extract event details here


def scrape_all(headless: bool = True):
    driver = setup_driver(headless=headless)
    institutions = {
        "met": "https://www.metmuseum.org/events",
        "moma": "https://www.moma.org/calendar",
        "albertine": "https://www.albertine.com/events",
    }
    for name, url in institutions.items():
        parse_events(driver, url)
    driver.quit()


if __name__ == "__main__":
    scrape_all(headless=True)
