import json
from datetime import datetime

print("🔄 Adding metadata to your existing events...")

# Load current events
with open('cultural_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Handle both old format (array) and new format (object)
if isinstance(events, dict) and 'events' in events:
    events_list = events['events']
    print("ℹ️ File already has metadata format")
else:
    events_list = events
    print(f"📊 Converting {len(events)} events to new format with metadata")

# Calculate summary statistics
institution_counts = {}
type_counts = {}

for event in events_list:
    museum = event.get('museum', 'unknown')
    event_type = event.get('type', 'unknown')
    
    institution_counts[museum] = institution_counts.get(museum, 0) + 1
    type_counts[event_type] = type_counts.get(event_type, 0) + 1

# Create enhanced data structure with metadata
data_with_metadata = {
    "events": events_list,
    "metadata": {
        "total_events": len(events_list),
        "scrape_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "institutions_scraped": len(institution_counts),
        "events_by_institution": institution_counts,
        "events_by_type": type_counts,
        "scraper_version": "Enhanced Marcet Society Scraper v2.0",
        "note": "Metadata added to existing scraped events"
    }
}

# Save enhanced file
with open('cultural_events.json', 'w', encoding='utf-8') as f:
    json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)

print("✅ Successfully added metadata!")
print(f"📊 Total events: {len(events_list)}")
print(f"🏛️ Institutions: {len(institution_counts)}")
print(f"🎭 Event types: {len(type_counts)}")
print("\n📋 Events by Institution:")
for museum, count in sorted(institution_counts.items()):
    print(f"   {museum}: {count} events")

print("\n📋 Events by Type:")
for event_type, count in sorted(type_counts.items()):
    print(f"   {event_type}: {count} events")

