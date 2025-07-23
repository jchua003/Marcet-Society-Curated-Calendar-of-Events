import React, { useState, useEffect } from 'react';
import { Calendar, MapPin, Clock, Users, BookOpen, Palette, Music, Search, Plus, ExternalLink } from 'lucide-react';
import './App.css';

const App = () => {
  // Institution Categories (based on your CSV)
  const institutionCategories = {
    "Art Museums": {
      "icon": "🖼️",
      "institutions": [
        ["moma", "MoMA"],
        ["met", "The Met"],
        ["frick", "Frick Collection"]
      ]
    },
    "Libraries & Literary": {
      "icon": "📚", 
      "institutions": [
        ["ny_society_library", "NY Society Library"],
        ["grolier_club", "Grolier Club"],
        ["poetry_society", "Poetry Society"],
        ["rizzoli", "Rizzoli Bookstore"]
      ]
    },
    "History & Culture": {
      "icon": "🏛️",
      "institutions": [
        ["womens_history", "Women's History"],
        ["ny_historical", "NY Historical Society"],
        ["asia_society", "Asia Society"],
        ["americas_society", "Americas Society"]
      ]
    },
    "Cultural Institutes": {
      "icon": "🇫🇷",
      "institutions": [
        ["albertine", "Albertine"],
        ["lalliance", "L'Alliance"]
      ]
    },
    "Arts & Social Clubs": {
      "icon": "🎭",
      "institutions": [
        ["national_arts_club", "National Arts Club"],
        ["explorers_club", "Explorer's Club"]
      ]
    },
    "Community": {
      "icon": "🏘️",
      "institutions": [
        ["morningside", "Morningside Institute"]
      ]
    }
  };

  // Sample events
  const sampleEvents = [
  {
    id: 1,
    title: 'YPC Studio Visit:',
    museum: 'moma',
    date: '2025-08-09',
    time: '7:00 PM',
    type: 'special_events',
    description: 'YPC Studio Visit:
Constanza Schaffner
6:00–7:30 p.m.
YPC offsite location
Gallery experience',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/10728'
  },
  {
    id: 2,
    title: 'Curatorial Walk-',
    museum: 'moma',
    date: '2025-09-04',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Curatorial Walk-
Through of
Jack Whitten:
The Messenger
6:00–8:00 p.m.
Sold out
MoMA, Floor 6
Gallery experience,
for members',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/10770'
  },
  {
    id: 3,
    title: 'UNIQLO Friday Nights',
    museum: 'moma',
    date: '2025-08-24',
    time: '7:00 PM',
    type: 'special_events',
    description: 'UNIQLO Friday Nights
5:30–8:30 p.m.
MoMA
Gallery experience',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/10253'
  },
  {
    id: 4,
    title: 'Drop-in Drawing',
    museum: 'moma',
    date: '2025-08-28',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Drop-in Drawing
5:30–7:30 p.m.
MoMA, Floor 1
Gallery experience',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/10619'
  },
  {
    id: 5,
    title: 'Member Early Hour',
    museum: 'moma',
    date: '2025-08-27',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Member Early Hour
9:30–10:30 a.m.
MoMA
Gallery experience,
for members',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/7435'
  },
  {
    id: 6,
    title: 'Before-Hours Tours',
    museum: 'moma',
    date: '2025-08-18',
    time: '7:00 PM',
    type: 'tours',
    description: 'Before-Hours Tours
with an Art Historian
9:30–10:30 a.m.
MoMA, Floor 5
Gallery experience',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.moma.org/calendar/events/10165'
  },
  {
    id: 7,
    title: 'Exhibitions',
    museum: 'met',
    date: '2025-08-07',
    time: '7:00 PM',
    type: 'exhibitions',
    description: 'Exhibitions',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.metmuseum.org/exhibitions'
  },
  {
    id: 8,
    title: 'Free Tours',
    museum: 'met',
    date: '2025-09-03',
    time: '7:00 PM',
    type: 'tours',
    description: 'Free Tours',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.metmuseum.org/tours'
  },
  {
    id: 9,
    title: 'Exhibitions',
    museum: 'womens_history',
    date: '2025-08-08',
    time: '7:00 PM',
    type: 'exhibitions',
    description: 'Exhibitions',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/womens-history'
  },
  {
    id: 10,
    title: 'Diane and Adam E. Max Conference on Women’s History',
    museum: 'womens_history',
    date: '2025-09-04',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Diane and Adam E. Max Conference on Women’s History',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/womens-history'
  },
  {
    id: 11,
    title: 'Upcoming Events',
    museum: 'asia_society',
    date: '2025-08-10',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Upcoming Events',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://asiasociety.org/new-york/events'
  },
  {
    id: 12,
    title: 'CURRENT EXHIBITIONS',
    museum: 'asia_society',
    date: '2025-08-15',
    time: '7:00 PM',
    type: 'exhibitions',
    description: 'CURRENT EXHIBITIONS',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://asiasociety.org/new-york/exhibitions/current'
  },
  {
    id: 13,
    title: 'PAST | FEATURED',
    museum: 'frick',
    date: '2025-08-18',
    time: '7:00 PM',
    type: 'special_events',
    description: 'PAST | FEATURED',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.frick.org/exhibitions'
  },
  {
    id: 14,
    title: 'Private Tours',
    museum: 'frick',
    date: '2025-09-02',
    time: '7:00 PM',
    type: 'tours',
    description: 'Private Tours',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.frick.org/programs'
  },
  {
    id: 15,
    title: 'IFA-Frick Symposium on the History of Art',
    museum: 'frick',
    date: '2025-08-06',
    time: '7:00 PM',
    type: 'panel_discussions',
    description: 'IFA-Frick Symposium on the History of Art
Digital Art History
Emerging Scholars',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.frick.org/programs/symposia#ifafrick'
  },
  {
    id: 16,
    title: 'Exhibitions',
    museum: 'ny_historical',
    date: '2025-08-13',
    time: '7:00 PM',
    type: 'exhibitions',
    description: 'Exhibitions',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/exhibitions'
  },
  {
    id: 17,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-27',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 18,
    title: 'Gallery Tour: Robert Caro in the Museum',
    museum: 'ny_historical',
    date: '2025-09-05',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Robert Caro in the Museum',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 19,
    title: 'Gallery Tour: Robert Caro in the Museum',
    museum: 'ny_historical',
    date: '2025-08-14',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Robert Caro in the Museum',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 20,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-01',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 21,
    title: 'Gallery Tour: Robert Caro in the Museum',
    museum: 'ny_historical',
    date: '2025-08-04',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Robert Caro in the Museum',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 22,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-02',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 23,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-11',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 24,
    title: 'Gallery Tour: Robert Caro in the Museum',
    museum: 'ny_historical',
    date: '2025-08-01',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Robert Caro in the Museum',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 25,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-25',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 26,
    title: 'Gallery Tour: Blacklisted: An American Story',
    museum: 'ny_historical',
    date: '2025-08-05',
    time: '7:00 PM',
    type: 'tours',
    description: 'Gallery Tour: Blacklisted: An American Story',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nyhistory.org/programs'
  },
  {
    id: 27,
    title: 'Ethics in Work and Everyday Life: Virtue & Romance',
    museum: 'morningside',
    date: '2025-08-25',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Ethics in Work and Everyday Life: Virtue & Romance',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.morningsideinstitute.org/cal/2025/6/10/human-flourishing-6'
  },
  {
    id: 28,
    title: 'Ethics in Work and Everyday Life: Virtue & Friendship',
    museum: 'morningside',
    date: '2025-08-23',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Ethics in Work and Everyday Life: Virtue & Friendship',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.morningsideinstitute.org/cal/2025/5/20/human-flourishing-5'
  },
  {
    id: 29,
    title: 'Ethics in Work and Everyday Life: Virtue & Work',
    museum: 'morningside',
    date: '2025-08-24',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Ethics in Work and Everyday Life: Virtue & Work',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.morningsideinstitute.org/cal/2025/4/8/human-flourishing-4'
  },
  {
    id: 30,
    title: 'LECTURES AND CONFERENCES',
    museum: 'morningside',
    date: '2025-08-10',
    time: '7:00 PM',
    type: 'lectures',
    description: 'LECTURES AND CONFERENCES',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.morningsideinstitute.org/lectures-conferences'
  },
  {
    id: 31,
    title: 'LECTURES AND CONFERENCES',
    museum: 'morningside',
    date: '2025-08-04',
    time: '7:00 PM',
    type: 'lectures',
    description: 'LECTURES AND CONFERENCES',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.morningsideinstitute.org/lectures-conferences'
  },
  {
    id: 32,
    title: 'The Albertine Book Club Reads \"I Who Have Never Known…',
    museum: 'albertine',
    date: '2025-07-29',
    time: '7:00 PM',
    type: 'readings',
    description: 'The Albertine Book Club Reads \"I Who Have Never Known…',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.albertine.com/events/the-albertine-book-club-reads-i-who-have-never-known-men-by-jacqueline-harpmann/'
  },
  {
    id: 33,
    title: 'Breadcrumb',
    museum: 'rizzoli',
    date: '2025-09-04',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Breadcrumb',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.rizzolibookstore.com/calendar'
  },
  {
    id: 34,
    title: 'Subscribe to our Newsletter',
    museum: 'rizzoli',
    date: '2025-08-22',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Subscribe to our Newsletter',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.rizzolibookstore.com/calendar'
  },
  {
    id: 35,
    title: 'Person, Place, Thing with Randy Cohen: Steve Clay and M.C. Kinniburgh',
    museum: 'grolier_club',
    date: '2025-08-13',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Person, Place, Thing with Randy Cohen: Steve Clay and M.C. Kinniburgh
Thu, Jun 26 • 6:00 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/person-place-thing-with-randy-cohen-steve-clay-and-mc-kinniburgh-tickets-1348772648299?aff=ebdsoporgprofile'
  },
  {
    id: 36,
    title: 'Lecture: Celebrating Black Bookstores',
    museum: 'grolier_club',
    date: '2025-07-29',
    time: '7:00 PM',
    type: 'lectures',
    description: 'Lecture: Celebrating Black Bookstores
Fri, Jun 13 • 6:00 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/lecture-celebrating-black-bookstores-tickets-1367365500019?aff=ebdsoporgprofile'
  },
  {
    id: 37,
    title: '19th-Century Novels Revived by Mandylion Press',
    museum: 'grolier_club',
    date: '2025-09-01',
    time: '7:00 PM',
    type: 'special_events',
    description: '19th-Century Novels Revived by Mandylion Press
Tue, Jun 3 • 6:30 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/19th-century-novels-revived-by-mandylion-press-tickets-1256037444809?aff=ebdsoporgprofile'
  },
  {
    id: 38,
    title: 'Lecture: Bettina von Arnim and Goethe\'s Letters',
    museum: 'grolier_club',
    date: '2025-08-07',
    time: '7:00 PM',
    type: 'lectures',
    description: 'Lecture: Bettina von Arnim and Goethe\'s Letters
Thu, May 29 • 6:00 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/lecture-bettina-von-arnim-and-goethes-letters-tickets-1274474791409?aff=ebdsoporgprofile'
  },
  {
    id: 39,
    title: 'After Words: A Roundtable on Visual Poetry',
    museum: 'grolier_club',
    date: '2025-08-16',
    time: '7:00 PM',
    type: 'special_events',
    description: 'After Words: A Roundtable on Visual Poetry
Thu, May 22 • 6:00 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/after-words-a-roundtable-on-visual-poetry-tickets-1269543902989?aff=ebdsoporgprofile'
  },
  {
    id: 40,
    title: 'Lecture: UFOs, Men in Black, and the Unbelievable Life of Gray Barker',
    museum: 'grolier_club',
    date: '2025-08-22',
    time: '7:00 PM',
    type: 'lectures',
    description: 'Lecture: UFOs, Men in Black, and the Unbelievable Life of Gray Barker
Mon, May 19 • 6:00 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/lecture-ufos-men-in-black-and-the-unbelievable-life-of-gray-barker-tickets-1259769176519?aff=ebdsoporgprofile'
  },
  {
    id: 41,
    title: 'Code Name Puritan: A Grolierite Spy',
    museum: 'grolier_club',
    date: '2025-08-16',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Code Name Puritan: A Grolierite Spy
Tue, May 13 • 6:30 PM
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/code-name-puritan-a-grolierite-spy-tickets-1274423728679?aff=ebdsoporgprofile'
  },
  {
    id: 42,
    title: 'Virtual Lecture: Richard Kopley & Susan Jaffe Tane on Edgar Allan Poe',
    museum: 'grolier_club',
    date: '2025-08-18',
    time: '7:00 PM',
    type: 'lectures',
    description: 'Virtual Lecture: Richard Kopley & Susan Jaffe Tane on Edgar Allan Poe
Mon, May 12 • 10:00 PM UTC
Free',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.eventbrite.com/e/virtual-lecture-richard-kopley-susan-jaffe-tane-on-edgar-allan-poe-tickets-1274320199019?aff=ebdsoporgprofile'
  },
  {
    id: 43,
    title: 'EVENTS CALENDAR',
    museum: 'national_arts_club',
    date: '2025-08-17',
    time: '7:00 PM',
    type: 'special_events',
    description: 'EVENTS CALENDAR',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nacnyc.org/Default.aspx?p=v35Calendar&title=Events%20Calendar&view=l3&ssid=323485&vnf=1'
  },
  {
    id: 44,
    title: 'CURRENT EXHIBITIONS',
    museum: 'national_arts_club',
    date: '2025-09-04',
    time: '7:00 PM',
    type: 'exhibitions',
    description: 'CURRENT EXHIBITIONS',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.nacnyc.org/arts-and-programs/exhibitions'
  },
  {
    id: 45,
    title: '403 - Forbidden',
    museum: 'explorers_club',
    date: '2025-08-24',
    time: '7:00 PM',
    type: 'special_events',
    description: '403 - Forbidden',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://www.explorers.org/calendar-of-events/month/'
  },
  {
    id: 46,
    title: 'Follow PSNY on Eventbrite and Instagram to ensure you get notified whenever we post a new event. Don’t miss out!',
    museum: 'poetry_society',
    date: '2025-08-30',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Follow PSNY on Eventbrite and Instagram to ensure you get notified whenever we post a new event. Don’t miss out!',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://psny.eventbrite.com/'
  },
  {
    id: 47,
    title: 'Join us at The New York Poetry Festival!',
    museum: 'poetry_society',
    date: '2025-08-21',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Join us at The New York Poetry Festival!',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://poetrysocietyny.org/nycpofest'
  },
  {
    id: 48,
    title: 'Join us at Poetry Camp 2025!',
    museum: 'poetry_society',
    date: '2025-08-13',
    time: '7:00 PM',
    type: 'special_events',
    description: 'Join us at Poetry Camp 2025!',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://poetrysocietyny.org/poetry-camp'
  },
  {
    id: 49,
    title: 'lallianceny.org',
    museum: 'lalliance',
    date: '2025-09-05',
    time: '7:00 PM',
    type: 'special_events',
    description: 'lallianceny.org',
    city: 'New York',
    price: 'See website',
    duration: '2 hours',
    link: 'https://lallianceny.org/events/'
  }
  ];

  // State
  const [selectedCity, setSelectedCity] = useState('New York');
  const [filterType, setFilterType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedInstitutions, setSelectedInstitutions] = useState({});

  // Event types
  const eventTypes = [
    { id: 'all', label: 'All Events', icon: Calendar },
    { id: 'exhibitions', label: 'Exhibitions', icon: Palette },
    { id: 'talks', label: 'Talks & Lectures', icon: Users },
    { id: 'readings', label: 'Readings', icon: BookOpen },
    { id: 'workshops', label: 'Workshops', icon: Music }
  ];

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

  // Filter events
  const selectedInstIds = getSelectedInstitutionIds();
  const filteredEvents = sampleEvents.filter(event => {
    const matchesCity = event.city === selectedCity;
    const matchesType = filterType === 'all' || event.type === filterType;
    const matchesInstitution = selectedInstIds.length === 0 || selectedInstIds.includes(event.museum);
    const matchesSearch = searchQuery === '' || 
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesCity && matchesType && matchesInstitution && matchesSearch;
  });

  // Get institution display name
  const getInstitutionName = (museumId) => {
    for (const category of Object.values(institutionCategories)) {
      for (const [id, name] of category.institutions) {
        if (id === museumId) return name;
      }
    }
    return museumId;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-stone-100">
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
                      ? 'bg-rose-500 text-white'
                      : 'bg-white text-stone-700 border border-stone-300 hover:bg-stone-50'
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
          <h3 className="text-lg font-semibold text-stone-700 mb-4">Filter by Institution Category:</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
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
                  onClick={() => window.open(event.link, '_blank')}
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
            <p className="text-stone-500 text-lg">No events found matching your criteria.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
