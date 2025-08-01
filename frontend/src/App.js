import React, { useState } from 'react';
import { gapi } from 'gapi-script';
import {
  Calendar,
  MapPin,
  Clock,
  Users,
  BookOpen,
  Palette,
  Music,
  Search,
  Plus
} from 'lucide-react';
import './App.css';

// TODO: Replace with your own Google API credentials
const CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '922415648629-7f6jn9v2vej7ka1knnnukvpi0i283tuk.apps.googleusercontent.com';
const API_KEY = process.env.REACT_APP_GOOGLE_API_KEY || 'YOUR_API_KEY';
const DISCOVERY_DOCS = [
  'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
];
const SCOPES = 'https://www.googleapis.com/auth/calendar.events';

const loadGapi = () =>
  new Promise((resolve, reject) => {
    if (window.gapi) {
      return resolve(window.gapi);
    }
    const script = document.createElement('script');
    script.src = 'https://apis.google.com/js/api.js';
    script.onload = () => resolve(window.gapi);
    script.onerror = () => reject(new Error('Failed to load gapi'));
    document.body.appendChild(script);
  });

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
  Community: {
    icon: "🏘️",
    institutions: [
      { id: "morningside", name: "Morningside Institute" }
    ]
  }
};

const eventTypes = [
  { id: 'all', label: 'All Events', icon: Calendar },
  { id: 'museums', label: 'Museums', icon: Palette },
  { id: 'lectures', label: 'Lectures', icon: BookOpen },
  { id: 'music', label: 'Music & Performance', icon: Music },
  { id: 'discussions', label: 'Discussions', icon: Users }
];

const sampleEvents = [
  {
    id: 1,
    title: 'Women in Science: A Historical Perspective',
    venue: 'Museum of Natural History',
    date: '2025-07-20',
    time: '2:00 PM',
    type: 'museums',
    description: 'Explore the contributions of women scientists throughout history',
    city: 'New York',
    museum: 'ny_historical'
  },
  {
    id: 2,
    title: 'Literary Salon: Contemporary Female Authors',
    venue: 'Public Library',
    date: '2025-07-22',
    time: '6:30 PM',
    type: 'discussions',
    description: 'Discussion on modern women writers and their impact',
    city: 'New York',
    museum: 'ny_society_library'
  },
  {
    id: 3,
    title: 'The Art of Enlightenment',
    venue: 'Metropolitan Museum',
    date: '2025-07-25',
    time: '11:00 AM',
    type: 'museums',
    description: 'Guided tour of Enlightenment era artworks',
    city: 'New York',
    museum: 'met'
  }
];

const cities = [
  'New York',
  'Los Angeles',
  'San Francisco',
  'London',
  'Washington DC',
  'Boston',
  'Chicago'
];

