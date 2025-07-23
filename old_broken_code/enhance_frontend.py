import re

# Institution categories mapping
categories = {
    'Art Museums': {
        'icon': '🖼️',
        'institutions': ['met', 'moma', 'frick'],
        'description': 'Fine art collections and exhibitions'
    },
    'Libraries & Literary': {
        'icon': '📚', 
        'institutions': ['ny_society_library', 'grolier_club', 'poetry_society', 'rizzoli'],
        'description': 'Books, manuscripts, and literary events'
    },
    'History & Culture': {
        'icon': '🏛️',
        'institutions': ['womens_history', 'ny_historical', 'asia_society', 'americas_society'],
        'description': 'Historical artifacts and cultural heritage'
    },
    'Arts & Social Clubs': {
        'icon': '🎭',
        'institutions': ['national_arts_club', 'explorers_club'],
        'description': 'Private clubs and artistic societies'
    },
    'Cultural Institutes': {
        'icon': '🇫🇷',
        'institutions': ['albertine', 'lalliance'], 
        'description': 'International cultural centers'
    },
    'Academic': {
        'icon': '🎓',
        'institutions': ['ifa_nyu'],
        'description': 'University programs and research'
    },
    'Community': {
        'icon': '🏘️',
        'institutions': ['morningside'],
        'description': 'Local community organizations'
    }
}

# Institution display names
institution_names = {
    'met': 'The Met',
    'moma': 'MoMA',
    'frick': 'Frick Collection', 
    'womens_history': "Women's History",
    'asia_society': 'Asia Society',
    'ny_historical': 'NY Historical Society',
    'morningside': 'Morningside',
    'ny_society_library': 'NY Society Library',
    'albertine': 'Albertine',
    'rizzoli': 'Rizzoli',
    'grolier_club': 'Grolier Club',
    'national_arts_club': 'National Arts Club',
    'explorers_club': "Explorer's Club",
    'americas_society': 'Americas Society',
    'poetry_society': 'Poetry Society',
    'lalliance': "L'Alliance",
    'ifa_nyu': 'IFA NYU'
}

print("🎨 ENHANCED FRONTEND DESIGN:")
print("=" * 50)

print("\n📋 Categories with institutions:")
for category, info in categories.items():
    print(f"\n{info['icon']} {category}")
    print(f"   {info['description']}")
    for inst in info['institutions']:
        display_name = institution_names.get(inst, inst)
        print(f"   • {display_name}")

print(f"\n📊 Total: {sum(len(info['institutions']) for info in categories.values())} institutions across {len(categories)} categories")

# Create the category mapping for JavaScript
js_categories = {}
for category, info in categories.items():
    js_categories[category] = {
        'icon': info['icon'],
        'institutions': info['institutions'],
        'description': info['description']
    }

js_institution_names = institution_names

print(f"\n🔧 Ready to implement in React with:")
print(f"   • {len(categories)} dropdown categories")  
print(f"   • Institution name mapping")
print(f"   • Category descriptions")
print(f"   • Icon system")

