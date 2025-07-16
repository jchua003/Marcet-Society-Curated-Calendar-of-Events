import json
import re
import os
from datetime import datetime

class ReactIntegrator:
    def __init__(self, scraped_events_file='cultural_events.json', react_app_path='frontend/src'):
        self.scraped_events_file = scraped_events_file
        self.react_app_path = react_app_path
        self.app_js_path = os.path.join(react_app_path, 'App.js')
        
    def load_scraped_events(self):
        """Load scraped events from JSON file"""
        try:
            with open(self.scraped_events_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {self.scraped_events_file} not found!")
            return []
    
    def convert_to_react_format(self, events):
        """Convert scraped events to React format"""
        react_events = []
        
        for i, event in enumerate(events, 1):
            # Clean up strings for JavaScript
            title = event['title'].replace("'", "\\'").replace('"', '\\"')
            description = event['description'].replace("'", "\\'").replace('"', '\\"')
            
            react_event = f"""  {{
    id: {i},
    title: '{title}',
    museum: '{event.get('museum', 'unknown')}',
    date: '{event.get('date', datetime.now().strftime('%Y-%m-%d'))}',
    time: '{event.get('time', '7:00 PM')}',
    type: '{event.get('type', 'talks')}',
    description: '{description}',
    city: '{event.get('city', 'New York')}',
    price: '{event.get('price', 'See website')}',
    duration: '{event.get('duration', '2 hours')}',
    link: '{event.get('link', '')}'
  }}"""
            react_events.append(react_event)
        
        return "[\n" + ",\n".join(react_events) + "\n  ]"
    
    def update_app_js(self, events):
        """Update App.js with new events"""
        if not os.path.exists(self.app_js_path):
            print(f"❌ Error: {self.app_js_path} not found!")
            return False
        
        try:
            # Read current App.js
            with open(self.app_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new events array
            new_events_array = self.convert_to_react_format(events)
            
            # Find and replace the sampleEvents array
            pattern = r'const sampleEvents = \[.*?\];'
            replacement = f'const sampleEvents = {new_events_array};'
            
            # Use re.DOTALL to match across multiple lines
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Check if replacement was successful
            if updated_content == content:
                print("⚠️  Warning: Could not find sampleEvents array in App.js")
                return False
            
            # Update the Learn More button to use the link
            learn_more_pattern = r'<button className="text-stone-500 hover:text-stone-700 text-sm flex items-center">\s*Learn More <ExternalLink className="w-3 h-3 ml-1" />\s*</button>'
            learn_more_replacement = '''<button 
                        onClick={() => window.open(event.link, '_blank')}
                        className="text-stone-500 hover:text-stone-700 text-sm flex items-center"
                      >
                        Learn More <ExternalLink className="w-3 h-3 ml-1" />
                      </button>'''
            
            updated_content = re.sub(learn_more_pattern, learn_more_replacement, updated_content)
            
            # Write updated content back
            with open(self.app_js_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Successfully updated {self.app_js_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating App.js: {e}")
            return False
    
    def create_backup(self):
        """Create backup of current App.js"""
        if os.path.exists(self.app_js_path):
            backup_path = f"{self.app_js_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            try:
                with open(self.app_js_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Backup created: {backup_path}")
                return True
                
            except Exception as e:
                print(f"❌ Error creating backup: {e}")
                return False
        
        return False
    
    def integrate(self):
        """Main integration function"""
        print("🔄 Starting React Integration...")
        print("=" * 50)
        
        # Load scraped events
        events = self.load_scraped_events()
        if not events:
            return False
        
        # Create backup
        print("📁 Creating backup...")
        self.create_backup()
        
        # Update App.js
        print("⚛️  Updating App.js...")
        if not self.update_app_js(events):
            return False
        
        print("=" * 50)
        print("🎉 Integration complete!")
        print(f"✅ Integrated {len(events)} events into your React app")
        print("\n📋 Next steps:")
        print("1. Test your React app locally")
        print("2. Commit and push changes to GitHub")
        print("3. Your live site will auto-update!")
        
        return True
    
    def print_events_summary(self):
        """Print summary of events to be integrated"""
        events = self.load_scraped_events()
        if not events:
            return
        
        print("\n📊 INTEGRATION SUMMARY")
        print("=" * 50)
        
        for event in events:
            print(f"📅 {event['title']}")
            print(f"   🏛️  {event['museum']} | 📍 {event['city']}")
            print(f"   �� {event['date']} at {event['time']}")
            print(f"   🎭 {event['type']} | 💰 {event['price']}")
            print(f"   🔗 {event['link']}")
            print()
        
        print(f"✅ Ready to integrate {len(events)} events!")

if __name__ == "__main__":
    integrator = ReactIntegrator()
    
    # Show what will be integrated
    integrator.print_events_summary()
    
    # Run integration
    integrator.integrate()

