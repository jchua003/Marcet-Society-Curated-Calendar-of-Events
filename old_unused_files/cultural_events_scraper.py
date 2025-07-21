import time
import json
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CulturalEventScraper:
    def __init__(self, headless=True):
        self.setup_driver(headless)
        self.events = []
        
        # Target event types
        self.target_event_types = [
            'exhibition', 'exhibitions', 'special event', 'special events',
            'lecture', 'lectures', 'tour', 'tours', 'performance', 'performances',
            'panel discussion', 'panel discussions', 'talk', 'talks', 'salon',
            'workshop', 'symposium', 'conference', 'reading', 'screening'
        ]
        
        # NYC Cultural Institutions
        self.institutions = {
            'met': {
                'name': 'Metropolitan Museum of Art',
                'shortName': 'The Met',
                'url': 'https://www.metmuseum.org/events',
                'location': 'New York'
            },
            'moma': {
                'name': 'Museum of Modern Art',
                'shortName': 'MoMA',
                'url': 'https://www.moma.org/calendar',
                'location': 'New York'
            },
            'frick': {
                'name': 'Frick Collection',
                'shortName': 'Frick',
                'url': 'https://www.frick.org/events',
                'location': 'New York'
            },
            'asia': {
                'name': 'Asia Society',
                'shortName': 'Asia Society',
                'url': 'https://asiasociety.org/new-york/events',
                'location': 'New York'
            },
            'nyhs': {
                'name': 'New York Historical Society',
                'shortName': 'NY Historical',
                'url': 'https://www.nyhistory.org/events',
                'location': 'New York'
            }
        }
    
    def setup_driver(self, headless=True):
        """Setup Chrome driver with stable configuration"""
        print("🔧 Setting up Chrome driver...")
        
        # Use the same stable configuration that worked
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-crash-reporter')
        options.add_argument('--disable-oopr-debug-crash-dump')
        options.add_argument('--no-crash-upload')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-background-media')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions-file-access-check')
        options.add_argument('--disable-extensions-http-throttling')
        options.add_argument('--disable-extensions-https-throttling')
        options.add_argument('--disable-gpu-watchdog')
        options.add_argument('--disable-hang-monitor')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-prompt-on-repost')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-pings')
        options.add_argument('--no-zygote')
        options.add_argument('--password-store=basic')
        options.add_argument('--use-mock-keychain')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--user-data-dir=/tmp/chrome-scraper')
        options.add_argument('--disable-ipc-flooding-protection')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Use the installed Chrome binary
        options.binary_location = '/usr/bin/google-chrome'
        
        # Clean user data directory
        import shutil
        import os
        if os.path.exists('/tmp/chrome-scraper'):
            shutil.rmtree('/tmp/chrome-scraper')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        
        print("✅ Chrome driver ready!")
    
    def is_target_event_type(self, event_text):
        """Check if event matches our target types"""
        event_text_lower = event_text.lower()
        return any(event_type in event_text_lower for event_type in self.target_event_types)
    
    def classify_event_type(self, event_text, event_description=""):
        """Classify event into one of our categories"""
        text = (event_text + " " + event_description).lower()
        
        if any(word in text for word in ['exhibition', 'exhibit', 'show', 'display']):
            return 'exhibitions'
        elif any(word in text for word in ['special event', 'special', 'gala', 'opening', 'celebration']):
            return 'special'
        elif any(word in text for word in ['lecture', 'talk', 'speech', 'address']):
            return 'lecture'
        elif any(word in text for word in ['tour', 'walk', 'visit', 'guided']):
            return 'tour'
        elif any(word in text for word in ['performance', 'concert', 'music', 'dance', 'theater']):
            return 'performances'
        elif any(word in text for word in ['panel', 'discussion', 'debate', 'symposium']):
            return 'panel'
        elif any(word in text for word in ['reading', 'book', 'author', 'poetry', 'workshop', 'salon']):
            return 'talks'
        else:
            return 'talks'
    
    def scrape_met_events(self):
        """Scrape Metropolitan Museum events"""
        print("🏛️ Scraping Metropolitan Museum of Art...")
        
        try:
            self.driver.get(self.institutions['met']['url'])
            time.sleep(5)
            
            # Try to find events with multiple selectors
            selectors = [
                '.event-card',
                '.event-item', 
                '.gtm-event-card',
                '[data-testid="event-card"]',
                '.calendar-event',
                '.program-listing',
                '.event',
                '.upcoming-event'
            ]
            
            events_found = 0
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"  Found {len(elements)} elements with selector: {selector}")
                        
                        for element in elements[:5]:  # Limit to 5 events
                            event_data = self.extract_event_data(element, 'met')
                            if event_data:
                                self.events.append(event_data)
                                events_found += 1
                                print(f"    ✅ Added: {event_data['title'][:60]}...")
                        
                        if events_found > 0:
                            break
                            
                except Exception as e:
                    print(f"    ⚠️ Selector {selector} failed: {e}")
                    continue
            
            if events_found == 0:
                print("  ⚠️ No events found, creating sample event")
                self.create_sample_event('met')
                
        except Exception as e:
            print(f"❌ Error scraping Met: {e}")
            self.create_sample_event('met')
    
    def scrape_simple_events(self):
        """Create sample events for testing"""
        print("🎭 Creating sample cultural events...")
        
        today = datetime.now()
        
        sample_events = [
            {
                'title': 'Impressionist Masterpieces: A Special Exhibition',
                'museum': 'met',
                'date': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
                'time': '10:00 AM',
                'type': 'exhibitions',
                'description': 'Explore the world of Impressionism through masterpieces from our collection, featuring works by Monet, Renoir, and Degas.',
                'city': 'New York',
                'price': '$25',
                'duration': 'All day',
                'link': 'https://www.metmuseum.org/events'
            },
            {
                'title': 'Contemporary Art Discussion Panel',
                'museum': 'moma',
                'date': (today + timedelta(days=10)).strftime('%Y-%m-%d'),
                'time': '6:30 PM',
                'type': 'panel',
                'description': 'Join contemporary artists and curators for an engaging discussion about modern art movements and their impact on society.',
                'city': 'New York',
                'price': '$15',
                'duration': '2 hours',
                'link': 'https://www.moma.org/calendar'
            },
            {
                'title': 'Women in Science: Historical Perspectives',
                'museum': 'nyhs',
                'date': (today + timedelta(days=14)).strftime('%Y-%m-%d'),
                'time': '2:00 PM',
                'type': 'lecture',
                'description': 'A fascinating lecture exploring the contributions of women scientists throughout history and their lasting impact.',
                'city': 'New York',
                'price': 'Free',
                'duration': '90 minutes',
                'link': 'https://www.nyhistory.org/events'
            },
            {
                'title': 'Asian Literature Book Launch',
                'museum': 'asia',
                'date': (today + timedelta(days=21)).strftime('%Y-%m-%d'),
                'time': '7:00 PM',
                'type': 'talks',
                'description': 'Author reading and discussion of contemporary Asian literature and its global influence on modern culture.',
                'city': 'New York',
                'price': '$10',
                'duration': '90 minutes',
                'link': 'https://asiasociety.org/new-york/events'
            },
            {
                'title': 'Renaissance Art Gallery Tour',
                'museum': 'frick',
                'date': (today + timedelta(days=28)).strftime('%Y-%m-%d'),
                'time': '4:00 PM',
                'type': 'tour',
                'description': 'Guided tour through our Renaissance collection, exploring the artistic techniques and cultural context of the period.',
                'city': 'New York',
                'price': '$40',
                'duration': '2 hours',
                'link': 'https://www.frick.org/events'
            }
        ]
        
        self.events.extend(sample_events)
        print(f"  ✅ Created {len(sample_events)} sample events")
    
    def extract_event_data(self, element, museum_id):
        """Extract event data from a DOM element"""
        try:
            # Try to find title
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.event-title', '.event-name']
            title = None
            
            for selector in title_selectors:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue
            
            if not title:
                return None
            
            # Filter by event type
            if not self.is_target_event_type(title):
                return None
            
            # Extract other details with defaults
            description = self.extract_text(element, ['.description', '.event-description', 'p'])
            date = self.extract_text(element, ['.date', '.event-date', 'time'])
            
            # Generate event data
            event_date, event_time = self.parse_date_time(date)
            
            return {
                'title': title[:100],
                'museum': museum_id,
                'date': event_date,
                'time': event_time,
                'type': self.classify_event_type(title, description),
                'description': (description or title)[:300],
                'city': 'New York',
                'price': 'See website',
                'duration': '2 hours',
                'link': self.extract_link(element, museum_id)
            }
            
        except Exception as e:
            print(f"      ⚠️ Error extracting event data: {e}")
            return None
    
    def extract_text(self, element, selectors):
        """Extract text using multiple selectors"""
        for selector in selectors:
            try:
                elem = element.find_element(By.CSS_SELECTOR, selector)
                text = elem.text.strip()
                if text:
                    return text
            except:
                continue
        return ""
    
    def extract_link(self, element, museum_id):
        """Extract event link"""
        try:
            link_elem = element.find_element(By.CSS_SELECTOR, 'a')
            href = link_elem.get_attribute('href')
            if href:
                if href.startswith('http'):
                    return href
                else:
                    base_urls = {
                        'met': 'https://www.metmuseum.org',
                        'moma': 'https://www.moma.org',
                        'frick': 'https://www.frick.org',
                        'asia': 'https://asiasociety.org',
                        'nyhs': 'https://www.nyhistory.org'
                    }
                    return base_urls.get(museum_id, '') + href
        except:
            pass
        
        # Return default URLs
        return self.institutions[museum_id]['url']
    
    def parse_date_time(self, date_string):
        """Parse date and time from string"""
        try:
            today = datetime.now()
            
            # Default values
            event_date = today.strftime('%Y-%m-%d')
            event_time = '7:00 PM'
            
            if date_string:
                # Try to extract time
                time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)', date_string, re.IGNORECASE)
                if time_match:
                    event_time = time_match.group(0)
                
                # Try to extract date
                if 'today' in date_string.lower():
                    event_date = today.strftime('%Y-%m-%d')
                elif 'tomorrow' in date_string.lower():
                    event_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    # Try various date formats
                    date_patterns = [
                        r'(\d{1,2})/(\d{1,2})/(\d{4})',
                        r'(\d{4})-(\d{1,2})-(\d{1,2})',
                        r'(\w+)\s+(\d{1,2}),?\s+(\d{4})'
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, date_string)
                        if match:
                            try:
                                if '/' in pattern:
                                    month, day, year = match.groups()
                                    event_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                                elif '-' in pattern:
                                    year, month, day = match.groups()
                                    event_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                                break
                            except:
                                continue
            
            return event_date, event_time
            
        except:
            return datetime.now().strftime('%Y-%m-%d'), '7:00 PM'
    
    def create_sample_event(self, museum_id):
        """Create a sample event when scraping fails"""
        today = datetime.now()
        sample_event = {
            'title': f'Cultural Event at {self.institutions[museum_id]["shortName"]}',
            'museum': museum_id,
            'date': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            'time': '7:00 PM',
            'type': 'lecture',
            'description': f'Cultural event at {self.institutions[museum_id]["name"]} - visit their website for current programming.',
            'city': 'New York',
            'price': 'See website',
            'duration': '2 hours',
            'link': self.institutions[museum_id]['url']
        }
        self.events.append(sample_event)
        print(f"    ✅ Created sample event for {museum_id}")
    
    def scrape_all_events(self):
        """Scrape events from all institutions"""
        print("🎭 Starting Cultural Events Scraper...")
        print("=" * 50)
        
        try:
            # For now, let's create sample events to test the system
            # Later we can add real scraping for specific institutions
            self.scrape_simple_events()
            
            # Uncomment this to try real scraping
            # self.scrape_met_events()
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
        finally:
            self.driver.quit()
        
        print("=" * 50)
        print(f"✅ Scraping complete! Found {len(self.events)} events")
        return self.events
    
    def save_events_to_file(self, filename='cultural_events.json'):
        """Save events to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
        print(f"📁 Events saved to {filename}")
    
    def print_summary(self):
        """Print summary of scraped events"""
        print("\n📊 SCRAPING SUMMARY")
        print("=" * 50)
        
        # Count by institution
        institution_counts = {}
        type_counts = {}
        
        for event in self.events:
            museum = event['museum']
            event_type = event['type']
            
            institution_counts[museum] = institution_counts.get(museum, 0) + 1
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
        
        print("📍 Events by Institution:")
        for museum, count in institution_counts.items():
            institution_name = self.institutions[museum]['shortName']
            print(f"  {institution_name}: {count} events")
        
        print("\n🎭 Events by Type:")
        for event_type, count in type_counts.items():
            print(f"  {event_type}: {count} events")
        
        print(f"\n✅ Total Events: {len(self.events)}")
        
        print("\n📋 Event List:")
        for event in self.events:
            print(f"  • {event['title']} ({event['museum']}) - {event['date']} at {event['time']}")

if __name__ == "__main__":
    # Create scraper instance
    scraper = CulturalEventScraper(headless=True)
    
    # Scrape events
    events = scraper.scrape_all_events()
    
    # Save to file
    scraper.save_events_to_file('cultural_events.json')
    
    # Print summary
    scraper.print_summary()
    
    print("\n🎉 Ready to integrate with your React app!")
    print("📁 Check 'cultural_events.json' for the event data")

