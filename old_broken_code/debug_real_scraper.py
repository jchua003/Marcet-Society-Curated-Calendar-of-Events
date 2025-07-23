import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class DebugScraper:
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """Setup Chrome driver"""
        print("🔧 Setting up Chrome driver...")
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.binary_location = '/usr/bin/google-chrome'
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(5)
            print("✅ Chrome driver ready!")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
    def debug_institution(self, name, url):
        """Debug what we can find on a specific institution page"""
        print(f"\n🔍 DEBUGGING: {name}")
        print(f"📡 URL: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            # Get page title
            page_title = self.driver.title
            print(f"📄 Page title: {page_title}")
            
            # Check if page loaded properly
            page_source_length = len(self.driver.page_source)
            print(f"📏 Page source length: {page_source_length} characters")
            
            # Try to find common event-related elements
            selectors_to_try = [
                '.event', '.event-card', '.event-item', '.program', '.program-item',
                '.calendar-item', '.exhibition', '.upcoming-event', '.gtm-event-card',
                'h3', 'h2', '[class*="event"]', '[class*="program"]', '[class*="calendar"]'
            ]
            
            print(f"🔍 Searching for elements...")
            for selector in selectors_to_try:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"   ✅ Found {len(elements)} elements with '{selector}'")
                        
                        # Show first few elements
                        for i, elem in enumerate(elements[:3]):
                            try:
                                text = elem.text.strip()[:100]
                                if text:
                                    print(f"      {i+1}: {text}...")
                            except:
                                print(f"      {i+1}: [Could not get text]")
                    else:
                        print(f"   ❌ No elements found with '{selector}'")
                except Exception as e:
                    print(f"   ⚠️ Error with '{selector}': {e}")
            
            # Look for any links that might be events
            all_links = self.driver.find_elements(By.CSS_SELECTOR, 'a')
            event_like_links = []
            for link in all_links[:20]:  # Check first 20 links
                try:
                    text = link.text.strip()
                    href = link.get_attribute('href')
                    if text and any(word in text.lower() for word in ['exhibition', 'event', 'lecture', 'talk', 'tour']):
                        event_like_links.append((text[:50], href))
                except:
                    continue
            
            if event_like_links:
                print(f"🔗 Found {len(event_like_links)} event-like links:")
                for text, href in event_like_links[:5]:
                    print(f"   • {text}: {href}")
            else:
                print("🔗 No event-like links found")
                
        except Exception as e:
            print(f"❌ Error debugging {name}: {e}")
    
    def debug_all_institutions(self):
        """Debug multiple institutions"""
        institutions = [
            ("The Met", "https://www.metmuseum.org/events"),
            ("MoMA", "https://www.moma.org/calendar"),
            ("Frick Collection", "https://www.frick.org/events"),
            ("Asia Society", "https://asiasociety.org/new-york/events"),
            ("NY Historical Society", "https://www.nyhistory.org/events")
        ]
        
        if not self.setup_driver():
            return
        
        try:
            for name, url in institutions:
                self.debug_institution(name, url)
                time.sleep(3)
                
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = DebugScraper()
    scraper.debug_all_institutions()

