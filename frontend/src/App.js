import React, { useState, useEffect } from 'react';
import { Calendar, Users, BookOpen, Palette, Music, Search } from 'lucide-react';
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

  // Cities for filtering
  const cities = [
    "New York",
    "Los Angeles",
    "San Francisco",
    "London",
    "Washington DC",
    "Boston",
    "Chicago"
  ];

  const [selectedCity, setSelectedCity] = useState("New York");
  const [events, setEvents] = useState(sampleEvents);
  const [isGoogleLoaded, setIsGoogleLoaded] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [accessToken, setAccessToken] = useState(null);

  const GOOGLE_CLIENT_ID = "922415648629-7f6jn9v2vej7ka1knnnukvpi0i283tuk.apps.googleusercontent.com";

  // Load events and initialize Google APIs
  useEffect(() => {
    fetch("cultural_events.json")
      .then((res) => res.json())
      .then((data) => {
        if (data.events) {
          setEvents(data.events);
        }
      })
      .catch(() => {});

    const initializeGoogleAPIs = async () => {
      try {
        await Promise.all([
          new Promise((resolve) => {
            const checkGSI = () => {
              if (window.google && window.google.accounts) {
                resolve();
              } else {
                setTimeout(checkGSI, 100);
              }
            };
            checkGSI();
          }),
          new Promise((resolve) => {
            const checkGAPI = () => {
              if (window.gapi) {
                resolve();
              } else {
                setTimeout(checkGAPI, 100);
              }
            };
            checkGAPI();
          }),
        ]);

        await new Promise((resolve) => {
          window.gapi.load("client", resolve);
        });

        await window.gapi.client.init({
          discoveryDocs: [
            "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
          ],
        });

        setIsGoogleLoaded(true);
      } catch (error) {
        console.error("Error initializing Google APIs:", error);
      }
    };

    initializeGoogleAPIs();
  }, []);

  const connectCalendar = () => {
    if (!isGoogleLoaded) {
      alert("Google API is still loading. Please wait a moment and try again.");
      return;
    }

    if (GOOGLE_CLIENT_ID === "YOUR_GOOGLE_CLIENT_ID_HERE") {
      alert("Please configure your Google Client ID first.");
      return;
    }

    try {
      window.google.accounts.oauth2
        .initTokenClient({
          client_id: GOOGLE_CLIENT_ID,
          scope: "https://www.googleapis.com/auth/calendar.events",
          callback: (response) => {
            if (response.access_token) {
              setAccessToken(response.access_token);
              window.gapi.client.setToken({ access_token: response.access_token });
              setIsConnected(true);
              alert("Successfully connected to Google Calendar!");
            }
          },
        })
        .requestAccessToken();
    } catch (error) {
      console.error("Error connecting to Google Calendar:", error);
      alert("Failed to connect to Google Calendar. Please try again.");
    }
  };

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
  const filteredEvents = events.filter(event => {
    const matchesCity = event.city === selectedCity;
    const matchesSearch =
      searchQuery === "" ||
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesType = filterType === "all" || event.type === filterType;
    
    const matchesInstitution = selectedInstIds.length === 0 || 
      selectedInstIds.includes(event.museum);
    
    return matchesCity && matchesSearch && matchesType && matchesInstitution;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-stone-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-stone-200">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center">
          <h1 className="text-4xl font-serif text-stone-800 mb-4">
            Marcet Society Curated Calendar
          </h1>
          <p className="text-stone-700 italic">
            "When you plead in favor of ignorance, there is a strong presumption that you are in the wrong."
          </p>
          <p className="text-sm text-stone-500">— Jane Marcet</p>
        </div>

        <div className="max-w-7xl mx-auto px-6 pb-6">
          <h3 className="text-lg font-serif text-stone-700 mb-3 text-center">Select City</h3>
          <div className="flex flex-wrap justify-center gap-2">
            {cities.map((city) => (
              <button
                key={city}
                onClick={() => setSelectedCity(city)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all border-2 ${
                  selectedCity === city
                    ? "bg-rose-400 text-white shadow-md border-rose-400"
                    : "bg-white text-stone-600 hover:bg-stone-50 border-rose-200 hover:border-rose-300"
                }`}
              >
                {city}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          <aside className="lg:col-span-1 space-y-6">
            {/* Search Bar */}
            <div>
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
            <div>
              <div className="flex flex-wrap gap-3">
                {eventTypes.map((type) => {
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
            <div>
              <h3 className="text-lg font-semibold text-stone-700 mb-2">Filter by Institution:</h3>
              <div className="space-y-3">
                {Object.entries(institutionCategories).map(([categoryName, categoryData]) => (
                  <select
                    key={categoryName}
                    value={selectedInstitutions[categoryName] || "all"}
                    onChange={(e) => {
                      setSelectedInstitutions((prev) => ({
                        ...prev,
                        [categoryName]: e.target.value,
                      }));
                    }}
                    className="w-full px-3 py-2 text-sm border border-stone-300 rounded-md focus:ring-2 focus:ring-rose-200 focus:border-rose-400 bg-white"
                  >
                    <option value="all">{categoryData.icon} All {categoryName}</option>
                    {categoryData.institutions.map((inst) => (
                      <option key={inst.id} value={inst.id}>
                        {inst.name}
                      </option>
                    ))}
                  </select>
                ))}
              </div>
            </div>

            {/* Events List */}
            <div className="space-y-4">
              {filteredEvents.map((event) => (
                <div key={event.id} className="bg-white rounded-md shadow p-4">
                  <h3 className="font-semibold text-sm text-stone-800">
                    {event.title}
                  </h3>
                  <p className="text-xs text-stone-600">
                    {getInstitutionName(event.museum)} – {event.date} {event.time}
                  </p>
                </div>
              ))}

              {filteredEvents.length === 0 && (
                <p className="text-stone-500 text-sm">No events found matching your criteria.</p>
              )}
            </div>

            <div className="text-center pt-4">
              {!isConnected ? (
                <button
                  onClick={connectCalendar}
                  disabled={!isGoogleLoaded}
                  className={`px-4 py-2 rounded-md font-medium transition-colors ${
                    isGoogleLoaded
                      ? "bg-rose-500 text-white hover:bg-rose-600"
                      : "bg-gray-300 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  {isGoogleLoaded ? "Connect Google Calendar" : "Loading..."}
                </button>
              ) : (
                <div className="inline-flex items-center px-3 py-2 bg-rose-50 text-rose-700 rounded-md border border-rose-200">
                  <Calendar className="w-4 h-4 mr-2" />Connected
                </div>
              )}
            </div>
          </aside>
          <section className="lg:col-span-3"></section>
        </div>
      </main>
    </div>
  );
};

export default App;
