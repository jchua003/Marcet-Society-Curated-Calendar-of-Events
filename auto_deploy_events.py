import subprocess
import json
import os
from datetime import datetime

def create_react_integration_script():
    """Create the React integration script if it doesn't exist"""
    react_integration_code = '''import json
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
            title = event.get('title', '').replace("'", "\\\\'").replace('"', '\\\\"')
            description = event.get('description', '').replace("'", "\\\\'").replace('"', '\\\\"')
            
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
        
        return "[\\n" + ",\\n".join(react_events) + "\\n  ]"
    
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
            pattern = r'const sampleEvents = \\[.*?\\];'
            replacement = f'const sampleEvents = {new_events_array};'
            
            # Use re.DOTALL to match across multiple lines
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Check if replacement was successful
            if updated_content == content:
                print("⚠️  Warning: Could not find sampleEvents array in App.js")
                return False
            
            # Write updated content back
            with open(self.app_js_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Successfully updated {self.app_js_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating App.js: {e}")
            return False
    
    def integrate(self):
        """Main integration function"""
        print("🔄 Starting React Integration...")
        
        # Load scraped events
        events = self.load_scraped_events()
        if not events:
            return False
        
        # Update App.js
        print("⚛️  Updating App.js...")
        if not self.update_app_js(events):
            return False
        
        print("🎉 Integration complete!")
        print(f"✅ Integrated {len(events)} events into your React app")
        
        return True

if __name__ == "__main__":
    integrator = ReactIntegrator()
    integrator.integrate()
'''
    
    with open('react_integration.py', 'w', encoding='utf-8') as f:
        f.write(react_integration_code)
    print("✅ Created react_integration.py")

def auto_deploy_scraped_events():
    """Automatically integrate scraped events and deploy to GitHub"""
    
    print("🔄 Starting automatic deployment of scraped events...")
    print("=" * 60)
    
    # Check if we have scraped events
    if not os.path.exists('cultural_events.json'):
        print("❌ No cultural_events.json found.")
        print("💡 Please run the scraper first")
        return False
    
    # Load events to count them
    try:
        with open('cultural_events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
    except Exception as e:
        print(f"❌ Error reading events file: {e}")
        return False
    
    if not events:
        print("❌ No events found in cultural_events.json")
        return False
    
    print(f"📊 Found {len(events)} events to deploy")
    
    # Count events by institution
    institution_counts = {}
    for event in events:
        museum = event.get('museum', 'unknown')
        institution_counts[museum] = institution_counts.get(museum, 0) + 1
    
    print("\n📍 Events by institution:")
    for museum, count in institution_counts.items():
        print(f"   {museum}: {count} events")
    
    print("\n" + "=" * 60)
    
    # Step 1: Check if React integration script exists
    if not os.path.exists('react_integration.py'):
        print("❌ react_integration.py not found. Creating it...")
        create_react_integration_script()
    
    # Step 2: Run React integration
    print("⚛️ Integrating events with React app...")
    try:
        result = subprocess.run(['python', 'react_integration.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ React integration successful!")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ React integration failed:")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ React integration timed out")
        return False
    except Exception as e:
        print(f"❌ Error running React integration: {e}")
        return False
    
    # Step 3: Check git status
    print("\n📦 Checking git status...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("ℹ️ No changes detected. Events may already be up to date.")
            return True
            
        print("📝 Changes detected, proceeding with deployment...")
        
    except subprocess.CalledProcessError:
        print("❌ Not in a git repository or git error")
        return False
    
    # Step 4: Git add, commit, and push
    try:
        print("📦 Adding files to git...")
        subprocess.run(['git', 'add', '.'], check=True, timeout=30)
        
        # Create detailed commit message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"""🎭 Auto-update with {len(events)} scraped cultural events

📅 Scraped: {timestamp}
📊 Total Events: {len(events)}
🏛️ Institutions: {len(institution_counts)}

📍 Event Breakdown:
{chr(10).join([f'   • {museum.replace("_", " ").title()}: {count} events' for museum, count in institution_counts.items()])}

🤖 Deployed via: Complete Marcet Scraper + Auto-Deploy Script
🌐 Live Site: https://jchua003.github.io/Marcet-Society-Curated-Calendar-of-Events"""
        
        print("💾 Committing changes...")
        subprocess.run(['git', 'commit', '-m', commit_message], 
                      check=True, timeout=30)
        
        print("🚀 Pushing to GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub!")
        else:
            print(f"❌ Push failed: {result.stderr}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("\n📍 Next Steps:")
        print("   1. ⏱️  Wait 2-3 minutes for GitHub Pages to deploy")
        print("   2. 🌐 Check your live site:")
        print("      https://jchua003.github.io/Marcet-Society-Curated-Calendar-of-Events")
        print("   3. ✅ Verify the new events are showing")
        print("\n💡 Tip: Check the Actions tab in your GitHub repo to monitor deployment")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Git operation timed out")
        return False

if __name__ == "__main__":
    success = auto_deploy_scraped_events()
    if success:
        print("\n🎭 Your Marcet Society website will be updated shortly!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")

