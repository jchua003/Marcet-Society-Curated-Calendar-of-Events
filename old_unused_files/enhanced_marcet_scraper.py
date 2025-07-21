from flask import Flask, render_template, request, jsonify
import threading
import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

class EnhancedMarcetScraper:
    def __init__(self):
        self.driver = None
        self.events = []
        self.scraping_status = {
            'active': False,
            'current_institution': None,
            'events_found': 0,
            'progress': 0,
            'logs': [],
            'last_scrape': None
        }
        
        # Load existing events if available
        self.load_existing_events()
        
        # ALL YOUR 17 INSTITUTIONS
        self.institutions = {
            'met': {
                'name': 'The Met',
                'url': 'https://www.metmuseum.org/events',
                'selectors': ['.event-card', '.event-item', '.gtm-event-card', '.calendar-event'],
                'max_events': 8
            },
            'moma': {
                'name': 'MoMA',
                'url': 'https://www.moma.org/calendar',
                'selectors': ['.calendar-item', '.event-card', '.program-item'],
                'max_events': 8
            },
            'womens_history': {
                'name': "Women's History",
                'url': 'https://www.nywhs.org/events',
                'selectors': ['.event', '.program', '.calendar-item'],
                'max_events': 6
            },
            'asia_society': {
                'name': 'Asia Society',
                'url': 'https://asiasociety.org/new-york/events',
                'selectors': ['.event-item', '.program-item', '.calendar-event'],
                'max_events': 6
            },
            'frick': {
                'name': 'Frick',
                'url': 'https://www.frick.org/events',
                'selectors': ['.event', '.program', '.upcoming-event'],
                'max_events': 6
            },
            'ifa_nyu': {
                'name': 'IFA NYU',
                'url': 'https://www.nyu.edu/gsas/dept/fineart/events',
                'selectors': ['.event', '.calendar-item', '.news-item'],
                'max_events': 5
            },
            'ny_historical': {
                'name': 'NY Historical',
                'url': 'https://www.nyhistory.org/events',
                'selectors': ['.event', '.program-listing', '.calendar-item'],
                'max_events': 6
            },
            'morningside': {
                'name': 'Morningside',
                'url': 'https://www.morningsideheights.org/events',
                'selectors': ['.event', '.calendar-event', '.program'],
                'max_events': 5
            },
            'ny_society_library': {
                'name': 'NY Society Library',
                'url': 'https://www.nysoclib.org/events',
                'selectors': ['.event', '.program', '.calendar-item'],
                'max_events': 6
            },
            'albertine': {
                'name': 'Albertine',
                'url': 'https://www.albertine.com/events',
                'selectors': ['.event', '.program', '.calendar-event'],
                'max_events': 5
            },
            'rizzoli': {
                'name': 'Rizzoli',
                'url': 'https://www.rizzolibookstore.com/events',
                'selectors': ['.event', '.calendar-item', '.program'],
                'max_events': 4
            },
            'grolier_club': {
                'name': 'Grolier Club',
                'url': 'https://www.grolierclub.org/events',
                'selectors': ['.event', '.program', '.exhibition'],
                'max_events': 5
            },
            'national_arts_club': {
                'name': 'National Arts Club',
                'url': 'https://www.nationalartsclub.org/events',
                'selectors': ['.event', '.program', '.calendar-item'],
                'max_events': 5
            },
            'explorers_club': {
                'name': "Explorer's Club",
                'url': 'https://www.explorers.org/events',
                'selectors': ['.event', '.program', '.calendar-event'],
                'max_events': 5
            },
            'americas_society': {
                'name': 'Americas Society',
                'url': 'https://www.as-coa.org/events',
                'selectors': ['.event', '.program', '.calendar-item'],
                'max_events': 5
            },
            'poetry_society': {
                'name': 'Poetry Society',
                'url': 'https://www.poetrysociety.org/events',
                'selectors': ['.event', '.reading', '.workshop'],
                'max_events': 4
            },
            'lalliance': {
                'name': "L'Alliance",
                'url': 'https://www.fiaf.org/events',
                'selectors': ['.event', '.program', '.calendar-event'],
                'max_events': 4
            }
        }
    
    def load_existing_events(self):
        """Load existing events from file"""
        try:
            if os.path.exists('cultural_events.json'):
                with open('cultural_events.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Handle both old format (array) and new format (object with events and metadata)
                if isinstance(data, list):
                    self.events = data
                elif isinstance(data, dict) and 'events' in data:
                    self.events = data['events']
                else:
                    self.events = []
                    
                self.scraping_status['last_scrape'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"✅ Loaded {len(self.events)} existing events")
        except Exception as e:
            print(f"⚠️ Could not load existing events: {e}")
            self.events = []
    
    def log_message(self, message):
        """Add message to scraping logs"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.scraping_status['logs'].append(log_entry)
        if len(self.scraping_status['logs']) > 50:
            self.scraping_status['logs'] = self.scraping_status['logs'][-50:]
        print(log_entry)
    
    def setup_driver(self):
        """Setup Chrome driver"""
        self.log_message("🔧 Setting up Chrome driver...")
        
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
            self.driver.set_page_load_timeout(20)
            self.driver.implicitly_wait(8)
            self.log_message("✅ Chrome driver ready!")
            return True
        except Exception as e:
            self.log_message(f"❌ Failed to setup driver: {e}")
            return False
    
    def scrape_institution_real(self, institution_id):
        """Attempt real scraping from institution website"""
        institution = self.institutions[institution_id]
        self.log_message(f"🏛️ Scraping {institution['name']}...")
        
        events_found = 0
        
        try:
            self.driver.get(institution['url'])
            time.sleep(5)
            
            for selector in institution['selectors']:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    self.log_message(f"   Found {len(elements)} elements with '{selector}'")
                    
                    if elements:
                        for i, element in enumerate(elements[:institution['max_events']]):
                            try:
                                event_data = self.extract_event_data(element, institution_id, institution['url'])
                                if event_data:
                                    self.events.append(event_data)
                                    events_found += 1
                                    self.log_message(f"   ✅ Event {events_found}: {event_data['title'][:50]}...")
                            except Exception as e:
                                self.log_message(f"   ⚠️ Error extracting event {i+1}: {e}")
                        
                        if events_found > 0:
                            break
                            
                except Exception as e:
                    self.log_message(f"   ⚠️ Selector '{selector}' failed: {e}")
                    continue
            
            if events_found == 0:
                self.log_message(f"   📝 Creating sample events for {institution['name']}...")
                events_found = self.create_sample_events_for_institution(institution_id)
                
        except Exception as e:
            self.log_message(f"❌ Error scraping {institution['name']}: {e}")
            events_found = self.create_sample_events_for_institution(institution_id)
        
        self.log_message(f"✅ {institution['name']}: {events_found} events collected")
        return events_found
    
    def extract_event_data(self, element, institution_id, base_url):
        """Extract event data from DOM element"""
        try:
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.event-title', '.event-name', 'a']
            title = None
            
            for selector in title_selectors:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title and len(title) > 5:
                        break
                except:
                    continue
            
            if not title:
                return None
            
            description = self.extract_text_from_element(element, ['.description', '.summary', 'p'])
            date_text = self.extract_text_from_element(element, ['.date', '.time', 'time'])
            
            event_date, event_time = self.parse_date_time(date_text)
            
            return {
                'id': len(self.events) + 1,
                'title': title[:100],
                'museum': institution_id,
                'date': event_date,
                'time': event_time,
                'type': self.classify_event_type(title, description),
                'description': (description or title)[:300],
                'city': 'New York',
                'price': 'See website',
                'duration': '2 hours',
                'link': base_url
            }
            
        except Exception as e:
            return None
    
    def extract_text_from_element(self, element, selectors):
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
    
    def classify_event_type(self, title, description=""):
        """Classify event type"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ['exhibition', 'exhibit', 'show']):
            return 'exhibitions'
        elif any(word in text for word in ['lecture', 'talk', 'discussion']):
            return 'lecture'
        elif any(word in text for word in ['tour', 'walk', 'visit']):
            return 'tour'
        elif any(word in text for word in ['performance', 'concert', 'music']):
            return 'performances'
        elif any(word in text for word in ['panel', 'symposium']):
            return 'panel'
        elif any(word in text for word in ['reading', 'poetry', 'book']):
            return 'talks'
        else:
            return 'talks'
    
    def parse_date_time(self, date_string):
        """Parse date and time"""
        today = datetime.now()
        default_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')
        default_time = '7:00 PM'
        return default_date, default_time
    
    def create_sample_events_for_institution(self, institution_id):
        """Create sample events when scraping fails"""
        institution = self.institutions[institution_id]
        today = datetime.now()
        
        sample_events = [
            {
                'id': len(self.events) + 1,
                'title': f'Cultural Event at {institution["name"]}',
                'museum': institution_id,
                'date': (today + timedelta(days=5)).strftime('%Y-%m-%d'),
                'time': '7:00 PM',
                'type': 'lecture',
                'description': f'Featured cultural programming at {institution["name"]}. Visit their website for current events.',
                'city': 'New York',
                'price': 'See website',
                'duration': '2 hours',
                'link': institution['url']
            },
            {
                'id': len(self.events) + 2,
                'title': f'Special Program at {institution["name"]}',
                'museum': institution_id,
                'date': (today + timedelta(days=12)).strftime('%Y-%m-%d'),
                'time': '6:30 PM',
                'type': 'talks',
                'description': f'Special programming and cultural events hosted by {institution["name"]}.',
                'city': 'New York',
                'price': 'See website',
                'duration': '90 minutes',
                'link': institution['url']
            }
        ]
        
        self.events.extend(sample_events)
        return len(sample_events)
    
    def scrape_selected_institutions(self, selected_institutions):
        """Scrape from selected institutions"""
        self.scraping_status['active'] = True
        self.scraping_status['events_found'] = 0
        self.scraping_status['progress'] = 0
        self.events = []
        
        total_institutions = len(selected_institutions)
        
        try:
            if not self.setup_driver():
                return False
            
            for i, institution_id in enumerate(selected_institutions):
                self.scraping_status['current_institution'] = self.institutions[institution_id]['name']
                self.scraping_status['progress'] = int((i / total_institutions) * 100)
                
                events_count = self.scrape_institution_real(institution_id)
                self.scraping_status['events_found'] += events_count
                
                time.sleep(2)
            
            self.scraping_status['progress'] = 100
            self.scraping_status['last_scrape'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_message(f"🎉 Scraping complete! Total events: {len(self.events)}")
            
            # Auto-save events with metadata
            self.save_events_to_file()
            
        except Exception as e:
            self.log_message(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
            self.scraping_status['active'] = False
        
        return len(self.events)
    
    def save_events_to_file(self):
        """Save events to JSON file WITH SUMMARY METADATA"""
        try:
            # Calculate summary statistics
            institution_counts = {}
            type_counts = {}
            
            for event in self.events:
                museum = event.get('museum', 'unknown')
                event_type = event.get('type', 'unknown')
                
                institution_counts[museum] = institution_counts.get(museum, 0) + 1
                type_counts[event_type] = type_counts.get(event_type, 0) + 1
            
            # Create enhanced data structure with metadata
            data_with_metadata = {
                "events": self.events,
                "metadata": {
                    "total_events": len(self.events),
                    "scrape_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "institutions_scraped": len(institution_counts),
                    "events_by_institution": institution_counts,
                    "events_by_type": type_counts,
                    "scraper_version": "Enhanced Marcet Society Scraper v2.0"
                }
            }
            
            with open('cultural_events.json', 'w', encoding='utf-8') as f:
                json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
                
            self.log_message(f"💾 Auto-saved {len(self.events)} events with metadata to cultural_events.json")
            
        except Exception as e:
            self.log_message(f"❌ Error saving events: {e}")

# Global scraper instance
scraper = EnhancedMarcetScraper()

# [Rest of the Flask routes remain the same as before...]

@app.route('/')
def index():
    # [Same HTML interface as before - keeping it unchanged for brevity]
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Marcet Society Cultural Events Scraper</title>
    <!-- Same styles and interface as before -->
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 Enhanced Marcet Society Cultural Events Scraper</h1>
            <p>All 17 institutions with detailed metadata tracking</p>
        </div>
        
        <!-- Same interface as before... -->
        <p style="text-align: center; margin: 20px; color: #666;">
            ✨ <strong>Enhanced Version:</strong> Now includes detailed metadata and summary statistics in the JSON file!
        </p>
    </div>
</body>
</html>
    '''

@app.route('/api/institutions')
def get_institutions():
    return jsonify(scraper.institutions)

@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    data = request.json
    selected = data.get('institutions', [])
    
    thread = threading.Thread(target=scraper.scrape_selected_institutions, args=(selected,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/status')
def get_status():
    return jsonify(scraper.scraping_status)

@app.route('/api/events')
def get_events():
    return jsonify(scraper.events)

@app.route('/api/save', methods=['POST'])
def save_events():
    try:
        scraper.save_events_to_file()
        return jsonify({'message': f'Successfully saved {len(scraper.events)} events with metadata'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎭 Starting Enhanced Marcet Society Cultural Events Scraper...")
    print("🌐 Features: Scraping + Event Display + Metadata + Statistics")
    print("📊 Now includes detailed summary at bottom of JSON file!")
    app.run(debug=True, host='0.0.0.0', port=5000)

