import json
import re
import os
from datetime import datetime

def main():
    print("🔄 Starting React Integration...")
    
    # Step 1: Load events from JSON file
    try:
        with open('cultural_events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both formats
        if isinstance(data, list):
            events = data
        elif isinstance(data, dict) and 'events' in data:
            events = data['events']
        else:
            print("❌ Could not find events in the JSON file")
            return False
            
        print(f"✅ Loaded {len(events)} events from JSON file")
        
    except Exception as e:
        print(f"❌ Error loading events: {e}")
        return False
    
    # Step 2: Check App.js exists
    app_js_path = 'frontend/src/App.js'
    if not os.path.exists(app_js_path):
        print(f"❌ Could not find {app_js_path}")
        return False
    
    # Step 3: Convert events to React format
    print("⚛️  Converting events to React format...")
    react_events = []
    
    for i, event in enumerate(events, 1):
        if not isinstance(event, dict):
            continue
            
        # Escape quotes for JavaScript
        title = (
            str(event.get('title', ''))
            .replace("'", "\\'")
            .replace("\n", "\\\\n")
        )
        description = (
            str(event.get('description', ''))
            .replace("'", "\\'")
            .replace("\n", "\\\\n")
        )
        
        react_event = f"""  {{
    id: {i},
    title: '{title}',
    museum: '{event.get('museum', 'unknown')}',
    date: '{event.get('date', '2025-07-25')}',
    time: '{event.get('time', '7:00 PM')}',
    type: '{event.get('type', 'talks')}',
    description: '{description}',
    city: '{event.get('city', 'New York')}',
    price: '{event.get('price', 'See website')}',
    duration: '{event.get('duration', '2 hours')}',
    link: '{event.get('link', '')}'
  }}"""
        react_events.append(react_event)
    
    new_events_array = "[\n" + ",\n".join(react_events) + "\n  ]"
    
    # Step 4: Update App.js with better pattern matching for multi-line arrays
    print("📝 Updating App.js...")
    try:
        with open(app_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # More flexible pattern that handles multi-line arrays
        # This pattern matches: const sampleEvents = [ ... ]; across multiple lines
        pattern = r'const sampleEvents\s*=\s*\[[\s\S]*?\];'
        
        print(f"   Using pattern: {pattern}")
        
        # Test if pattern matches
        match = re.search(pattern, content)
        if match:
            print(f"   ✅ Pattern matched! Found array with {len(match.group())} characters")
            # Replace the matched section
            updated_content = re.sub(pattern, f'const sampleEvents = {new_events_array};', content)
        else:
            print("   ❌ Pattern didn't match. Let's try a different approach...")
            
            # Alternative: Find the line with const sampleEvents and replace everything until the matching ];
            lines = content.split('\n')
            start_idx = None
            end_idx = None
            bracket_count = 0
            
            for i, line in enumerate(lines):
                if 'const sampleEvents' in line and '=' in line and '[' in line:
                    start_idx = i
                    bracket_count = line.count('[') - line.count(']')
                    print(f"   Found start at line {i+1}: {line.strip()}")
                elif start_idx is not None:
                    bracket_count += line.count('[') - line.count(']')
                    if bracket_count <= 0 and ('];' in line or ']' in line):
                        end_idx = i
                        print(f"   Found end at line {i+1}: {line.strip()}")
                        break
            
            if start_idx is not None and end_idx is not None:
                # Replace the lines
                new_lines = lines[:start_idx] + [f'const sampleEvents = {new_events_array};'] + lines[end_idx+1:]
                updated_content = '\n'.join(new_lines)
                print(f"   ✅ Replaced lines {start_idx+1} to {end_idx+1}")
            else:
                print("   ❌ Could not find sampleEvents array boundaries")
                return False
        
        # Write the updated content
        with open(app_js_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Successfully updated App.js with {len(events)} events")
        return True
        
    except Exception as e:
        print(f"❌ Error updating App.js: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
