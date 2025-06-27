export interface BirthData {
  name: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export interface PlanetPosition {
  name: string;
  sign: string;
  degree: number;
  house: number;
  retrograde: boolean;
}

export interface BirthChart {
  sun_sign: string;
  moon_sign: string;
  rising_sign: string;
  planets: PlanetPosition[];
  houses: Record<string, string>;
  aspects: Array<Record<string, string>>;
}

export interface AstroResponse {
  birth_chart: BirthChart;
  raw_data: Record<string, any>;
}