import React, { useState } from 'react';
import { BirthData } from '../types/astro';

interface BirthDataFormProps {
  onSubmit: (data: BirthData) => void;
  loading: boolean;
}

const BirthDataForm: React.FC<BirthDataFormProps> = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState<BirthData>({
    name: '',
    birth_date: '',
    birth_time: '',
    birth_place: '',
    latitude: 0,
    longitude: 0,
    timezone: 'America/New_York'
  });
  const [coordinatesFound, setCoordinatesFound] = useState(false);
  const [searchTimeout, setSearchTimeout] = useState<NodeJS.Timeout | null>(null);
  const [suggestions, setSuggestions] = useState<Array<{name: string, lat: number, lng: number, timezone: string}>>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleSuggestionSelect = (suggestion: {name: string, lat: number, lng: number, timezone: string}) => {
    setFormData(prev => ({
      ...prev,
      birth_place: suggestion.name,
      latitude: suggestion.lat,
      longitude: suggestion.lng,
      timezone: suggestion.timezone
    }));
    setCoordinatesFound(true);
    setShowSuggestions(false);
    setSuggestions([]);
    console.log(`Selected suggestion: ${suggestion.name}`);
  };

  // Function to get timezone from coordinates
  const getTimezoneForCoords = async (lat: number, lng: number): Promise<string> => {
    try {
      // Using WorldTimeAPI (completely free, no API key required)
      const response = await fetch(
        `https://worldtimeapi.org/api/timezone`
      );
      
      if (response.ok) {
        const timezones = await response.json();
        // Use a simple geographic approximation to find closest timezone
        return estimateTimezoneFromCoords(lat, lng, timezones);
      }
    } catch (error) {
      console.log('WorldTimeAPI failed, using geographic estimation...');
    }
    
    // Fallback: Geographic timezone estimation
    return estimateTimezoneFromCoords(lat, lng);
  };

  // Function to estimate timezone based on coordinates
  const estimateTimezoneFromCoords = (lat: number, lng: number, availableTimezones?: string[]): string => {
    // Specific city mappings for better accuracy
    const cityTimezones = [
      { name: 'Mumbai', lat: 19.0760, lng: 72.8777, timezone: 'Asia/Kolkata' },
      { name: 'Delhi', lat: 28.7041, lng: 77.1025, timezone: 'Asia/Kolkata' },
      { name: 'Bangkok', lat: 13.7563, lng: 100.5018, timezone: 'Asia/Bangkok' },
      { name: 'Singapore', lat: 1.3521, lng: 103.8198, timezone: 'Asia/Singapore' },
      { name: 'Hong Kong', lat: 22.3193, lng: 114.1694, timezone: 'Asia/Hong_Kong' },
      { name: 'Beijing', lat: 39.9042, lng: 116.4074, timezone: 'Asia/Shanghai' },
      { name: 'Shanghai', lat: 31.2304, lng: 121.4737, timezone: 'Asia/Shanghai' },
      { name: 'Jakarta', lat: -6.2088, lng: 106.8456, timezone: 'Asia/Jakarta' },
      { name: 'Manila', lat: 14.5995, lng: 120.9842, timezone: 'Asia/Manila' },
      { name: 'Karachi', lat: 24.8607, lng: 67.0011, timezone: 'Asia/Karachi' },
      { name: 'Dubai', lat: 25.2048, lng: 55.2708, timezone: 'Asia/Dubai' },
      { name: 'Istanbul', lat: 41.0082, lng: 28.9784, timezone: 'Europe/Istanbul' },
      { name: 'Cairo', lat: 30.0444, lng: 31.2357, timezone: 'Africa/Cairo' },
      { name: 'Lagos', lat: 6.5244, lng: 3.3792, timezone: 'Africa/Lagos' },
      { name: 'Mexico City', lat: 19.4326, lng: -99.1332, timezone: 'America/Mexico_City' },
      { name: 'São Paulo', lat: -23.5505, lng: -46.6333, timezone: 'America/Sao_Paulo' },
      { name: 'Buenos Aires', lat: -34.6037, lng: -58.3816, timezone: 'America/Argentina/Buenos_Aires' }
    ];
    
    // Find closest city match (within 2 degrees)
    for (const city of cityTimezones) {
      const latDiff = Math.abs(lat - city.lat);
      const lngDiff = Math.abs(lng - city.lng);
      if (latDiff < 2 && lngDiff < 2) {
        console.log(`Matched timezone for nearby city: ${city.name} -> ${city.timezone}`);
        return city.timezone;
      }
    }
    
    // Fallback to geographic regions
    if (lng >= -180 && lng < -157.5) return 'Pacific/Honolulu';
    if (lng >= -157.5 && lng < -135) return 'America/Anchorage';
    if (lng >= -135 && lng < -120) return 'America/Los_Angeles';
    if (lng >= -120 && lng < -105) return 'America/Denver';
    if (lng >= -105 && lng < -90) return 'America/Chicago';
    if (lng >= -90 && lng < -75) return 'America/New_York';
    if (lng >= -75 && lng < -60) return 'America/Halifax';
    if (lng >= -60 && lng < -45) return 'America/Sao_Paulo';
    if (lng >= -45 && lng < -15) return 'Atlantic/Azores';
    if (lng >= -15 && lng < 15) return 'Europe/London';
    if (lng >= 15 && lng < 30) return 'Europe/Paris';
    if (lng >= 30 && lng < 45) return 'Europe/Moscow';
    if (lng >= 45 && lng < 75) return 'Asia/Dubai';
    if (lng >= 75 && lng < 90) return 'Asia/Kolkata';
    if (lng >= 90 && lng < 105) return 'Asia/Bangkok';
    if (lng >= 105 && lng < 120) return 'Asia/Shanghai';
    if (lng >= 120 && lng < 135) return 'Asia/Tokyo';
    if (lng >= 135 && lng < 150) return 'Pacific/Sydney';
    if (lng >= 150 && lng <= 180) return 'Pacific/Auckland';
    
    return 'UTC'; // Default fallback
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'latitude' || name === 'longitude' ? parseFloat(value) || 0 : value
    }));

    // Auto-search for coordinates when birth place changes
    if (name === 'birth_place') {
      // Clear existing timeout
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
      
      // Check if the entered value matches a suggestion exactly
      const matchingSuggestion = suggestions.find(s => s.name === value);
      if (matchingSuggestion) {
        console.log(`Found exact match for: ${value}`);
        handleSuggestionSelect(matchingSuggestion);
      } else if (value.length > 2) {
        // Debounce the search to avoid too many calls
        console.log(`Searching for: ${value}`);
        const timeout = setTimeout(async () => await handleLocationSearch(value), 500);
        setSearchTimeout(timeout);
      } else {
        setCoordinatesFound(false);
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }
  };

  // Handle input focus to show suggestions
  const handleFocus = () => {
    if (suggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  // Handle input blur to hide suggestions (with delay)
  const handleBlur = () => {
    // Delay hiding to allow for clicks on suggestions
    setTimeout(() => {
      setShowSuggestions(false);
    }, 200);
  };

  const handleLocationSearch = async (place: string) => {
    if (!place || place.length < 3) {
      setSuggestions([]);
      return;
    }
    
    console.log(`Searching for suggestions for: "${place}"`);
    
    const allSuggestions: Array<{name: string, lat: number, lng: number, timezone: string}> = [];
    
    // First try the hardcoded cities for common locations (faster)
    const quickCities: Record<string, { lat: number; lng: number; timezone: string }> = {
      // US Cities
      'new york': { lat: 40.7128, lng: -74.0060, timezone: 'America/New_York' },
      'new york city': { lat: 40.7128, lng: -74.0060, timezone: 'America/New_York' },
      'nyc': { lat: 40.7128, lng: -74.0060, timezone: 'America/New_York' },
      'los angeles': { lat: 34.0522, lng: -118.2437, timezone: 'America/Los_Angeles' },
      'la': { lat: 34.0522, lng: -118.2437, timezone: 'America/Los_Angeles' },
      'chicago': { lat: 41.8781, lng: -87.6298, timezone: 'America/Chicago' },
      'houston': { lat: 29.7604, lng: -95.3698, timezone: 'America/Chicago' },
      'phoenix': { lat: 33.4484, lng: -112.0740, timezone: 'America/Phoenix' },
      'philadelphia': { lat: 39.9526, lng: -75.1652, timezone: 'America/New_York' },
      'san antonio': { lat: 29.4241, lng: -98.4936, timezone: 'America/Chicago' },
      'san diego': { lat: 32.7157, lng: -117.1611, timezone: 'America/Los_Angeles' },
      'dallas': { lat: 32.7767, lng: -96.7970, timezone: 'America/Chicago' },
      'san jose': { lat: 37.3382, lng: -121.8863, timezone: 'America/Los_Angeles' },
      'austin': { lat: 30.2672, lng: -97.7431, timezone: 'America/Chicago' },
      'san francisco': { lat: 37.7749, lng: -122.4194, timezone: 'America/Los_Angeles' },
      'seattle': { lat: 47.6062, lng: -122.3321, timezone: 'America/Los_Angeles' },
      'denver': { lat: 39.7392, lng: -104.9903, timezone: 'America/Denver' },
      'washington': { lat: 38.9072, lng: -77.0369, timezone: 'America/New_York' },
      'miami': { lat: 25.7617, lng: -80.1918, timezone: 'America/New_York' },
      'atlanta': { lat: 33.7490, lng: -84.3880, timezone: 'America/New_York' },
      'boston': { lat: 42.3601, lng: -71.0589, timezone: 'America/New_York' },
      'las vegas': { lat: 36.1699, lng: -115.1398, timezone: 'America/Los_Angeles' },
      
      // International Cities
      'london': { lat: 51.5074, lng: -0.1278, timezone: 'Europe/London' },
      'paris': { lat: 48.8566, lng: 2.3522, timezone: 'Europe/Paris' },
      'tokyo': { lat: 35.6762, lng: 139.6503, timezone: 'Asia/Tokyo' },
      'sydney': { lat: -33.8688, lng: 151.2093, timezone: 'Australia/Sydney' },
      'toronto': { lat: 43.6532, lng: -79.3832, timezone: 'America/Toronto' },
      'vancouver': { lat: 49.2827, lng: -123.1207, timezone: 'America/Vancouver' },
      'berlin': { lat: 52.5200, lng: 13.4050, timezone: 'Europe/Berlin' },
      'rome': { lat: 41.9028, lng: 12.4964, timezone: 'Europe/Rome' },
      'madrid': { lat: 40.4168, lng: -3.7038, timezone: 'Europe/Madrid' },
      'amsterdam': { lat: 52.3676, lng: 4.9041, timezone: 'Europe/Amsterdam' },
      'moscow': { lat: 55.7558, lng: 37.6176, timezone: 'Europe/Moscow' },
      'mumbai': { lat: 19.0760, lng: 72.8777, timezone: 'Asia/Kolkata' },
      'delhi': { lat: 28.7041, lng: 77.1025, timezone: 'Asia/Kolkata' },
      'beijing': { lat: 39.9042, lng: 116.4074, timezone: 'Asia/Shanghai' },
      'shanghai': { lat: 31.2304, lng: 121.4737, timezone: 'Asia/Shanghai' },
      'hong kong': { lat: 22.3193, lng: 114.1694, timezone: 'Asia/Hong_Kong' },
      'singapore': { lat: 1.3521, lng: 103.8198, timezone: 'Asia/Singapore' },
      'melbourne': { lat: -37.8136, lng: 144.9631, timezone: 'Australia/Melbourne' },
      'mexico city': { lat: 19.4326, lng: -99.1332, timezone: 'America/Mexico_City' },
      'sao paulo': { lat: -23.5505, lng: -46.6333, timezone: 'America/Sao_Paulo' },
      'buenos aires': { lat: -34.6037, lng: -58.3816, timezone: 'America/Argentina/Buenos_Aires' }
    };

    // Normalize input for matching
    const normalizedPlace = place.toLowerCase().trim();
    console.log(`Normalized search: "${normalizedPlace}"`);
    
    // Find all matching quick cities
    for (const [cityName, cityCoords] of Object.entries(quickCities)) {
      if (cityName.includes(normalizedPlace) || cityName.startsWith(normalizedPlace)) {
        allSuggestions.push({
          name: cityName.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
          lat: cityCoords.lat,
          lng: cityCoords.lng,
          timezone: cityCoords.timezone
        });
      }
    }
    
    // If we have fewer than 5 suggestions, try geocoding service for more
    if (allSuggestions.length < 5) {
      console.log('Adding geocoding suggestions...');
      try {
        const encodedPlace = encodeURIComponent(place);
        const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&limit=5&q=${encodedPlace}`;
        
        const response = await fetch(geocodeUrl, {
          headers: {
            'User-Agent': 'The Oracle Personality App'
          }
        });
        
        const data = await response.json();
        
        if (data && data.length > 0) {
          for (const result of data) {
            const lat = parseFloat(result.lat);
            const lng = parseFloat(result.lon);
            const displayName = result.display_name.split(',').slice(0, 2).join(', ');
            
            // Get timezone for the coordinates
            const timezone = await getTimezoneForCoords(lat, lng);
            
            allSuggestions.push({
              name: displayName,
              lat: lat,
              lng: lng,
              timezone: timezone
            });
            
            // Limit to 5 total suggestions
            if (allSuggestions.length >= 5) break;
          }
          console.log(`Geocoding found ${data.length} suggestions`);
        }
      } catch (error) {
        console.error('Geocoding error:', error);
      }
    }

    // Update suggestions
    setSuggestions(allSuggestions);
    setShowSuggestions(allSuggestions.length > 0);
    console.log(`Found ${allSuggestions.length} suggestions:`, allSuggestions.map(s => s.name));
    
    // If only one suggestion and it's an exact match, auto-select it
    if (allSuggestions.length === 1 && allSuggestions[0].name.toLowerCase() === normalizedPlace) {
      const coords = allSuggestions[0];
      setFormData(prev => ({
        ...prev,
        latitude: coords.lat,
        longitude: coords.lng,
        timezone: coords.timezone
      }));
      setCoordinatesFound(true);
      setShowSuggestions(false);
      console.log(`Auto-selected exact match: ${coords.name}`);
    } else {
      setCoordinatesFound(false);
    }
  };

  return (
    <div className="birth-data-form">
      <h2>Enter Your Birth Information</h2>
      <p>To generate your personality assessment, we need your birth details for astrological analysis.</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter your full name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="birth_date">Birth Date:</label>
          <input
            type="date"
            id="birth_date"
            name="birth_date"
            value={formData.birth_date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="birth_time">Birth Time:</label>
          <input
            type="time"
            id="birth_time"
            name="birth_time"
            value={formData.birth_time}
            onChange={handleChange}
            required
          />
          <small>Enter the exact time you were born (as accurate as possible)</small>
        </div>

        <div className="form-group" style={{position: 'relative'}}>
          <label htmlFor="birth_place">Birth Place:</label>
          <input
            type="text"
            id="birth_place"
            name="birth_place"
            value={formData.birth_place}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            required
            placeholder="Any city worldwide (e.g., New York, Paris, Mumbai, etc.)"
            autoComplete="off"
          />
          
          {/* Custom Dropdown */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions-dropdown">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="suggestion-item"
                  onClick={() => handleSuggestionSelect(suggestion)}
                >
                  <div className="suggestion-name">{suggestion.name}</div>
                  <div className="suggestion-details">
                    {suggestion.lat.toFixed(4)}, {suggestion.lng.toFixed(4)} • {suggestion.timezone}
                  </div>
                </div>
              ))}
            </div>
          )}
          
          <small>
            Type any city name worldwide - select from dropdown suggestions
            {coordinatesFound && <span style={{color: 'green', fontWeight: 'bold'}}> ✓ Coordinates found!</span>}
            <br />
            <strong>Works with any city:</strong> New York, London, Tokyo, Mumbai, São Paulo, etc.
          </small>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="latitude">Latitude:</label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              value={formData.latitude}
              onChange={handleChange}
              step="0.0001"
              required
              placeholder="40.7128"
            />
          </div>

          <div className="form-group">
            <label htmlFor="longitude">Longitude:</label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              step="0.0001"
              required
              placeholder="-74.0060"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="timezone">Timezone:</label>
          <select
            id="timezone"
            name="timezone"
            value={formData.timezone}
            onChange={handleChange}
            required
          >
            <option value="America/New_York">Eastern Time (ET)</option>
            <option value="America/Chicago">Central Time (CT)</option>
            <option value="America/Denver">Mountain Time (MT)</option>
            <option value="America/Los_Angeles">Pacific Time (PT)</option>
            <option value="America/Halifax">Atlantic Time (AT)</option>
            <option value="America/Sao_Paulo">São Paulo (BRT)</option>
            <option value="America/Mexico_City">Mexico City (CST)</option>
            <option value="America/Argentina/Buenos_Aires">Buenos Aires (ART)</option>
            <option value="Europe/London">London (GMT)</option>
            <option value="Europe/Paris">Paris (CET)</option>
            <option value="Europe/Moscow">Moscow (MSK)</option>
            <option value="Europe/Istanbul">Istanbul (TRT)</option>
            <option value="Africa/Cairo">Cairo (EET)</option>
            <option value="Africa/Lagos">Lagos (WAT)</option>
            <option value="Asia/Dubai">Dubai (GST)</option>
            <option value="Asia/Kolkata">India (IST)</option>
            <option value="Asia/Bangkok">Bangkok (ICT)</option>
            <option value="Asia/Shanghai">China (CST)</option>
            <option value="Asia/Tokyo">Tokyo (JST)</option>
            <option value="Asia/Singapore">Singapore (SGT)</option>
            <option value="Asia/Hong_Kong">Hong Kong (HKT)</option>
            <option value="Asia/Jakarta">Jakarta (WIB)</option>
            <option value="Asia/Manila">Manila (PHT)</option>
            <option value="Pacific/Sydney">Sydney (AEDT)</option>
            <option value="Pacific/Auckland">Auckland (NZDT)</option>
            <option value="UTC">UTC</option>
          </select>
        </div>

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Fetching Astrological Data...' : 'Get My Astrological Data'}
        </button>
      </form>

      <div className="privacy-note">
        <p><strong>Privacy:</strong> Your birth information is used only to generate your assessment and is not stored permanently.</p>
      </div>
    </div>
  );
};

export default BirthDataForm;