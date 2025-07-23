import re

def main():
    print("🎨 Implementing Categorized Institution UI...")
    
    # Institution categories based on your CSV data
    categories = {
        'Art Museums': {
            'icon': '🖼️',
            'institutions': [
                ('moma', 'MoMA'),
                ('met', 'The Met'),
                ('frick', 'Frick Collection')
            ]
        },
        'Libraries & Literary': {
            'icon': '📚',
            'institutions': [
                ('ny_society_library', 'NY Society Library'),
                ('grolier_club', 'Grolier Club'),
                ('poetry_society', 'Poetry Society'),
                ('rizzoli', 'Rizzoli Bookstore')
            ]
        },
        'History & Culture': {
            'icon': '🏛️',
            'institutions': [
                ('womens_history', "Women's History"),
                ('ny_historical', 'NY Historical Society'),
                ('asia_society', 'Asia Society'),
                ('americas_society', 'Americas Society')
            ]
        },
        'Cultural Institutes': {
            'icon': '��🇷',
            'institutions': [
                ('albertine', 'Albertine'),
                ('lalliance', "L'Alliance")
            ]
        },
        'Arts & Social Clubs': {
            'icon': '🎭',
            'institutions': [
                ('national_arts_club', 'National Arts Club'),
                ('explorers_club', "Explorer's Club")
            ]
        },
        'Community': {
            'icon': '🏘️',
            'institutions': [
                ('morningside', 'Morningside Institute')
            ]
        }
    }
    
    try:
        # Read current App.js
        with open('frontend/src/App.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Loaded current App.js")
        
        # Create backup
        with open('frontend/src/App.js.ui-backup', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Created backup")
        
        # Add categories data after imports
        categories_code = f'''
// Institution Categories
const institutionCategories = {str(categories).replace("'", '"')};

// State for selected institutions per category
const [selectedInstitutions, setSelectedInstitutions] = useState({{}});
'''
        
        # Find where to insert (after useState imports)
        useState_pattern = r"import.*useState.*from 'react';"
        match = re.search(useState_pattern, content)
        
        if match:
            insertion_point = match.end()
            # Insert categories after the import
            new_content = content[:insertion_point] + '\n' + categories_code + content[insertion_point:]
            print("✅ Added categories data")
        else:
            print("❌ Could not find useState import")
            return False
        
        # Create the categorized dropdowns JSX
        categorized_dropdowns_jsx = '''
      {/* Categorized Institution Dropdowns */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-stone-700 mb-3">Filter by Institution Category:</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {Object.entries(institutionCategories).map(([categoryName, categoryData]) => (
            <div key={categoryName} className="relative">
              <select
                value={selectedInstitutions[categoryName] || 'all'}
                onChange={(e) => {
                  setSelectedInstitutions(prev => ({
                    ...prev,
                    [categoryName]: e.target.value
                  }));
                }}
                className="w-full px-3 py-2 text-sm border border-stone-300 rounded-md focus:ring-2 focus:ring-rose-200 focus:border-rose-400 bg-white"
              >
                <option value="all">
                  {categoryData.icon} All {categoryName}
                </option>
                {categoryData.institutions.map(([instId, instName]) => (
                  <option key={instId} value={instId}>
                    {instName}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      </div>'''
        
        # Find existing filters section and add our dropdowns
        filter_section_pattern = r'(<div[^>]*className[^>]*gap.*?>)'
        match = re.search(filter_section_pattern, new_content)
        
        if match:
            insertion_point = match.end()
            new_content = new_content[:insertion_point] + categorized_dropdowns_jsx + new_content[insertion_point:]
            print("✅ Added categorized dropdowns")
        else:
            print("⚠️ Could not find filter section, adding after header")
            # Add after header section instead
            header_pattern = r'</header>'
            header_match = re.search(header_pattern, new_content)
            if header_match:
                insertion_point = header_match.end()
                new_content = new_content[:insertion_point] + '\n      <div className="max-w-7xl mx-auto px-6 py-4">' + categorized_dropdowns_jsx + '\n      </div>' + new_content[insertion_point:]
                print("✅ Added after header")
        
        # Update filtering logic
        filter_update = '''
    // Get selected institution IDs from all categories
    const getSelectedInstitutionIds = () => {
      const selected = [];
      Object.values(selectedInstitutions).forEach(instId => {
        if (instId && instId !== 'all') {
          selected.push(instId);
        }
      });
      return selected;
    };

    const selectedInstIds = getSelectedInstitutionIds();
    const matchesInstitution = selectedInstIds.length === 0 || 
      selectedInstIds.includes(event.museum);'''
        
        # Find existing filtering logic and replace/enhance it
        existing_filter_pattern = r'const matchesInstitution = .*?;'
        if re.search(existing_filter_pattern, new_content):
            # Replace existing logic
            new_content = re.sub(existing_filter_pattern, 
                               'const matchesInstitution = selectedInstIds.length === 0 || selectedInstIds.includes(event.museum);', 
                               new_content)
            
            # Add helper function before filtering
            filter_start = new_content.find('const matchesInstitution')
            new_content = new_content[:filter_start] + filter_update.split('const matchesInstitution')[0] + new_content[filter_start:]
            print("✅ Updated filtering logic")
        else:
            print("⚠️ Could not find existing filter logic")
        
        # Write the enhanced App.js
        with open('frontend/src/App.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Successfully implemented categorized institution UI!")
        print("\n🎨 Your UI now has:")
        print("   • 6 categorized institution dropdown menus")
        print("   • Art Museums, Libraries, History & Culture, etc.")
        print("   • Multi-select capability (one from each category)")
        print("   • Same beautiful existing design")
        
        return True
        
    except Exception as e:
        print(f"❌ Error implementing UI: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ UI implementation failed")
        exit(1)

