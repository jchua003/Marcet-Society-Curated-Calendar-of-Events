import React, { useState } from 'react';
import { Calendar, MapPin, Clock, Users, BookOpen, Palette, Music, Search, ExternalLink } from 'lucide-react';
import './App.css';

const App = () => {
  // Institution Categories (based on your CSV data)
  const institutionCategories = {
    "Art Museums": {
      icon: "🖼️",
      institutions: [
        { id: "moma", name: "MoMA" },
        { id: "met", name: "The Met" },
        { id: "frick", name: "Frick Collection" }
      ]
    },
    "Libraries & Literary": {
      icon: "📚",
      institutions: [
        { id: "ny_society_library", name: "NY Society Library" },
        { id: "grolier_club", name: "Grolier Club" },
        { id: "poetry_society", name: "Poetry Society" },
        { id: "rizzoli", name: "Rizzoli Bookstore" }
      ]
    },
    "History & Culture": {
      icon: "🏛️",
      institutions: [
        { id: "womens_history", name: "Women's History" },
        { id: "ny_historical", name: "NY Historical Society" },
        { id: "asia_society", name: "Asia Society" },
        { id: "americas_society", name: "Americas Society" }
      ]
    },
    "Cultural Institutes": {
      icon: "🇫🇷",
      institutions: [
        { id: "albertine", name: "Albertine" },
        { id: "lalliance", name: "L'Alliance" }
      ]
    },
    "Arts & Social Clubs": {
      icon: "🎭",
      institutions: [
        { id: "national_arts_club", name: "National Arts Club" },
        { id: "explorers_club", name: "Explorer's Club" }
      ]
    },
    "Community": {
      icon: "🏘️",
      institutions: [
        { id: "morningside", name: "Morningside Institute" }
      ]
    }
  };

  // Clean sample events (no broken strings!)
  const sampleEvents = [
    {
      id: 1,
      title: "Contemporary Art Exhibition",
      museum: "moma",
      date: "2025-07-25",
      time: "7:00 PM",
      type: "exhibitions",
      description: "Explore contemporary masterpieces in this curated exhibition.",
      city: "New York",
      price: "See website",
      duration: "2 hours",
      link: "https://www.moma.org"
    },
    {
      id: 2,
      title: "Ancient Egyptian Art Gallery Talk",
      museum: "met",
      date: "2025-07-26",
      time: "6:00 PM",
      type: "talks",
      description: "Expert-led discussion about ancient Egyptian artifacts.",
      city: "New York",
      price: "Free",
      duration: "90 minutes",
      link: "https://www.metmuseum.org"
    },
    {
      id: 3,
      title: "Poetry Reading Evening",
      museum: "poetry_society",
      date: "2025-07-27",
      time: "7:30 PM",
      type: "readings",
      description: "Contemporary poetry with local and visiting authors.",
      city: "New York",
      price: "$15",
      duration: "2 hours",
      link: "https://poetrysocietyny.org"
    },
    {
      id: 4,
      title: "French Literature Workshop",
      museum: "albertine",
      date: "2025-07-28",
      time: "6:00 PM",
      type: "workshops",
      description: "Interactive workshop exploring French literary traditions.",
      city: "New York",
      price: "$25",
      duration: "2.5 hours",
      link: "https://www.albertine.com"
    },
    {
      id: 5,
      title: "Historical Manuscripts Exhibition",
      museum: "grolier_club",
      date: "2025-07-29",
      time: "5:00 PM",
      type: "exhibitions",
      description: "Rare manuscripts and historical documents on display.",
      city: "New York",
      price: "Free",
      duration: "3 hours",
      link: "https://www.grolierclub.org"
    },
    {
      id: 6,
      title: "Women in History Lecture",
      museum: "womens_history",
      date: "2025-07-30",
      time: "7:00 PM",
      type: "lectures",
      description: "Celebrating contributions of women throughout history.",
      city: "New York",
      price: "Free",
      duration: "90 minutes",
      link: "https://www.nyhistory.org"
    }
  ];

  // State for filters
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [selectedInstitutions, setSelectedInstitutions] = useState({});

  // Event types
  const eventTypes = [
    { id: "all", label: "All Events", icon: Calendar },
    { id: "exhibitions", label: "Exhibitions", icon: Palette },
    { id: "talks", label: "Talks & Lectures", icon: Users },
    { id: "readings", label: "Readings", icon: BookOpen },
    { id: "workshops", label: "Workshops", icon: Music },
    { id: "lectures", label: "Lectures", icon: Users }
  ];

  // Get institution display name
  const getInstitutionName = (museumId) => {
    for (const category of Object.values(institutionCategories)) {
      for (const inst of category.institutions) {
        if (inst.id === museumId) return inst.name;
      }
    }
    return museumId;
  };

  // Get selected institution IDs from all categories
  const getSelectedInstitutionIds = () => {
    const selected = [];
    Object.values(selectedInstitutions).forEach(instId => {
      if (instId && instId !== "all") {
        selected.push(instId);
      }
    });
    return selected;
  };

  // Filter events
  const selectedInstIds = getSelectedInstitutionIds();
  const filteredEvents = sampleEvents.filter(event => {
    const matchesSearch = searchQuery === "" || 
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesType = filterType === "all" || event.type === filterType;
    
    const matchesInstitution = selectedInstIds.length === 0 || 
      selectedInstIds.includes(event.museum);
    
    return matchesSearch && matchesType && matchesInstitution;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-stone-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-stone-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-stone-800 mb-2">
            🎭 Marcet Society Cultural Events
          </h1>
          <p className="text-lg text-stone-600">
            Discover New York's finest cultural programming
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-stone-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search events..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-stone-300 rounded-lg focus:ring-2 focus:ring-rose-200 focus:border-rose-400"
            />
          </div>
        </div>

        {/* Event Type Filter */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-3">
            {eventTypes.map(type => {
              const Icon = type.icon;
              return (
                <button
                  key={type.id}
                  onClick={() => setFilterType(type.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full transition-colors ${
                    filterType === type.id
                      ? "bg-rose-500 text-white"
                      : "bg-white text-stone-700 border border-stone-300 hover:bg-stone-50"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {type.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Categorized Institution Dropdowns */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-stone-700 mb-4">
            Filter by Institution Category:
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(institutionCategories).map(([categoryName, categoryData]) => (
              <div key={categoryName} className="relative">
                <select
                  value={selectedInstitutions[categoryName] || "all"}
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
                  {categoryData.institutions.map(inst => (
                    <option key={inst.id} value={inst.id}>
                      {inst.name}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        </div>

        {/* Events Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredEvents.map(event => (
            <div key={event.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-xl font-semibold text-stone-800 line-clamp-2">
                  {event.title}
                </h3>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2 text-stone-600">
                  <MapPin className="w-4 h-4" />
                  <span>{getInstitutionName(event.museum)}</span>
                </div>
                <div className="flex items-center gap-2 text-stone-600">
                  <Calendar className="w-4 h-4" />
                  <span>{event.date}</span>
                </div>
                <div className="flex items-center gap-2 text-stone-600">
                  <Clock className="w-4 h-4" />
                  <span>{event.time}</span>
                </div>
              </div>

              <p className="text-stone-600 mb-4 line-clamp-3">
                {event.description}
              </p>

              <div className="flex items-center justify-between">
                <span className="px-3 py-1 bg-rose-100 text-rose-700 rounded-full text-sm">
                  {event.price}
                </span>
                <button
                  onClick={() => window.open(event.link, "_blank")}
                  className="flex items-center gap-2 px-4 py-2 bg-rose-500 text-white rounded-md hover:bg-rose-600 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  Learn More
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredEvents.length === 0 && (
          <div className="text-center py-12">
            <p className="text-stone-500 text-lg">
              No events found matching your criteria.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
