import requests
import json
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.schemas.astro import BirthDataRequest, AstroResponse, BirthChart, PlanetPosition

class ProkeralaService:
    def __init__(self):
        self.client_id = settings.PROKERALA_CLIENT_ID
        self.client_secret = settings.PROKERALA_CLIENT_SECRET
        self.base_url = settings.PROKERALA_API_URL
        self.access_token = None
        self.token_expires_at = None
        
    async def get_birth_chart(self, birth_data: BirthDataRequest) -> Optional[AstroResponse]:
        """
        Get birth chart data from Prokerala API with OAuth2 authentication
        """
        try:
            # Check if we have valid credentials
            if not self.client_id or self.client_id == "YOUR_PROKERALA_CLIENT_ID_HERE":
                print("Prokerala API credentials not configured")
                return None
            
            # Ensure we have a valid access token
            if not await self._ensure_valid_token():
                print("Failed to obtain valid Prokerala access token")
                return None
            
            # Prepare birth chart request
            payload = {
                "datetime": f"{birth_data.birth_date}T{birth_data.birth_time}:00",
                "coordinates": f"{birth_data.latitude},{birth_data.longitude}",
                "ayanamsa": 1  # Lahiri ayanamsa (most common)
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            print(f"Making Prokerala API call to {self.base_url}/astrology/birth-details")
            response = requests.post(
                f"{self.base_url}/astrology/birth-details", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code == 200:
                return self._parse_prokerala_response(response.json(), birth_data)
            else:
                print(f"Prokerala API call failed with status {response.status_code}: {response.text}")
                return None
            
        except Exception as e:
            print(f"Error calling Prokerala API: {e}")
            return None
    
    async def _ensure_valid_token(self) -> bool:
        """
        Ensure we have a valid OAuth2 access token
        """
        # Check if current token is still valid
        if (self.access_token and self.token_expires_at and 
            datetime.now() < self.token_expires_at - timedelta(minutes=5)):
            return True
        
        # Get new access token
        return await self._get_access_token()
    
    async def _get_access_token(self) -> bool:
        """
        Get OAuth2 access token from Prokerala
        """
        try:
            token_url = f"{self.base_url}/token"
            
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            print("Requesting new Prokerala access token...")
            response = requests.post(token_url, data=payload, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                print(f"Successfully obtained Prokerala access token (expires in {expires_in}s)")
                return True
            else:
                print(f"Failed to get Prokerala access token: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error getting Prokerala access token: {e}")
            return False
    
    def _parse_prokerala_response(self, response_data: Dict, birth_data: BirthDataRequest) -> AstroResponse:
        """
        Parse Prokerala API response into our standard schema
        """
        try:
            print("Parsing Prokerala API response...")
            
            # Prokerala typically returns data in this structure
            data = response_data.get("data", {})
            
            # Extract basic chart information
            sun_sign = self._extract_sign_from_planet(data, "Sun")
            moon_sign = self._extract_sign_from_planet(data, "Moon")
            rising_sign = data.get("ascendant", {}).get("sign", {}).get("name", "Cancer")
            
            # Parse planets data
            planets = []
            planets_data = data.get("planets", [])
            
            for planet_info in planets_data:
                planet = PlanetPosition(
                    name=planet_info.get("name", "Unknown"),
                    sign=planet_info.get("sign", {}).get("name", "Aries"),
                    degree=float(planet_info.get("longitude", 0)) % 30,  # Degree within sign
                    house=int(planet_info.get("house", 1)),
                    retrograde=planet_info.get("is_retrograde", False)
                )
                planets.append(planet)
            
            # Parse houses - Prokerala returns house cusp information
            houses = {}
            house_data = data.get("houses", [])
            for i, house_info in enumerate(house_data[:12], 1):
                houses[str(i)] = house_info.get("sign", {}).get("name", "Aries")
            
            # Parse aspects - Prokerala may include planetary aspects
            aspects = []
            aspects_data = data.get("aspects", [])
            for aspect_info in aspects_data:
                aspects.append({
                    "planet1": aspect_info.get("planet1", {}).get("name", ""),
                    "planet2": aspect_info.get("planet2", {}).get("name", ""),
                    "aspect": aspect_info.get("aspect_name", ""),
                    "orb": float(aspect_info.get("orb", 0))
                })
            
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
                raw_data={"prokerala_data": response_data}
            )
            
        except Exception as e:
            print(f"Error parsing Prokerala API response: {e}")
            # Return mock data if parsing fails
            return self._get_fallback_chart_data(birth_data)
    
    def _extract_sign_from_planet(self, data: Dict, planet_name: str) -> str:
        """
        Helper to extract zodiac sign for a specific planet
        """
        planets = data.get("planets", [])
        for planet in planets:
            if planet.get("name", "").lower() == planet_name.lower():
                return planet.get("sign", {}).get("name", "Leo")
        return "Leo"  # Default fallback
    
    def _get_fallback_chart_data(self, birth_data: BirthDataRequest) -> AstroResponse:
        """
        Fallback chart data if Prokerala parsing fails
        """
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
            raw_data={"fallback": True, "birth_data": birth_data.dict()}
        )

prokerala_service = ProkeralaService()