#!/usr/bin/env python3
"""
Complete Cultural Events Workflow
Scrapes events from cultural institutions and integrates them into React app
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Import our custom modules
from cultural_events_scraper import CulturalEventScraper
from react_integration import ReactIntegrator

class WorkflowManager:
    def __init__(self, config=None):
        self.config = config or self.default_config()
        self.setup_directories()
        
    def default_config(self):
        return {
            'scraped_events_file': 'cultural_events.json',
            'react_app_path': 'frontend/src',
            'output_dir': 'scraper_output',
            'headless': True,
            'max_events_per_institution': 10,
            'delay_between_sites': 2
        }
    
    def setup_directories(self):
        """Create necessary directories"""
        Path(self.config['output_dir']).mkdir(exist_ok=True)
        
    def run_full_workflow(self):
        """Run complete workflow: scrape → validate → integrate → deploy"""
        print("🎭 MARCET SOCIETY CULTURAL EVENTS WORKFLOW")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 1: Scrape events
        print("STEP 1: Scraping Cultural Events")
        print("-" * 30)
        
        events = self.scrape_events()
        if not events:
            print("❌ No events scraped. Workflow terminated.")
            return False
        
        # Step 2: Validate and clean events
        print("\nSTEP 2: Validating Events")
        print("-" * 30)
        
        valid_events = self.validate_events(events)
        if not valid_events:
            print("❌ No valid events found. Workflow terminated.")
            return False
        
        # Step 3: Integrate with React app
        print("\nSTEP 3: Integrating with React App")
        print("-" * 30)
        
        if not self.integrate_events(valid_events):
            print("❌ Integration failed. Workflow terminated.")
            return False
        
        # Step 4: Generate deployment files
        print("\nSTEP 4: Generating Deployment Files")
        print("-" * 30)
        
        self.generate_deployment_files(valid_events)
        
        # Step 5: Summary
        print("\nSTEP 5: Workflow Summary")
        print("-" * 30)
        
        self.print_workflow_summary(valid_events)
        
        print("\n🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return True
    
    def scrape_events(self):
        """Scrape events from all institutions"""
        try:
            scraper = CulturalEventScraper(
                headless=self.config['headless']
            )
            
            # Customize scraper settings
            scraper.max_events_per_institution = self.config['max_events_per_institution']
            scraper.delay_between_sites = self.config['delay_between_sites']
            
            events = scraper.scrape_all_events()
            
            # Save raw scraped data
            raw_file = os.path.join(self.config['output_dir'], 'raw_scraped_events.json')
            with open(raw_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Scraped {len(events)} events")
            print(f"📁 Raw data saved to: {raw_file}")
            
            return events
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return []
    
    def validate_events(self, events):
        """Validate and clean scraped events"""
        print(f"📊 Validating {len(events)} events...")
        
        valid_events = []
        validation_errors = []
        
        for i, event in enumerate(events, 1):
            try:
                # Required fields check
                required_fields = ['title', 'museum', 'date', 'time', 'type', 'description', 'city']
                missing_fields = [field for field in required_fields if not event.get(field)]
                
                if missing_fields:
                    validation_errors.append(f"Event {i}: Missing fields: {missing_fields}")
                    continue
                
                # Date validation
                try:
                    datetime.strptime(event['date'], '%Y-%m-%d')
                except ValueError:
                    validation_errors.append(f"Event {i}: Invalid date format: {event['date']}")
                    continue
                
                # Clean up text fields
                event['title'] = event['title'].strip()[:100]  # Limit title length
                event['description'] = event['description'].strip()[:300]  # Limit description
                
                # Ensure required fields have defaults
                event['price'] = event.get('price', 'See website')
                event['duration'] = event.get('duration', '2 hours')
                event['link'] = event.get('link', '')
                
                valid_events.append(event)
                
            except Exception as e:
                validation_errors.append(f"Event {i}: Validation error: {e}")
        
        # Save validation report
        validation_report = {
            'total_scraped': len(events),
            'valid_events': len(valid_events),
            'validation_errors': validation_errors,
            'validation_timestamp': datetime.now().isoformat()
        }
        
        report_file = os.path.join(self.config['output_dir'], 'validation_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(validation_report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(valid_events)} valid events")
        print(f"⚠️  {len(validation_errors)} validation errors")
        print(f"📁 Validation report saved to: {report_file}")
        
        return valid_events
    
    def integrate_events(self, events):
        """Integrate events with React app"""
        try:
            # Save clean events file
            clean_file = self.config['scraped_events_file']
            with open(clean_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            
            # Run integration
            integrator = ReactIntegrator(
                scraped_events_file=clean_file,
                react_app_path=self.config['react_app_path']
            )
            
            success = integrator.integrate()
            
            if success:
                print(f"✅ Successfully integrated {len(events)} events")
            else:
                print("❌ Integration failed")
            
            return success
            
        except Exception as e:
            print(f"❌ Error during integration: {e}")
            return False
    
    def generate_deployment_files(self, events):
        """Generate files needed for deployment"""
        output_dir = self.config['output_dir']
        
        try:
            # 1. Generate events summary
            summary = self.generate_events_summary(events)
            summary_file = os.path.join(output_dir, 'events_summary.json')
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            # 2. Generate React component code
            react_code = self.generate_react_component(events)
            react_file = os.path.join(output_dir, 'EventsComponent.jsx')
            with open(react_file, 'w', encoding='utf-8') as f:
                f.write(react_code)
            
            # 3. Generate deployment README
            readme = self.generate_deployment_readme(events)
            readme_file = os.path.join(output_dir, 'DEPLOYMENT_README.md')
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme)
            
            print(f"✅ Generated deployment files in: {output_dir}")
            
        except Exception as e:
            print(f"❌ Error generating deployment files: {e}")
    
    def generate_events_summary(self, events):
        """Generate summary statistics"""
        summary = {
            'total_events': len(events),
            'last_updated': datetime.now().isoformat(),
            'events_by_type': {},
            'events_by_museum': {},
            'events_by_city': {},
            'upcoming_events': 0
        }
        
        today = datetime.now().date()
        
        for event in events:
            # Count by type
            event_type = event.get('type', 'unknown')
            summary['events_by_type'][event_type] = summary['events_by_type'].get(event_type, 0) + 1
            
            # Count by museum
            museum = event.get('museum', 'unknown')
            summary['events_by_museum'][museum] = summary['events_by_museum'].get(museum, 0) + 1
            
            # Count by city
            city = event.get('city', 'unknown')
            summary['events_by_city'][city] = summary['events_by_city'].get(city, 0) + 1
            
            # Count upcoming events
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
                if event_date >= today:
                    summary['upcoming_events'] += 1
            except:
                pass
        
        return summary
    
    def generate_react_component(self, events):
        """Generate a React component with the events"""
        component_code = f'''// Auto-generated Events Component
// Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Total events: {len(events)}

import React from 'react';
import {{ Calendar, MapPin, Clock, ExternalLink }} from 'lucide-react';

const culturalEvents = {json.dumps(events, indent=2)};

const EventsComponent = () => {{
  return (
    <div className="events-container">
      <h2>Cultural Events</h2>
      <div className="events-grid">
        {{culturalEvents.map((event, index) => (
          <div key={{index}} className="event-card">
            <h3>{{event.title}}</h3>
            <div className="event-meta">
              <span><MapPin size={{16}} /> {{event.museum}}</span>
              <span><Clock size={{16}} /> {{event.date}} at {{event.time}}</span>
              <span><Calendar size={{16}} /> {{event.type}}</span>
            </div>
            <p>{{event.description}}</p>
            <div className="event-actions">
              <span className="price">{{event.price}}</span>
              {{event.link && (
                <a href={{event.link}} target="_blank" rel="noopener noreferrer">
                  Learn More <ExternalLink size={{16}} />
                </a>
              )}}
            </div>
          </div>
        ))}}
      </div>
    </div>
  );
}};

export default EventsComponent;
'''
        return component_code
    
    def generate_deployment_readme(self, events):
        """Generate deployment README"""
        readme = f'''# Cultural Events Deployment Guide

## 📊 Summary
- **Total Events**: {len(events)}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Generated Files**: {len(os.listdir(self.config['output_dir']))} files

## 🚀 Deployment Steps

### 1. Verify Integration
```bash
cd frontend
npm start
```

### 2. Test Functionality
- ✅ Events display correctly
- ✅ Filtering works
- ✅ Google Calendar integration works
- ✅ "Learn More" links work

### 3. Deploy to GitHub Pages
```bash
git add .
git commit -m "Update cultural events - {datetime.now().strftime('%Y-%m-%d')}"
git push origin main
```

### 4. Monitor Deployment
- Check GitHub Actions for build status
- Verify live site updates
- Test all functionality on live site

## 📁 Generated Files
- `cultural_events.json` - Clean events data
- `events_summary.json` - Statistics and summary
- `EventsComponent.jsx` - React component
- `validation_report.json` - Validation results
- `DEPLOYMENT_README.md` - This file

## 🔄 Automated Updates
To keep events fresh, run this workflow regularly:

```bash
python complete_workflow.py
```

## 🎭 Event Types Included
- Exhibitions
- Special Events
- Lectures
- Tours
- Performances
- Panel Discussions
- Talks

## 🏛️ Institutions Covered
- Metropolitan Museum of Art
- Museum of Modern Art
- Frick Collection
- Asia Society
- NY Historical Society
- And more...

## 🎯 Next Steps
1. Set up automated scheduling
2. Add more institutions
3. Expand to other cities
4. Implement caching
5. Add event notifications

---
*Generated by Marcet Society Cultural Events Workflow*
'''
        return readme
    
    def print_workflow_summary(self, events):
        """Print final workflow summary"""
        summary = self.generate_events_summary(events)
        
        print("📈 WORKFLOW STATISTICS")
        print(f"Total Events: {summary['total_events']}")
        print(f"Upcoming Events: {summary['upcoming_events']}")
        print()
        
        print("🎭 Events by Type:")
        for event_type, count in summary['events_by_type'].items():
            print(f"  {event_type}: {count}")
        print()
        
        print("🏛️ Events by Museum:")
        for museum, count in summary['events_by_museum'].items():
            print(f"  {museum}: {count}")
        print()
        
        print("📁 Files Generated:")
        for filename in os.listdir(self.config['output_dir']):
            filepath = os.path.join(self.config['output_dir'], filename)
            size = os.path.getsize(filepath)
            print(f"  {filename} ({size:,} bytes)")

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cultural Events Workflow')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--max-events', type=int, default=10, help='Max events per institution')
    parser.add_argument('--output-dir', default='scraper_output', help='Output directory')
    parser.add_argument('--react-path', default='frontend/src', help='React app path')
    parser.add_argument('--preview', action='store_true', help='Preview only, no integration')
    
    args = parser.parse_args()
    
    config = {
        'scraped_events_file': 'cultural_events.json',
        'react_app_path': args.react_path,
        'output_dir': args.output_dir,
        'headless': args.headless,
        'max_events_per_institution': args.max_events,
        'delay_between_sites': 2
    }
    
    workflow = WorkflowManager(config)
    
    if args.preview:
        print("🔍 PREVIEW MODE - No changes will be made")
        print("=" * 50)
        # Add preview functionality here
    else:
        success = workflow.run_full_workflow()
        exit(0 if success else 1)

if __name__ == "__main__":
    main()