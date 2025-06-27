import requests
import json
from typing import Dict, Optional
from app.core.config import settings
from app.schemas.astro import BirthDataRequest, AstroResponse, BirthChart, PlanetPosition
from app.services.prokerala_service import prokerala_service

class AstroService:
    def __init__(self):
        self.api_key = settings.ASTRO_API_KEY
        self.base_url = settings.ASTRO_API_URL
        
    async def get_birth_chart(self, birth_data: BirthDataRequest) -> Optional[AstroResponse]:
        """
        Get birth chart data using multi-provider fallback system:
        1. Primary API (AstroAPI.com)
        2. Secondary API (Prokerala)
        3. Mock data
        """
        print("Starting multi-provider astrology data fetch...")
        
        # Try primary provider first (AstroAPI.com)
        primary_result = await self._try_primary_api(birth_data)
        if primary_result:
            print("Successfully retrieved data from primary API (AstroAPI.com)")
            return primary_result
        
        # Try secondary provider (Prokerala)
        print("Primary API failed, trying secondary provider (Prokerala)...")
        secondary_result = await self._try_secondary_api(birth_data)
        if secondary_result:
            print("Successfully retrieved data from secondary API (Prokerala)")
            return secondary_result
        
        # Fall back to mock data
        print("All API providers failed, falling back to mock data")
        return self._get_mock_chart_data(birth_data)
    
    async def _try_primary_api(self, birth_data: BirthDataRequest) -> Optional[AstroResponse]:
        """
        Try to get data from primary API (AstroAPI.com)
        """
        try:
            # Check if primary API key is configured
            if not self.api_key or self.api_key == "YOUR_ACTUAL_API_KEY_HERE":
                print("Primary API (AstroAPI.com) key not configured")
                return None
            
            # Real API call to AstroAPI.com
            payload = {
                "birth_date": birth_data.birth_date,
                "birth_time": birth_data.birth_time,
                "latitude": birth_data.latitude,
                "longitude": birth_data.longitude,
                "timezone": birth_data.timezone,
                "name": birth_data.name
            }
            
            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            print(f"Making primary API call to {self.base_url}/birth-chart")
            response = requests.post(f"{self.base_url}/birth-chart", 
                                   json=payload, headers=headers)
            
            if response.status_code == 200:
                return self._parse_api_response(response.json())
            else:
                print(f"Primary API call failed with status {response.status_code}: {response.text}")
                return None
            
        except Exception as e:
            print(f"Error calling primary API: {e}")
            return None
    
    async def _try_secondary_api(self, birth_data: BirthDataRequest) -> Optional[AstroResponse]:
        """
        Try to get data from secondary API (Prokerala)
        """
        try:
            return await prokerala_service.get_birth_chart(birth_data)
        except Exception as e:
            print(f"Error calling secondary API: {e}")
            return None
    
    def _get_mock_chart_data(self, birth_data: BirthDataRequest) -> AstroResponse:
        """Mock birth chart data for development"""
        planets = [
            PlanetPosition(name="Sun", sign="Leo", degree=15.5, house=7),
            PlanetPosition(name="Moon", sign="Scorpio", degree=22.3, house=10),
            PlanetPosition(name="Mercury", sign="Virgo", degree=8.7, house=8),
            PlanetPosition(name="Venus", sign="Cancer", degree=28.1, house=6),
            PlanetPosition(name="Mars", sign="Gemini", degree=12.9, house=5),
            PlanetPosition(name="Jupiter", sign="Sagittarius", degree=5.4, house=11),
            PlanetPosition(name="Saturn", sign="Capricorn", degree=18.2, house=12),
            PlanetPosition(name="Uranus", sign="Aquarius", degree=3.8, house=1),
            PlanetPosition(name="Neptune", sign="Pisces", degree=25.6, house=2),
            PlanetPosition(name="Pluto", sign="Scorpio", degree=17.9, house=10)
        ]
        
        birth_chart = BirthChart(
            sun_sign="Leo",
            moon_sign="Scorpio",
            rising_sign="Cancer",
            planets=planets,
            houses={
                "1": "Cancer", "2": "Leo", "3": "Virgo", "4": "Libra",
                "5": "Scorpio", "6": "Sagittarius", "7": "Capricorn", 
                "8": "Aquarius", "9": "Pisces", "10": "Aries", 
                "11": "Taurus", "12": "Gemini"
            },
            aspects=[
                {"planet1": "Sun", "planet2": "Moon", "aspect": "Square", "orb": 3.2},
                {"planet1": "Venus", "planet2": "Mars", "aspect": "Trine", "orb": 1.8}
            ]
        )
        
        return AstroResponse(
            birth_chart=birth_chart,
            raw_data={"mock": True, "birth_data": birth_data.dict()}
        )
    
    def _parse_api_response(self, response_data: Dict) -> AstroResponse:
        """Parse actual API response into our schema"""
        try:
            # This is a generic parser - you'll need to adapt this based on your actual API response format
            # Each astrology API has a different response structure
            
            # Extract basic chart information
            sun_sign = response_data.get('sun_sign', 'Leo')
            moon_sign = response_data.get('moon_sign', 'Scorpio') 
            rising_sign = response_data.get('ascendant', 'Cancer')
            
            # Parse planets data
            planets = []
            planets_data = response_data.get('planets', {})
            for planet_name, planet_info in planets_data.items():
                planet = PlanetPosition(
                    name=planet_name,
                    sign=planet_info.get('sign', 'Aries'),
                    degree=float(planet_info.get('degree', 0)),
                    house=int(planet_info.get('house', 1)),
                    retrograde=planet_info.get('retrograde', False)
                )
                planets.append(planet)
            
            # Parse houses
            houses = response_data.get('houses', {})
            
            # Parse aspects
            aspects = response_data.get('aspects', [])
            
            birth_chart = BirthChart(
                sun_sign=sun_sign,
                moon_sign=moon_sign,
                rising_sign=rising_sign,
                planets=planets,
                houses=houses,
                aspects=aspects
            )
            
            return AstroResponse(
                birth_chart=birth_chart,
                raw_data=response_data
            )
            
        except Exception as e:
            print(f"Error parsing API response: {e}")
            # Fall back to mock data if parsing fails
            return self._get_mock_chart_data(None)

astro_service = AstroService()