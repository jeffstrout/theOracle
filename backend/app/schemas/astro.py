from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List, Union

class BirthDataRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: float
    longitude: float
    timezone: str

class PlanetPosition(BaseModel):
    name: str
    sign: str
    degree: float
    house: int
    retrograde: bool = False

class BirthChart(BaseModel):
    sun_sign: str
    moon_sign: str
    rising_sign: str
    planets: List[PlanetPosition]
    houses: Dict[str, str]
    aspects: List[Dict[str, Union[str, float]]]

class AstroResponse(BaseModel):
    birth_chart: BirthChart
    raw_data: Dict