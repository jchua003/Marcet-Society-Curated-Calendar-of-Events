import re

def main():
    print("🔧 Adding categorized institution dropdowns to your existing UI...")
    
    # Institution categories (same as before)
    categories = {
        'Art Museums': {
            'icon': '🖼️',
            'institutions': [
                ('met', 'The Met'),
                ('moma', 'MoMA'),
                ('frick', 'Frick Collection')
            ]
        },
        'Libraries & Literary': {
            'icon': '📚',
            'institutions': [
                ('ny_society_library', 'NY Society Library'),
                ('grolier_club', 'Grolier Club'), 
                ('poetry_society', 'Poetry Society'),
                ('rizzoli', 'Rizzoli')
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
        'Arts & Social Clubs': {
            'icon': '🎭',
            'institutions': [
                ('national_arts_club', 'National Arts Club'),
                ('explorers_club', "Explorer's Club")
            ]
        },
        'Cultural Institutes': {
            'icon': '🇫🇷',
            'institutions': [
                ('albertine', 'Albertine'),
                ('lalliance', "L'Alliance")
            ]
        },
        'Academic': {
            'icon': '🎓',
            'institutions': [('ifa_nyu', 'IFA NYU')]
        },
        'Community': {
            'icon': '🏘️',
            'institutions': [('morningside', 'Morningside')]
        }
    }
    
    # Read current App.js
    try:
        with open('frontend/src/App.js', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Loaded existing App.js")
    except Exception as e:
        print(f"❌ Error reading App.js: {e}")
        return False
    
    # Create backup
    with open('frontend/src/App.js.backup2', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created backup at App.js.backup2")
    
    # Add categories data to the top of the component
    categories_js = f"""
  // Institution categories for dropdown filtering
  const institutionCategories = {str(categories).replace("'", '"')};
  
  // Track selected institutions per category
  const [selectedInstitutions, setSelectedInstitutions] = useState({{}});
"""
    
    # Find where to insert the categories (after existing useState)
    useState_pattern = r'(const \[.*?, set.*?\] = useState\(.*?\);)'
    matches = re.findall(useState_pattern, content)
    
    if matches:
        last_useState = matches[-1]
        insertion_point = content.find(last_useState) + len(last_useState)
        new_content = content[:insertion_point] + categories_js + content[insertion_point:]
        print("✅ Added categories data")
    else:
        print("❌ Could not find useState declarations")
        return False
    
    # Find the current institution filter and replace it
    # Look for the current institution dropdown
    institution_dropdown_pattern = r'<select[^>]*institution[^>]*>[\s\S]*?</select>'
    
    # Create new categorized dropdowns JSX
    categorized_dropdowns = '''
      {/* Categorized Institution Dropdowns */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
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
      </div>'''
    
    # Replace or add the categorized dropdowns
    if re.search(institution_dropdown_pattern, new_content):
        new_content = re.sub(institution_dropdown_pattern, categorized_dropdowns, new_content)
        print("✅ Replaced existing institution dropdown")
    else:
        # Find a good place to insert (after existing filters)
        filter_section = r'(<div[^>]*className[^>]*gap.*?>[\s\S]*?</div>)'
        match = re.search(filter_section, new_content)
        if match:
            insertion_point = match.end()
            new_content = new_content[:insertion_point] + '\n      ' + categorized_dropdowns + new_content[insertion_point:]
            print("✅ Added categorized dropdowns after existing filters")
    
    # Update the filtering logic
    filter_logic = '''
    // Enhanced filtering with categorized institutions
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
    const matchesInstitution = selectedInstIds.length === 0 || selectedInstIds.includes(event.museum);'''
    
    # Find existing filter logic and enhance it
    existing_filter_pattern = r'const matchesInstitution = .*?;'
    if re.search(existing_filter_pattern, new_content):
        new_content = re.sub(existing_filter_pattern, 'const matchesInstitution = selectedInstIds.length === 0 || selectedInstIds.includes(event.museum);', new_content)
        
        # Add the helper function before the existing filter
        helper_insertion = new_content.find('const matchesInstitution')
        new_content = new_content[:helper_insertion] + filter_logic.split('const matchesInstitution')[0] + new_content[helper_insertion:]
        print("✅ Updated filtering logic")
    
    # Write the enhanced content
    try:
        with open('frontend/src/App.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Successfully enhanced App.js with categorized dropdowns")
        return True
    except Exception as e:
        print(f"❌ Error writing enhanced App.js: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Enhancement complete!")
        print("📋 Your UI now has:")
        print("   • 7 categorized institution dropdowns")
        print("   • Same beautiful existing layout") 
        print("   • Enhanced filtering capabilities")
    else:
        print("\n❌ Enhancement failed")
        
