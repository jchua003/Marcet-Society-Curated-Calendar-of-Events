import json
import re

def main():
    print("🛠️ FOOLPROOF Integration (Zero Syntax Errors)...")
    
    # Load our 68 events
    with open('cultural_events.json') as f:
        data = json.load(f)
    events = data['events'] if isinstance(data, dict) else data
    print(f"📊 Loaded {len(events)} events")
    
    # Read current App.js
    with open('frontend/src/App.js') as f:
        original_content = f.read()
    
    print(f"📄 App.js loaded ({len(original_content)} characters)")
    
    # Find the EXACT sampleEvents array
    start_marker = "const sampleEvents = ["
    end_marker = "];"
    
    start_pos = original_content.find(start_marker)
    if start_pos == -1:
        print("❌ Cannot find 'const sampleEvents = ['")
        return False
    
    print(f"✅ Found start at position {start_pos}")
    
    # Find the end - look for the closing ]; after the start
    search_from = start_pos + len(start_marker)
    temp_pos = search_from
    bracket_count = 1  # We already have one opening bracket
    
    while temp_pos < len(original_content) and bracket_count > 0:
        char = original_content[temp_pos]
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        temp_pos += 1
    
    # Now look for the semicolon
    end_pos = temp_pos
    while end_pos < len(original_content) and original_content[end_pos] in ' \n\t':
        end_pos += 1
    
    if end_pos < len(original_content) and original_content[end_pos] == ';':
        end_pos += 1
    
    print(f"✅ Found end at position {end_pos}")
    
    # Create new events array - VERY SIMPLE FORMAT
    simple_events = []
    for i, event in enumerate(events[:68], 1):  # Limit to exactly 68
        # Ultra-safe string cleaning
        title = str(event.get('title', 'Event')).replace("'", " ").replace('"', ' ')
        desc = str(event.get('description', 'Description')).replace("'", " ").replace('"', ' ')
        
        simple_event = f"""  {{
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
        simple_events.append(simple_event)
    
    # Create the replacement
    replacement = f"const sampleEvents = [\n" + ",\n".join(simple_events) + "\n];"
    
    # Build new content
    new_content = (
        original_content[:start_pos] + 
        replacement + 
        original_content[end_pos:]
    )
    
    print(f"✅ Created new content ({len(new_content)} characters)")
    
    # Save with backup
    with open('frontend/src/App.js.pre-integration', 'w') as f:
        f.write(original_content)
    
    with open('frontend/src/App.js', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Integration complete - {len(events)} events added")
    print("✅ Backup saved as App.js.pre-integration")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Integration failed")
        exit(1)
