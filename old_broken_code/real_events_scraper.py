import time
import json
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import dateutil.parser
from urllib.parse import urljoin

class RealEventsScraperPro:
    def __init__(self):
        self.driver = None
        self.events = []
        self.target_event_types = [
            'exhibitions', 'special events', 'lectures', 'tours', 
            'symposia', 'panel discussions', 'artist talks', 'gallery talks'
        ]
        
        # Define date range: Rest of July + All August
        today = datetime.now()
        self.start_date = today.replace(day=today.day)  # From today
        self.end_date = datetime(2025, 8, 31)  # End of August
        
        print(f"🗓️ Scraping events from {self.start_date.strftime('%B %d')} to {self.end_date.strftime('%B %d, %Y')}")
        
        # Institution configurations with real URLs and selectors
        self.institutions = {
            'met': {
                'name': 'The Met',
                'urls': [
                    'https://www.metmuseum.org/events/exhibitions',
                    'https://www.metmuseum.org/events/lectures',
                    'https://www.metmuseum.org/events/talks'
                ],
                'selectors': {
                    'event_cards': ['.gtm-event-card', '.event-card', '.program-item'],
                    'title': ['h3', 'h2', '.event-title', '.title'],
                    'date': ['.date', '.event-date', 'time', '.datetime'],
                    'description': ['.description', '.summary', 'p'],
                    'link': ['a']
                }
            },
            'moma': {
                'name': 'MoMA',
                'urls': [
                    'https://www.moma.org/calendar/exhibitions',
                    'https://www.moma.org/calendar/events'
                ],
                'selectors': {
                    'event_cards': ['.calendar-item', '.exhibition-item', '.event-card'],
                    'title': ['h3', 'h2', '.title'],
                    'date': ['.date', '.dates', 'time'],
                    'description': ['.description', '.summary'],
                    'link': ['a']
                }
            },
            'frick': {
                'name': 'Frick Collection',
                'urls': ['https://www.frick.org/events'],
                'selectors': {
                    'event_cards': ['.event', '.program', '.upcoming-event'],
                    'title': ['h3', 'h2', '.event-title'],
                    'date': ['.date', '.event-date'],
                    'description': ['.description', '.summary'],
                    'link': ['a']
                }
            },
            'asia_society': {
                'name': 'Asia Society',
                'urls': ['https://asiasociety.org/new-york/events'],
                'selectors': {
                    'event_cards': ['.event-item', '.program-item'],
                    'title': ['h3', 'h2', '.title'],
                    'date': ['.date', '.event-date'],
                    'description': ['.description', '.excerpt'],
                    'link': ['a']
                }
            },
            'ny_historical': {
                'name': 'NY Historical Society',
                'urls': ['https://www.nyhistory.org/events'],
                'selectors': {
                    'event_cards': ['.event', '.program-listing'],
                    'title': ['h3', 'h2', '.event-title'],
                    'date': ['.date', '.event-date'],
                    'description': ['.description', '.summary'],
                    'link': ['a']
                }
            },
            'ny_society_library': {
                'name': 'NY Society Library',
                'urls': ['https://www.nysoclib.org/events'],
                'selectors': {
                    'event_cards': ['.event', '.program'],
                    'title': ['h3', 'h2', '.title'],
                    'date': ['.date', '.event-date'],
                    'description': ['.description', '.content'],
                    'link': ['a']
                }
            },
            'grolier_club': {
                'name': 'Grolier Club',
                'urls': ['https://www.grolierclub.org/events'],
                'selectors': {
                    'event_cards': ['.event', '.exhibition', '.program'],
                    'title': ['h3', 'h2', '.title'],
                    'date': ['.date', '.dates'],
                    'description': ['.description', '.summary'],
                    'link': ['a']
                }
            },
            'americas_society': {
                'name': 'Americas Society',
                'urls': ['https://www.as-coa.org/events'],
                'selectors': {
                    'event_cards': ['.event', '.program'],
                    'title': ['h3', 'h2', '.title'],
                    'date': ['.date', '.event-date'],
                    'description': ['.description', '.summary'],
                    'link': ['a']
                }
            }
        }
    
    def setup_driver(self):
        """Setup Chrome driver for scraping"""
        print("🔧 Setting up Chrome driver for real event scraping...")
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-images')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.binary_location = '/usr/bin/google-chrome'
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            print("✅ Chrome driver ready for real scraping!")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
    def extract_text_safely(self, element, selectors):
        """Safely extract text using multiple selector options"""
        for selector in selectors:
            try:
                elem = element.find_element(By.CSS_SELECTOR, selector)
                text = elem.text.strip()
                if text:
                    return text
            except:
                continue
        return ""
    
    def extract_link_safely(self, element, base_url):
        """Extract event link safely"""
        try:
            link_elem = element.find_element(By.CSS_SELECTOR, 'a')
            href = link_elem.get_attribute('href')
            if href:
                return urljoin(base_url, href)
        except:
            pass
        return base_url
    
    def parse_date_intelligently(self, date_string):
        """Parse dates intelligently from various formats"""
        if not date_string:
            return None
            
        try:
            # Common patterns to clean up
            date_string = re.sub(r'(On view|Through|Ongoing|Opens|Closes)', '', date_string, flags=re.IGNORECASE)
            date_string = re.sub(r'[–—-].*$', '', date_string)  # Remove end dates
            date_string = date_string.strip()
            
            # Try to parse with dateutil
            parsed_date = dateutil.parser.parse(date_string, fuzzy=True)
            
            # Check if date is in our target range
            if self.start_date <= parsed_date <= self.end_date:
                return parsed_date.strftime('%Y-%m-%d')
        except:
            pass
        
        return None
    
    def classify_event_type_intelligently(self, title, description=""):
        """Classify event type based on title and description"""
        text = (title + " " + description).lower()
        
        # More sophisticated classification
        if any(word in text for word in ['exhibition', 'exhibit', 'on view', 'gallery', 'installation']):
            return 'exhibitions'
        elif any(word in text for word in ['artist talk', 'artist discussion', 'artist conversation']):
            return 'artist_talks'
        elif any(word in text for word in ['gallery talk', 'gallery tour']):
            return 'gallery_talks'
        elif any(word in text for word in ['panel', 'panel discussion', 'symposium', 'symposia']):
            return 'panel_discussions'
        elif any(word in text for word in ['lecture', 'talk', 'presentation']):
            return 'lectures'
        elif any(word in text for word in ['tour', 'guided tour', 'walking tour']):
            return 'tours'
        elif any(word in text for word in ['special event', 'celebration', 'opening', 'reception']):
            return 'special_events'
        else:
            return 'lectures'  # Default fallback
    
    def is_target_event_type(self, event_type):
        """Check if event type is in our target list"""
        return any(target in event_type.lower() for target in [
            'exhibition', 'special event', 'lecture', 'tour', 
            'symposia', 'panel discussion', 'artist talk', 'gallery talk'
        ])
    
    def scrape_institution_real_events(self, institution_id):
        """Scrape real events from institution"""
        institution = self.institutions[institution_id]
        print(f"\n🏛️ Scraping REAL events from {institution['name']}...")
        
        events_found = 0
        
        for url in institution['urls']:
            print(f"   📡 Checking: {url}")
            
            try:
                self.driver.get(url)
                time.sleep(5)  # Wait for page load
                
                # Try different event card selectors
                for card_selector in institution['selectors']['event_cards']:
                    try:
                        events = self.driver.find_elements(By.CSS_SELECTOR, card_selector)
                        print(f"      Found {len(events)} potential events with '{card_selector}'")
                        
                        for event_elem in events[:15]:  # Limit per selector
                            try:
                                # Extract event details
                                title = self.extract_text_safely(event_elem, institution['selectors']['title'])
                                date_text = self.extract_text_safely(event_elem, institution['selectors']['date'])
                                description = self.extract_text_safely(event_elem, institution['selectors']['description'])
                                link = self.extract_link_safely(event_elem, url)
                                
                                if not title or len(title) < 5:
                                    continue
                                
                                # Parse and validate date
                                parsed_date = self.parse_date_intelligently(date_text)
                                if not parsed_date:
                                    continue
                                
                                # Classify event type
                                event_type = self.classify_event_type_intelligently(title, description)
                                
                                # Check if it's a target event type
                                if not self.is_target_event_type(event_type):
                                    continue
                                
                                # Create event object
                                event = {
                                    'id': len(self.events) + 1,
                                    'title': title[:100],
                                    'museum': institution_id,
                                    'date': parsed_date,
                                    'time': '7:00 PM',  # Default time, could be improved
                                    'type': event_type,
                                    'description': description[:300] if description else title,
                                    'city': 'New York',
                                    'price': 'See website',
                                    'duration': '2 hours',
                                    'link': link
                                }
                                
                                self.events.append(event)
                                events_found += 1
                                
                                print(f"      ✅ {events_found}: {title[:50]}...")
                                
                            except Exception as e:
                                continue
                        
                        if events_found > 0:
                            break  # Success with this selector
                            
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"      ❌ Error with {url}: {e}")
                continue
        
        print(f"   🎭 Total real events from {institution['name']}: {events_found}")
        return events_found
    
    def scrape_all_real_events(self):
        """Scrape real events from all institutions"""
        print("🚀 Starting REAL EVENTS scraping from NYC cultural institutions...")
        print("=" * 70)
        
        if not self.setup_driver():
            return []
        
        try:
            total_events = 0
            
            for institution_id in self.institutions.keys():
                events_count = self.scrape_institution_real_events(institution_id)
                total_events += events_count
                time.sleep(3)  # Be respectful to servers
            
            print("\n" + "=" * 70)
            print(f"🎉 REAL EVENTS SCRAPING COMPLETE!")
            print(f"📊 Total real events found: {len(self.events)}")
            print(f"🏛️ Institutions scraped: {len(self.institutions)}")
            
            # Show summary by type
            type_counts = {}
            for event in self.events:
                event_type = event['type']
                type_counts[event_type] = type_counts.get(event_type, 0) + 1
            
            print(f"\n📋 Events by type:")
            for event_type, count in sorted(type_counts.items()):
                print(f"   {event_type}: {count} events")
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return self.events
    
    def save_real_events(self, filename='real_cultural_events.json'):
        """Save real events with metadata"""
        if not self.events:
            print("❌ No events to save")
            return
        
        # Calculate metadata
        institution_counts = {}
        type_counts = {}
        
        for event in self.events:
            museum = event.get('museum', 'unknown')
            event_type = event.get('type', 'unknown')
            
            institution_counts[museum] = institution_counts.get(museum, 0) + 1
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
        
        # Create enhanced data structure
        data_with_metadata = {
            "events": self.events,
            "metadata": {
                "total_events": len(self.events),
                "scrape_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "scrape_period": f"{self.start_date.strftime('%B %d')} - {self.end_date.strftime('%B %d, %Y')}",
                "institutions_scraped": len(institution_counts),
                "target_event_types": self.target_event_types,
                "events_by_institution": institution_counts,
                "events_by_type": type_counts,
                "scraper_version": "Real Events Scraper Pro v1.0"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Real events saved to {filename}")
        
        # Display summary
        print(f"\n📊 REAL EVENTS SUMMARY:")
        print(f"🎭 Total Events: {len(self.events)}")
        print(f"🏛️ Institutions: {len(institution_counts)}")
        for museum, count in institution_counts.items():
            print(f"   • {museum}: {count} events")

if __name__ == "__main__":
    scraper = RealEventsScraperPro()
    real_events = scraper.scrape_all_real_events()
    
    if real_events:
        scraper.save_real_events()
        print("\n🎯 Ready to integrate real events with your React app!")
        print("📁 Check 'real_cultural_events.json' for actual event data")
    else:
        print("❌ No real events were scraped")

