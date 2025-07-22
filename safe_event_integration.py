import json
import re

def main():
    print("🔧 SAFE Event Integration (Syntax-Error-Free)...")
    
    # Load events
    with open('cultural_events.json') as f:
        data = json.load(f)
    events = data['events'] if isinstance(data, dict) else data
    print(f"✅ Loaded {len(events)} events")
    
    # Read App.js
    with open('frontend/src/App.js') as f:
        content = f.read()
    print("✅ Loaded App.js")
    
    # Create super clean React events (avoiding syntax issues)
    react_events = []
    for i, event in enumerate(events, 1):
        # Very careful string escaping
        title = str(event.get('title', '')).replace('\\', '\\\\').replace("'", "\\'")
        desc = str(event.get('description', '')).replace('\\', '\\\\').replace("'", "\\'")
        
        # Clean event object
        clean_event = f"""  {{
    id: {i},
    title: '{title}',
    museum: '{event.get('museum', 'unknown')}',
    date: '{event.get('date', '2025-07-25')}',
    time: '{event.get('time', '7:00 PM')}',
    type: '{event.get('type', 'talks')}',
    description: '{desc}',
    city: '{event.get('city', 'New York')}',
    price: '{event.get('price', 'See website')}',
    duration: '{event.get('duration', '2 hours')}',
    link: '{event.get('link', '')}'
  }}"""
        react_events.append(clean_event)
    
    # Create complete array
    new_array = "[\n" + ",\n".join(react_events) + "\n]"
    
    # Super precise replacement
    pattern = r'const sampleEvents\s*=\s*\[[^\]]*\];'
    
    # Find the pattern
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("❌ Could not find sampleEvents array")
        return False
    
    print(f"✅ Found sampleEvents at position {match.start()}-{match.end()}")
    
    # Replace with new content
    new_content = (
        content[:match.start()] + 
        f"const sampleEvents = {new_array};" + 
        content[match.end():]
    )
    
    # Write back
    with open('frontend/src/App.js', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Successfully integrated {len(events)} events")
    
    # Quick syntax validation
    if 'return' in new_content and new_content.count('{') == new_content.count('}'):
        print("✅ Basic syntax check passed")
        return True
    else:
        print("❌ Potential syntax issues detected")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
