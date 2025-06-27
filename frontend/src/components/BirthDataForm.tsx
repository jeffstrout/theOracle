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
  };

  const handleLocationSearch = async (place: string) => {
    // Mock coordinates for common cities - in production, use a geocoding service
    const mockCoordinates: Record<string, { lat: number; lng: number; timezone: string }> = {
      'New York': { lat: 40.7128, lng: -74.0060, timezone: 'America/New_York' },
      'Los Angeles': { lat: 34.0522, lng: -118.2437, timezone: 'America/Los_Angeles' },
      'Chicago': { lat: 41.8781, lng: -87.6298, timezone: 'America/Chicago' },
      'London': { lat: 51.5074, lng: -0.1278, timezone: 'Europe/London' },
      'Paris': { lat: 48.8566, lng: 2.3522, timezone: 'Europe/Paris' },
      'Tokyo': { lat: 35.6762, lng: 139.6503, timezone: 'Asia/Tokyo' }
    };

    const coords = mockCoordinates[place];
    if (coords) {
      setFormData(prev => ({
        ...prev,
        latitude: coords.lat,
        longitude: coords.lng,
        timezone: coords.timezone
      }));
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

        <div className="form-group">
          <label htmlFor="birth_place">Birth Place:</label>
          <input
            type="text"
            id="birth_place"
            name="birth_place"
            value={formData.birth_place}
            onChange={handleChange}
            onBlur={(e) => handleLocationSearch(e.target.value)}
            required
            placeholder="City, State/Country"
          />
          <small>We'll automatically find coordinates for common cities</small>
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
            <option value="Europe/London">London (GMT)</option>
            <option value="Europe/Paris">Paris (CET)</option>
            <option value="Asia/Tokyo">Tokyo (JST)</option>
          </select>
        </div>

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Generating Assessment...' : 'Generate My Personality Profile'}
        </button>
      </form>

      <div className="privacy-note">
        <p><strong>Privacy:</strong> Your birth information is used only to generate your assessment and is not stored permanently.</p>
      </div>
    </div>
  );
};

export default BirthDataForm;