const App = () => {
  const [selectedCity, setSelectedCity] = useState('New York');
  const [selectedEvents, setSelectedEvents] = useState(new Set());
  const [filterType, setFilterType] = useState('all');
  const [selectedInstitutions, setSelectedInstitutions] = useState({});
  const [isConnected, setIsConnected] = useState(false);

  const getSelectedInstitutionIds = () => {
    const ids = [];
    Object.values(selectedInstitutions).forEach((inst) => {
      if (inst && inst !== 'all') ids.push(inst);
    });
    return ids;
  };

  const filteredEvents = sampleEvents.filter((event) => {
    const matchesCity = event.city === selectedCity;
    const matchesType = filterType === 'all' || event.type === filterType;
    const selectedIds = getSelectedInstitutionIds();
    const matchesInstitution =
      selectedIds.length === 0 || selectedIds.includes(event.museum);
    return matchesCity && matchesType && matchesInstitution;
  });

  const toggleEventSelection = (eventId) => {
    const newSelected = new Set(selectedEvents);
    if (newSelected.has(eventId)) {
      newSelected.delete(eventId);
    } else {
      newSelected.add(eventId);
    }
    setSelectedEvents(newSelected);
  };

  const connectCalendar = () => {
    loadGapi().then((gapi) => {
      const initClient = () => {
        gapi.client
          .init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES
          })
          .then(() => gapi.auth2.getAuthInstance().signIn())
          .then(() => setIsConnected(true));
      };
      gapi.load('client:auth2', initClient);
    });
  };

  const addEventsToCalendar = () => {
    if (!isConnected) return;
    const selected = sampleEvents.filter((e) => selectedEvents.has(e.id));
    selected.forEach((event) => {
      const start = new Date(`${event.date} ${event.time}`);
      const end = new Date(start.getTime() + 60 * 60 * 1000);
      gapi.client.calendar.events.insert({
        calendarId: 'primary',
        resource: {
          summary: event.title,
          location: event.venue,
          description: event.description,
          start: { dateTime: start.toISOString() },
          end: { dateTime: end.toISOString() }
        }
      });
    });
    setSelectedEvents(new Set());
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-100">
      {/* Header */}

      <header className="bg-white shadow-sm border-b border-indigo-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl  text-black mb-3">
              Cultural Events Calendar
            </h1>
            <p className="text-lg text-black max-w-2xl mx-auto leading-relaxed">
              Discover enriching cultural experiences across the world's great cities
            </p>
            <div className="mt-6 p-4 bg-indigo-50 rounded-lg border-l-4 border-indigo-400 max-w-3xl mx-auto">
              <p className="text-black italic ">
                "The cultivation of the mind is as necessary as the cultivation of the body."
              </p>
              <p className="text-black text-sm mt-2">— Jane Marcet</p>
            </div>
          </div>


          {/* City Selector */}
          <div className="flex flex-wrap justify-center gap-2 mb-6">
            {cities.map((city) => (
              <button
                key={city}
                onClick={() => setSelectedCity(city)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                  selectedCity === city
                    ? 'bg-indigo-800 text-white shadow-md'
                    : 'bg-white text-black hover:bg-indigo-100 border border-indigo-300'
                }`}
              >
                {city}
              </button>
            ))}
          </div>

          {/* Calendar Connection */}
          <div className="text-center">
            {!isConnected ? (
              <button
                onClick={connectCalendar}
                className="bg-indigo-800 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg"
              >
                <Calendar className="inline-block w-5 h-5 mr-2" />
                Connect Your Calendar
              </button>
            ) : (
              <div className="inline-flex items-center px-4 py-2 bg-green-50 text-black rounded-lg border border-green-200">
                <Calendar className="w-5 h-5 mr-2" />
                Calendar Connected
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Filters */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6 border border-indigo-200">
              <h3 className="text-lg  text-black mb-4">Filter Events</h3>

              {/* Search */}
              <div className="mb-6">
                <div className="relative">
                  <Search className="absolute left-3 top-3 w-4 h-4 text-black" />
                  <input
                    type="text"
                    placeholder="Search events..."
                    className="w-full pl-10 pr-4 py-2 border border-indigo-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Filter by Institution */}
              <div className="space-y-4 mb-6">
                <h4 className="text-lg  font-medium text-black">Filter by Institution:</h4>
                {Object.entries(institutionCategories).map(([categoryName, categoryData]) => (
                  <select
                    key={categoryName}
                    value={selectedInstitutions[categoryName] || 'all'}
                    onChange={(e) =>
                      setSelectedInstitutions((prev) => ({
                        ...prev,
                        [categoryName]: e.target.value
                      }))
                    }
                    className="w-full px-4 py-2 text-sm border border-indigo-300 rounded-full shadow-sm bg-baby-blue text-black"
                  >
                    <option value="all">
                      {categoryData.icon} All {categoryName}
                    </option>
                    {categoryData.institutions.map((inst) => (
                      <option key={inst.id} value={inst.id}>
                        {inst.name}
                      </option>
                    ))}
                  </select>
                ))}
              </div>

              {/* Event Types */}
              <div className="space-y-2">
                {eventTypes.map((type) => {
                  const Icon = type.icon;
                  return (
                    <button
                      key={type.id}
                      onClick={() => setFilterType(type.id)}
                      className={`w-full flex items-center px-3 py-2 rounded-lg text-sm transition-colors duration-200 ${
                        filterType === type.id
                          ? 'bg-indigo-100 text-black border border-indigo-300'
                          : 'text-black hover:bg-indigo-50'
                      }`}
                    >
                      <Icon className="w-4 h-4 mr-3" />
                      {type.label}
                    </button>
                  );
                })}
              </div>

              {/* Selected Events Summary */}
              {selectedEvents.size > 0 && (
                <div className="mt-6 p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                  <h4 className=" font-medium text-black mb-2">
                    Selected Events ({selectedEvents.size})
                  </h4>
                  <button
                    onClick={addEventsToCalendar}
                    disabled={!isConnected}
                    className="w-full bg-indigo-800 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors duration-200 disabled:opacity-50"
                  >
                    Add to Calendar
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Events List */}
          <div className="lg:col-span-3">
            <div className="mb-6">
              <h2 className="text-2xl  text-black mb-2">Events in {selectedCity}</h2>
              <p className="text-black">
                {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
              </p>
            </div>

            <div className="grid gap-6">
              {filteredEvents.map((event) => (
                <div
                  key={event.id}
                  className={`bg-white rounded-lg shadow-sm border transition-all duration-200 hover:shadow-md cursor-pointer ${
                    selectedEvents.has(event.id)
                      ? 'border-indigo-400 bg-indigo-50'
                      : 'border-indigo-200 hover:border-indigo-300'
                  }`}
                  onClick={() => toggleEventSelection(event.id)}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl  text-black mb-2">
                          {event.title}
                        </h3>
                        <div className="flex items-center text-black text-sm space-x-4">
                          <span className="flex items-center">
                            <MapPin className="w-4 h-4 mr-1" />
                            {event.venue}
                          </span>
                          <span className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {event.date} at {event.time}
                          </span>
                        </div>
                      </div>
                      <div
                        className={`ml-4 p-2 rounded-full transition-colors duration-200 ${
                          selectedEvents.has(event.id)
                            ? 'bg-indigo-800 text-white'
                            : 'bg-indigo-100 text-black hover:bg-indigo-200'
                        }`}
                      >
                        <Plus className="w-4 h-4" />
                      </div>
                    </div>

                    <p className="text-black leading-relaxed">{event.description}</p>

                    <div className="mt-4 pt-4 border-t border-indigo-100">
                      <span className="inline-block px-3 py-1 bg-indigo-100 text-black text-xs rounded-full">
                        {eventTypes.find((t) => t.id === event.type)?.label}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredEvents.length === 0 && (
              <div className="text-center py-12">
                <Calendar className="w-16 h-16 text-black mx-auto mb-4" />
                <h3 className="text-lg  text-black mb-2">No events found</h3>
                <p className="text-black">
                  Try adjusting your filters or check back later for new events.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-indigo-200 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-black">
            <p className="text-sm">Inspiring intellectual curiosity through cultural engagement</p>
            <p className="text-xs mt-2 text-black">Built with dedication to lifelong learning</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
