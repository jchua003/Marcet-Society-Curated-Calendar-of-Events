import React, { useState, useEffect } from 'react';
import { Calendar, MapPin, Clock, Users, BookOpen, Palette, Music, Search, Plus, ExternalLink } from 'lucide-react';
import './App.css';

const App = () => {
  const [selectedCity, setSelectedCity] = useState('New York');
  const [selectedEvents, setSelectedEvents] = useState(new Set());
  const [filterType, setFilterType] = useState('all');
  const [selectedInstitution, setSelectedInstitution] = useState('all');
  const [isConnected, setIsConnected] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [accessToken, setAccessToken] = useState(null);
  const [isGoogleLoaded, setIsGoogleLoaded] = useState(false);

  // Replace with your OAuth Client ID from Google Cloud Console
  const GOOGLE_CLIENT_ID = '922415648629-7f6jn9v2vej7ka1knnnukvpi0i283tuk.apps.googleusercontent.com';

  // Initialize Google APIs
  useEffect(() => {
    const initializeGoogleAPIs = async () => {
      try {
        // Wait for both Google APIs to load
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
          })
        ]);

        // Initialize gapi client
        await new Promise((resolve) => {
          window.gapi.load('client', resolve);
        });

        await window.gapi.client.init({
          discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
        });

        setIsGoogleLoaded(true);
        console.log('Google APIs initialized successfully');
      } catch (error) {
        console.error('Error initializing Google APIs:', error);
      }
    };

    initializeGoogleAPIs();
  }, []);

  const cities = [
    'New York', 'Los Angeles', 'San Francisco', 'London', 'Washington DC', 'Boston', 'Chicago'
  ];

  const eventTypes = [
    { id: 'all', label: 'All Events', icon: Calendar },
    { id: 'exhibitions', label: 'Exhibitions', icon: Palette },
    { id: 'special', label: 'Special Event', icon: Users },
    { id: 'lecture', label: 'Lecture', icon: BookOpen },
    { id: 'tour', label: 'Tour', icon: MapPin },
    { id: 'performances', label: 'Performances', icon: Music },
    { id: 'panel', label: 'Panel Discussion', icon: Users },
    { id: 'talks', label: 'Talks', icon: BookOpen }
  ];

  const institutionsByCity = {
    'New York': [
      { id: 'met', name: 'Metropolitan Museum of Art', shortName: 'The Met' },
      { id: 'moma', name: 'Museum of Modern Art', shortName: 'MoMA' },
      { id: 'womens', name: 'Women\'s History Museum', shortName: 'Women\'s History' },
      { id: 'asia', name: 'Asia Society', shortName: 'Asia Society' },
      { id: 'frick', name: 'Frick Collection', shortName: 'Frick' },
      { id: 'ifa', name: 'Institute of Fine Arts NYU', shortName: 'IFA NYU' },
      { id: 'nyhs', name: 'New York Historical Society', shortName: 'NY Historical' },
      { id: 'morningside', name: 'Morningside Institute', shortName: 'Morningside' },
      { id: 'nysl', name: 'New York Society Library', shortName: 'NY Society Library' },
      { id: 'albertine', name: 'Albertine Books', shortName: 'Albertine' },
      { id: 'rizzoli', name: 'Rizzoli Bookstore', shortName: 'Rizzoli' },
      { id: 'grolier', name: 'Grolier Club', shortName: 'Grolier Club' },
      { id: 'nac', name: 'National Arts Club', shortName: 'National Arts Club' },
      { id: 'explorers', name: 'Explorer\'s Club', shortName: 'Explorer\'s Club' },
      { id: 'americas', name: 'Art at America Society', shortName: 'Americas Society' },
      { id: 'poetry', name: 'New York Poetry Society', shortName: 'Poetry Society' },
      { id: 'alliance', name: 'L\'Alliance', shortName: 'L\'Alliance' }
    ],
    'Los Angeles': [
      { id: 'lacma', name: 'Los Angeles County Museum of Art', shortName: 'LACMA' },
      { id: 'getty', name: 'Getty Center', shortName: 'Getty' },
      { id: 'broad', name: 'The Broad', shortName: 'The Broad' }
    ]
  };

  const sampleEvents = [
    {
      id: 1,
      title: 'Women in Science: Revolutionary Discoveries',
      museum: 'womens',
      date: '2025-07-20',
      time: '2:00 PM',
      type: 'lecture',
      description: 'Explore groundbreaking discoveries by women scientists and their lasting impact on our understanding of the natural world.',
      city: 'New York',
      price: 'Free',
      duration: '90 minutes'
    },
    {
      id: 2,
      title: 'Impressionist Masterpieces Exhibition',
      museum: 'met',
      date: '2025-07-22',
      time: '10:00 AM',
      type: 'exhibitions',
      description: 'A comprehensive look at Impressionist works from the museum\'s collection, featuring rarely displayed pieces.',
      city: 'New York',
      price: '$25',
      duration: 'All day'
    },
    {
      id: 3,
      title: 'Contemporary Art Discussion',
      museum: 'moma',
      date: '2025-07-25',
      time: '6:30 PM',
      type: 'panel',
      description: 'Join contemporary artists and curators for an engaging panel discussion on modern art movements.',
      city: 'New York',
      price: '$15',
      duration: '2 hours'
    },
    {
      id: 4,
      title: 'Book Launch: Asian Literature Today',
      museum: 'asia',
      date: '2025-07-24',
      time: '7:00 PM',
      type: 'talks',
      description: 'Author reading and discussion of contemporary Asian literature and its global influence.',
      city: 'New York',
      price: '$10',
      duration: '90 minutes'
    },
    {
      id: 5,
      title: 'Renaissance Art History Seminar',
      museum: 'ifa',
      date: '2025-07-26',
      time: '3:00 PM',
      type: 'lecture',
      description: 'Graduate-level seminar exploring Renaissance artistic techniques and cultural context.',
      city: 'New York',
      price: '$30',
      duration: '3 hours'
    },
    {
      id: 6,
      title: 'Garden Party & Poetry Reading',
      museum: 'frick',
      date: '2025-07-27',
      time: '4:00 PM',
      type: 'special',
      description: 'Special afternoon poetry reading in the beautiful Frick Collection garden courtyard.',
      city: 'New York',
      price: '$40',
      duration: '2 hours'
    },
    {
      id: 7,
      title: 'Literary Salon: Women Writers',
      museum: 'nysl',
      date: '2025-07-28',
      time: '6:00 PM',
      type: 'talks',
      description: 'Monthly salon discussing influential women writers and their contributions to literature.',
      city: 'New York',
      price: '$20',
      duration: '2 hours'
    },
    {
      id: 8,
      title: 'Book Arts Workshop',
      museum: 'grolier',
      date: '2025-07-29',
      time: '10:00 AM',
      type: 'special',
      description: 'Hands-on workshop in traditional bookbinding and letterpress printing techniques.',
      city: 'New York',
      price: '$65',
      duration: '4 hours'
    },
    {
      id: 9,
      title: 'Exploration Photography Exhibition',
      museum: 'explorers',
      date: '2025-07-30',
      time: '11:00 AM',
      type: 'exhibitions',
      description: 'Stunning photography from recent expeditions to remote corners of the world.',
      city: 'New York',
      price: '$15',
      duration: 'All day'
    },
    {
      id: 10,
      title: 'French Literature Circle',
      museum: 'albertine',
      date: '2025-07-31',
      time: '7:30 PM',
      type: 'talks',
      description: 'Monthly discussion of contemporary French literature with wine and light refreshments.',
      city: 'New York',
      price: '$25',
      duration: '90 minutes'
    },
    {
      id: 11,
      title: 'Contemporary Poetry Workshop',
      museum: 'poetry',
      date: '2025-08-01',
      time: '2:00 PM',
      type: 'special',
      description: 'Interactive workshop for aspiring poets to develop their craft and share their work.',
      city: 'New York',
      price: '$35',
      duration: '3 hours'
    },
    {
      id: 12,
      title: 'Art & Philosophy Panel',
      museum: 'nac',
      date: '2025-08-02',
      time: '1:00 PM',
      type: 'panel',
      description: 'Interdisciplinary panel discussion on the relationship between artistic expression and philosophical thought.',
      city: 'New York',
      price: '$20',
      duration: '2.5 hours'
    },
    {
      id: 13,
      title: 'Historical NYC Walking Tour',
      museum: 'nyhs',
      date: '2025-08-03',
      time: '10:00 AM',
      type: 'tour',
      description: 'Guided walking tour exploring the hidden history of Manhattan with historical society experts.',
      city: 'New York',
      price: '$30',
      duration: '3 hours'
    },
    {
      id: 14,
      title: 'Book Signing: Art & Culture',
      museum: 'rizzoli',
      date: '2025-08-04',
      time: '6:00 PM',
      type: 'talks',
      description: 'Author book signing and talk about the intersection of art and cultural identity.',
      city: 'New York',
      price: 'Free',
      duration: '1 hour'
    },
    {
      id: 15,
      title: 'French Cultural Evening',
      museum: 'alliance',
      date: '2025-08-05',
      time: '7:00 PM',
      type: 'performances',
      description: 'Evening of French music, poetry, and performance celebrating francophone culture.',
      city: 'New York',
      price: '$18',
      duration: '2 hours'
    }
  ];

  const filteredEvents = sampleEvents.filter(event => {
    const matchesCity = event.city === selectedCity;
    const matchesType = filterType === 'all' || event.type === filterType;
    const matchesInstitution = selectedInstitution === 'all' || event.museum === selectedInstitution;
    const matchesSearch = searchQuery === '' || 
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesCity && matchesType && matchesInstitution && matchesSearch;
  });

  const handleCityChange = (city) => {
    setSelectedCity(city);
    setSelectedInstitution('all');
  };

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
    if (!isGoogleLoaded) {
      alert('Google API is still loading. Please wait a moment and try again.');
      return;
    }

    if (GOOGLE_CLIENT_ID === 'YOUR_GOOGLE_CLIENT_ID_HERE') {
      alert('Please configure your Google Client ID first.');
      return;
    }

    try {
      window.google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/calendar.events',
        callback: (response) => {
          if (response.access_token) {
            setAccessToken(response.access_token);
            setIsConnected(true);
            window.gapi.client.setToken({ access_token: response.access_token });
            alert('Successfully connected to Google Calendar!');
          }
        },
      }).requestAccessToken();
    } catch (error) {
      console.error('Error connecting to Google Calendar:', error);
      alert('Failed to connect to Google Calendar. Please try again.');
    }
  };

  const convertTo24Hour = (time12h) => {
    const [time, modifier] = time12h.split(' ');
    let [hours, minutes] = time.split(':');
    if (hours === '12') hours = '00';
    if (modifier === 'PM') hours = parseInt(hours, 10) + 12;
    return `${hours.padStart(2, '0')}:${minutes}`;
  };

  const addSelectedToCalendar = async () => {
    if (!isConnected || !accessToken) {
      alert('Please connect your Google Calendar first.');
      return;
    }

    if (selectedEvents.size === 0) {
      alert('Please select at least one event.');
      return;
    }

    try {
      const eventsToAdd = Array.from(selectedEvents).map(eventId => {
        const event = sampleEvents.find(e => e.id === eventId);
        const startTime = convertTo24Hour(event.time);
        const startDateTime = `${event.date}T${startTime}:00`;
        
        const endTime = new Date(`${event.date}T${startTime}:00`);
        endTime.setHours(endTime.getHours() + 2);
        const endDateTime = endTime.toISOString().slice(0, 19);

        return {
          summary: event.title,
          description: `${event.description}\n\nVenue: ${getInstitutionName(event.museum)}\nPrice: ${event.price}\nDuration: ${event.duration}`,
          location: getInstitutionName(event.museum),
          start: {
            dateTime: startDateTime,
            timeZone: 'America/New_York'
          },
          end: {
            dateTime: endDateTime,
            timeZone: 'America/New_York'
          }
        };
      });

      let successCount = 0;
      for (const event of eventsToAdd) {
        try {
          await window.gapi.client.calendar.events.insert({
            calendarId: 'primary',
            resource: event
          });
          successCount++;
        } catch (error) {
          console.error('Error adding event:', error);
        }
      }

      alert(`Successfully added ${successCount} event(s) to your calendar!`);
      setSelectedEvents(new Set());
    } catch (error) {
      console.error('Error adding events to calendar:', error);
      alert('Failed to add events to calendar. Please try again.');
    }
  };

  const getInstitutionName = (institutionId) => {
    const institutions = institutionsByCity[selectedCity] || [];
    const institution = institutions.find(inst => inst.id === institutionId);
    return institution ? institution.name : 'Unknown Institution';
  };

  const getInstitutionShortName = (institutionId) => {
    const institutions = institutionsByCity[selectedCity] || [];
    const institution = institutions.find(inst => inst.id === institutionId);
    return institution ? institution.shortName : 'Unknown';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-stone-100">
      <header className="bg-white shadow-sm border-b border-stone-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <div className="w-16 h-16 bg-rose-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-rose-600 font-serif text-xl font-bold">MS</span>
              </div>
              <h1 className="text-4xl font-serif text-stone-800">
                Curated Social Intellectual Calendar
              </h1>
            </div>
            <p className="text-lg text-stone-600 max-w-2xl mx-auto leading-relaxed">
              Discover enriching intellectual experiences at museums, libraries, societies, and cultural venues
            </p>
            <div className="mt-6 p-4 bg-stone-50 rounded-lg border-l-4 border-rose-400 max-w-3xl mx-auto">
              <p className="text-stone-700 italic font-serif">
                "When you plead in favor of ignorance, there is a strong presumption that you are in the wrong."
              </p>
              <p className="text-stone-500 text-sm mt-2">— Jane Marcet</p>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-serif text-stone-700 mb-3 text-center">Select City</h3>
            <div className="flex flex-wrap justify-center gap-2">
              {cities.map(city => (
                <button
                  key={city}
                  onClick={() => handleCityChange(city)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border-2 ${
                    selectedCity === city
                      ? 'bg-rose-400 text-white shadow-md border-rose-400'
                      : 'bg-white text-stone-600 hover:bg-stone-50 border-rose-200 hover:border-rose-300'
                  }`}
                >
                  {city}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-serif text-stone-700 mb-3 text-center">Select Institution</h3>
            <div className="flex flex-wrap justify-center gap-2 max-w-5xl mx-auto">
              <button
                onClick={() => setSelectedInstitution('all')}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border-2 ${
                  selectedInstitution === 'all'
                    ? 'bg-rose-400 text-white shadow-md border-rose-400'
                    : 'bg-white text-stone-600 hover:bg-stone-50 border-rose-200 hover:border-rose-300'
                }`}
              >
                All Institutions
              </button>
              {(institutionsByCity[selectedCity] || []).map(institution => (
                <button
                  key={institution.id}
                  onClick={() => setSelectedInstitution(institution.id)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border-2 ${
                    selectedInstitution === institution.id
                      ? 'bg-rose-400 text-white shadow-md border-rose-400'
                      : 'bg-white text-stone-600 hover:bg-stone-50 border-rose-200 hover:border-rose-300'
                  }`}
                >
                  {institution.shortName}
                </button>
              ))}
            </div>
          </div>

          <div className="text-center">
            {!isConnected ? (
              <button
                onClick={connectCalendar}
                disabled={!isGoogleLoaded}
                className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 shadow-md hover:shadow-lg ${
                  isGoogleLoaded
                    ? 'bg-rose-400 text-white hover:bg-rose-500'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <Calendar className="inline-block w-5 h-5 mr-2" />
                {isGoogleLoaded ? 'Connect Google Calendar' : 'Loading...'}
              </button>
            ) : (
              <div className="inline-flex items-center px-4 py-2 bg-rose-50 text-rose-700 rounded-lg border border-rose-200">
                <Calendar className="w-5 h-5 mr-2" />
                Calendar Connected
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6 border border-stone-200">
              <h3 className="text-lg font-serif text-stone-800 mb-4">Filter Events</h3>
              
              <div className="mb-6">
                <div className="relative">
                  <Search className="absolute left-3 top-3 w-4 h-4 text-stone-400" />
                  <input
                    type="text"
                    placeholder="Search events..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border-2 border-rose-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-300 focus:border-rose-400"
                  />
                </div>
              </div>

              <div className="space-y-2 mb-6">
                <label className="block text-sm font-medium text-stone-700 mb-2">Event Type</label>
                {eventTypes.map(type => {
                  const Icon = type.icon;
                  return (
                    <button
                      key={type.id}
                      onClick={() => setFilterType(type.id)}
                      className={`w-full flex items-center px-3 py-2 rounded-lg text-sm transition-colors duration-200 border-2 ${
                        filterType === type.id
                          ? 'bg-rose-50 text-rose-800 border-rose-300'
                          : 'text-stone-600 hover:bg-stone-50 border-rose-200 hover:border-rose-300'
                      }`}
                    >
                      <Icon className="w-4 h-4 mr-3" />
                      {type.label}
                    </button>
                  );
                })}
              </div>

              {selectedEvents.size > 0 && (
                <div className="mt-6 p-4 bg-stone-50 rounded-lg border border-stone-200">
                  <h4 className="font-medium text-stone-800 mb-2">
                    Selected Events ({selectedEvents.size})
                  </h4>
                  <button 
                    onClick={addSelectedToCalendar}
                    disabled={!isConnected}
                    className={`w-full py-2 px-4 rounded-lg transition-colors duration-200 ${
                      isConnected
                        ? 'bg-rose-400 text-white hover:bg-rose-500'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {isConnected ? 'Add to My Calendar' : 'Connect Calendar First'}
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="mb-6">
              <h2 className="text-2xl font-serif text-stone-800 mb-2">
                Cultural Events in {selectedCity}
              </h2>
              <p className="text-stone-600">
                {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
              </p>
            </div>

            <div className="grid gap-6">
              {filteredEvents.map(event => (
                <div
                  key={event.id}
                  className={`bg-white rounded-lg shadow-sm border transition-all duration-200 hover:shadow-md cursor-pointer ${
                    selectedEvents.has(event.id)
                      ? 'border-rose-300 bg-rose-50'
                      : 'border-stone-200 hover:border-stone-300'
                  }`}
                  onClick={() => toggleEventSelection(event.id)}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-serif text-stone-800 mb-2">
                          {event.title}
                        </h3>
                        <div className="flex items-center text-stone-600 text-sm space-x-4 mb-2">
                          <span className="flex items-center">
                            <MapPin className="w-4 h-4 mr-1" />
                            {getInstitutionShortName(event.museum)}
                          </span>
                          <span className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {event.date} at {event.time}
                          </span>
                        </div>
                        <div className="flex items-center text-stone-500 text-sm space-x-4">
                          <span>Duration: {event.duration}</span>
                          <span>Price: {event.price}</span>
                        </div>
                      </div>
                      <div className={`ml-4 p-2 rounded-full transition-colors duration-200 ${
                        selectedEvents.has(event.id)
                          ? 'bg-rose-400 text-white'
                          : 'bg-stone-100 text-stone-400 hover:bg-stone-200'
                      }`}>
                        <Plus className="w-4 h-4" />
                      </div>
                    </div>
                    
                    <p className="text-stone-600 leading-relaxed mb-4">
                      {event.description}
                    </p>
                    
                    <div className="flex justify-between items-center pt-4 border-t border-stone-100">
                      <div className="flex space-x-2">
                        <span className="inline-block px-3 py-1 bg-stone-100 text-stone-700 text-xs rounded-full">
                          {eventTypes.find(t => t.id === event.type)?.label}
                        </span>
                        <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                          {getInstitutionShortName(event.museum)}
                        </span>
                      </div>
                      <button className="text-stone-500 hover:text-stone-700 text-sm flex items-center">
                        Learn More <ExternalLink className="w-3 h-3 ml-1" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredEvents.length === 0 && (
              <div className="text-center py-12">
                <Calendar className="w-16 h-16 text-stone-300 mx-auto mb-4" />
                <h3 className="text-lg font-serif text-stone-600 mb-2">
                  No events found
                </h3>
                <p className="text-stone-500">
                  Try adjusting your filters or check back later for new events.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-stone-200 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-stone-600">
            <p className="text-sm">
              Inspiring intellectual curiosity through cultural institutions
            </p>
            <p className="text-xs mt-2 text-stone-500">
              Built with dedication to lifelong learning
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
