import axios from 'axios';
import { BirthData } from '../types/astro';
import { PersonalityAssessment, PersonalityTestType } from '../types/personality';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const astroApi = {
  getBirthChart: async (birthData: BirthData) => {
    const response = await api.post('/api/astro/birth-chart', birthData);
    return response.data;
  },
};

export const personalityApi = {
  getFullAssessment: async (birthData: BirthData): Promise<PersonalityAssessment> => {
    const response = await api.post('/api/personality/full-assessment', birthData);
    return response.data;
  },

  getSingleAssessment: async (testType: PersonalityTestType, birthData: BirthData) => {
    const response = await api.post(`/api/personality/assessment/${testType}`, birthData);
    return response.data;
  },

  getAvailableTests: async () => {
    const response = await api.get('/api/personality/tests');
    return response.data;
  },
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;