import json
import re
import os
from datetime import datetime

def main():
    print("🔄 Starting SAFE React Integration...")
    
    # Load events
    try:
        with open('cultural_events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'events' in data:
            events = data['events']
        else:
            events = data
            
        print(f"✅ Loaded {len(events)} events")
        
    except Exception as e:
        print(f"❌ Error loading events: {e}")
        return False
    
    # Read App.js
    app_js_path = 'frontend/src/App.js'
    try:
        with open(app_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ App.js loaded successfully")
        
    except Exception as e:
        print(f"❌ Error reading App.js: {e}")
        return False
    
    # Create backup
    backup_path = app_js_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created backup at {backup_path}")
    
    # Convert events to React format
    print("⚛️  Converting events...")
    react_events = []
    
    for i, event in enumerate(events, 1):
        if not isinstance(event, dict):
            continue
            
        # Very careful escaping
        title = str(event.get('title', '')).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        description = str(event.get('description', '')).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        
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
    
    new_events_array = "[\n" + ",\n".join(react_events) + "\n]"
    
    # Use a very precise pattern to find and replace
    print("🔍 Finding sampleEvents array...")
    
    # Find the exact start and end positions
    start_pattern = r'const sampleEvents\s*=\s*\['
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ Could not find 'const sampleEvents = ['")
        return False
        
    start_pos = start_match.start()
    
    # Find the matching closing bracket
    bracket_count = 0
    i = start_match.end() - 1  # Start from the opening bracket
    end_pos = None
    
    while i < len(content):
        char = content[i]
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                # Found the closing bracket, now look for the semicolon
                j = i + 1
                while j < len(content) and content[j] in ' \n\t':
                    j += 1
                if j < len(content) and content[j] == ';':
                    end_pos = j + 1
                    break
                else:
                    end_pos = i + 1
                    break
        i += 1
    
    if end_pos is None:
        print("❌ Could not find the end of sampleEvents array")
        return False
    
    print(f"✅ Found sampleEvents from position {start_pos} to {end_pos}")
    
    # Replace the content
    new_content = (
        content[:start_pos] + 
        f"const sampleEvents = {new_events_array};" + 
        content[end_pos:]
    )
    
    # Write the updated content
    try:
        with open(app_js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Successfully updated App.js with {len(events)} events")
        
        # Verify the file is valid
        with open(app_js_path, 'r', encoding='utf-8') as f:
            test_read = f.read()
        
        if len(test_read) < len(content):
            print("⚠️  Warning: New file is smaller than original")
        else:
            print(f"✅ File size check passed ({len(test_read)} chars)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing App.js: {e}")
        # Restore backup
        with open(backup_path, 'r', encoding='utf-8') as f:
            with open(app_js_path, 'w', encoding='utf-8') as f2:
                f2.write(f.read())
        print("✅ Restored backup due to error")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
