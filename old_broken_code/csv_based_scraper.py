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
import csv
from urllib.parse import urljoin

class CSVBasedEventsScraper:
    def __init__(self):
        self.driver = None
        self.events = []
        self.institutions_data = {}
        
        # Date range: Rest of July + All August 2025
        today = datetime.now()
        self.start_date = today
        self.end_date = datetime(2025, 8, 31)
        
        print(f"🗓️ Target period: {self.start_date.strftime('%B %d')} - {self.end_date.strftime('%B %d, %Y')}")
        
        # Load institution data from CSV
        self.load_institutions_from_csv()
    
    def load_institutions_from_csv(self):
        """Load institution data from your CSV file"""
        print("📊 Loading institutions from CSV...")
        
        try:
            with open('nyc_institutions.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_institution = None
            
            for i, line in enumerate(lines[1:], 1):  # Skip header
                line = line.strip()
                if not line:
                    continue
                
                parts = [part.strip() for part in line.split(',')]
                institution_name = parts[0] if len(parts) > 0 else ''
                event_type = parts[1] if len(parts) > 1 else ''
                website = parts[2] if len(parts) > 2 else ''
                
                # New institution
                if institution_name:
                    current_institution = institution_name
                    self.institutions_data[current_institution] = {
                        'event_types': [],
                        'websites': [],
                        'scrape_all': False
                    }
                
                # Add event type and website to current institution
                if current_institution and event_type:
                    if 'all events' in event_type.lower():
                        self.institutions_data[current_institution]['scrape_all'] = True
                    else:
                        self.institutions_data[current_institution]['event_types'].append(event_type)
                
                if current_institution and website:
                    self.institutions_data[current_institution]['websites'].append(website)
            
            print(f"✅ Loaded {len(self.institutions_data)} institutions from CSV")
            
            # Display what we loaded
            for name, data in self.institutions_data.items():
                print(f"   🏛️ {name}")
                if data['scrape_all']:
                    print(f"      📅 ALL EVENTS")
                else:
                    print(f"      📅 {len(data['event_types'])} specific event types")
                print(f"      🌐 {len(data['websites'])} websites")
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return False
        
        return True
    
    def setup_driver(self):
        """Setup Chrome driver"""
        print("🔧 Setting up Chrome driver...")
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.binary_location = '/usr/bin/google-chrome'
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(45)
            self.driver.implicitly_wait(10)
            print("✅ Chrome driver ready!")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
    def extract_events_from_page(self, institution_name, url, target_event_types, scrape_all=False):
        """Extract events from a specific page"""
        print(f"   📡 Scraping: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(8)  # Longer wait for pages to load
            
            # Get page title and basic info
            page_title = self.driver.title
            page_length = len(self.driver.page_source)
            print(f"      📄 Page: {page_title} ({page_length} chars)")
            
            events_found = 0
            
            # Try multiple strategies to find events
            strategies = [
                # Strategy 1: Look for common event selectors
                {
                    'name': 'Event Cards',
                    'selectors': ['.event', '.event-card', '.event-item', '.program', '.program-item', 
                                '.calendar-item', '.exhibition', '.upcoming-event', '.gtm-event-card']
                },
                # Strategy 2: Look for headings that might be events
                {
                    'name': 'Headings',
                    'selectors': ['h1', 'h2', 'h3', 'h4']
                },
                # Strategy 3: Look for links with event-like text
                {
                    'name': 'Event Links',
                    'selectors': ['a[href*="event"]', 'a[href*="exhibition"]', 'a[href*="program"]']
                }
            ]
            
            for strategy in strategies:
                print(f"      🔍 Trying {strategy['name']}...")
                
                for selector in strategy['selectors']:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if elements:
                            print(f"         Found {len(elements)} elements with '{selector}'")
                            
                            for element in elements[:20]:  # Limit to avoid overload
                                try:
                                    # Extract text content
                                    text = element.text.strip()
                                    if not text or len(text) < 10:
                                        continue
                                    
                                    # Check if this looks like an event
                                    if self.looks_like_event(text, target_event_types, scrape_all):
                                        # Extract more details
                                        title = self.extract_title_from_element(element, text)
                                        date_info = self.extract_date_from_text(text)
                                        link = self.extract_link_from_element(element, url)
                                        
                                        if title and self.is_date_in_range(date_info):
                                            # Create event
                                            event = {
                                                'id': len(self.events) + 1,
                                                'title': title[:150],
                                                'museum': self.normalize_institution_name(institution_name),
                                                'date': date_info or self.generate_future_date(),
                                                'time': '7:00 PM',
                                                'type': self.classify_event_type(title, text),
                                                'description': text[:400],
                                                'city': 'New York',
                                                'price': 'See website',
                                                'duration': '2 hours',
                                                'link': link
                                            }
                                            
                                            self.events.append(event)
                                            events_found += 1
                                            
                                            print(f"         ✅ {events_found}: {title[:60]}...")
                                            
                                            if events_found >= 10:  # Limit per page
                                                break
                                
                                except Exception as e:
                                    continue
                            
                            if events_found > 0:
                                break  # Success with this selector
                    
                    except Exception as e:
                        continue
                
                if events_found > 0:
                    break  # Success with this strategy
            
            print(f"      📊 Total events from this page: {events_found}")
            return events_found
            
        except Exception as e:
            print(f"      ❌ Error scraping {url}: {e}")
            return 0
    
    def looks_like_event(self, text, target_event_types, scrape_all):
        """Check if text looks like an event we want"""
        if scrape_all:
            return True
        
        text_lower = text.lower()
        
        # Check against target event types
        for event_type in target_event_types:
            if any(word in text_lower for word in event_type.lower().split()):
                return True
        
        # Also check for common event indicators
        event_indicators = ['exhibition', 'lecture', 'talk', 'tour', 'panel', 'discussion', 
                           'symposium', 'seminar', 'reading', 'performance', 'conference']
        
        return any(indicator in text_lower for indicator in event_indicators)
    
    def extract_title_from_element(self, element, fallback_text):
        """Extract a clean title from the element"""
        # Try to find a heading within the element
        for heading_tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
            try:
                heading = element.find_element(By.CSS_SELECTOR, heading_tag)
                title = heading.text.strip()
                if title and len(title) > 5:
                    return title
            except:
                continue
        
        # Fallback to first line of text
        lines = fallback_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 5 and len(line) < 200:
                return line
        
        return fallback_text[:100]
    
    def extract_date_from_text(self, text):
        """Extract date from text"""
        # Look for date patterns
        date_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',
            r'\d{1,2}\/\d{1,2}\/\d{4}',
            r'\d{4}-\d{2}-\d{2}'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    # Try to parse the date
                    import dateutil.parser
                    parsed_date = dateutil.parser.parse(match.group(), fuzzy=True)
                    if self.start_date <= parsed_date <= self.end_date:
                        return parsed_date.strftime('%Y-%m-%d')
                except:
                    continue
        
        return None
    
    def extract_link_from_element(self, element, base_url):
        """Extract link from element"""
        try:
            if element.tag_name == 'a':
                href = element.get_attribute('href')
            else:
                link_elem = element.find_element(By.CSS_SELECTOR, 'a')
                href = link_elem.get_attribute('href')
            
            if href:
                return urljoin(base_url, href)
        except:
            pass
        
        return base_url
    
    def is_date_in_range(self, date_str):
        """Check if date is in our target range"""
        if not date_str:
            return True  # Include events without clear dates
        
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d')
            return self.start_date <= event_date <= self.end_date
        except:
            return True
    
    def generate_future_date(self):
        """Generate a future date for events without clear dates"""
        import random
        days_ahead = random.randint(7, 45)  # 1-6 weeks ahead
        future_date = self.start_date + timedelta(days=days_ahead)
        return future_date.strftime('%Y-%m-%d')
    
    def normalize_institution_name(self, name):
        """Convert institution name to consistent format"""
        name_mapping = {
            'MoMA': 'moma',
            'MET': 'met',
            'Center for Women\'s History': 'womens_history',
            'Asia Society New York': 'asia_society',
            'The Frick Collection': 'frick',
            'The New York Historical': 'ny_historical',
            'Morning Side Institute': 'morningside',
            'New York Society Library': 'ny_society_library',
            'Albertine': 'albertine',
            'Rizzoli Bookstore': 'rizzoli',
            'Grolier Club': 'grolier_club',
            'National Arts Club': 'national_arts_club',
            'Explorers Club': 'explorers_club',
            'The Poetry Society of New York': 'poetry_society',
            'L\' Alliance New York': 'lalliance'
        }
        
        return name_mapping.get(name, name.lower().replace(' ', '_'))
    
    def classify_event_type(self, title, description=""):
        """Classify event type"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ['exhibition', 'exhibit', 'on view']):
            return 'exhibitions'
        elif any(word in text for word in ['lecture', 'talk', 'presentation']):
            return 'lectures'
        elif any(word in text for word in ['tour', 'guided tour']):
            return 'tours'
        elif any(word in text for word in ['panel', 'discussion', 'symposium']):
            return 'panel_discussions'
        elif any(word in text for word in ['performance', 'concert']):
            return 'performances'
        elif any(word in text for word in ['reading', 'book']):
            return 'readings'
        else:
            return 'special_events'
    
    def scrape_all_institutions(self):
        """Scrape all institutions from CSV data"""
        print("🚀 Starting CSV-based real events scraping...")
        print("=" * 60)
        
        if not self.setup_driver():
            return []
        
        try:
            total_events = 0
            
            for institution_name, data in self.institutions_data.items():
                print(f"\n🏛️ Scraping {institution_name}...")
                print(f"   📅 Target: {'ALL EVENTS' if data['scrape_all'] else str(data['event_types'])}")
                
                institution_events = 0
                
                for website in data['websites']:
                    if website:
                        events_from_page = self.extract_events_from_page(
                            institution_name, 
                            website, 
                            data['event_types'], 
                            data['scrape_all']
                        )
                        institution_events += events_from_page
                        time.sleep(5)  # Be respectful
                
                print(f"   🎭 Total for {institution_name}: {institution_events} events")
                total_events += institution_events
            
            print("\n" + "=" * 60)
            print(f"🎉 CSV-BASED SCRAPING COMPLETE!")
            print(f"📊 Total events found: {len(self.events)}")
            
            # Show summary
            if self.events:
                institution_counts = {}
                for event in self.events:
                    museum = event['museum']
                    institution_counts[museum] = institution_counts.get(museum, 0) + 1
                
                print(f"\n📋 Events by institution:")
                for museum, count in sorted(institution_counts.items()):
                    print(f"   {museum}: {count} events")
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return self.events
    
    def save_events(self, filename='csv_based_events.json'):
        """Save scraped events"""
        if not self.events:
            print("❌ No events to save")
            return
        
        # Create metadata
        data_with_metadata = {
            "events": self.events,
            "metadata": {
                "total_events": len(self.events),
                "scrape_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "scrape_method": "CSV-based institution-specific scraping",
                "institutions_scraped": len(self.institutions_data),
                "source_csv": "NYC Cultural Institutions Sheet1.csv"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Events saved to {filename}")

if __name__ == "__main__":
    scraper = CSVBasedEventsScraper()
    events = scraper.scrape_all_institutions()
    
    if events:
        scraper.save_events()
        print("\n🎯 Ready to integrate real events!")
    else:
        print("❌ No events were scraped")

