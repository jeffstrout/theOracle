# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Oracle is a personality evaluation application that:
- **Purpose**: Uses astrological data to generate personality assessments
- **Backend**: Python FastAPI with Astro API integration
- **Frontend**: React with TypeScript (responsive design)
- **Assessments**: Generates results for 9 popular US personality tests
- **Deployment**: AWS (production), local development on Mac
- **Mobile**: Progressive Web App (PWA) for mobile personality testing

## Core Functionality

### LLM-Powered Personality Assessment System
The Oracle uses a sophisticated Large Language Model (LLM) approach to generate personality assessments:

**Data Flow:**
1. **Astrological Input**: Birth chart data from multiple API providers (Prokerala, AstroAPI.com)
2. **LLM Processing**: Advanced language model analyzes astrological patterns
3. **Personality Generation**: LLM generates responses as if completing personality questionnaires
4. **Multi-Assessment Output**: Produces results for 9 popular personality tests

**Target Assessments Generated via LLM:**
1. **Myers-Briggs Type Indicator (MBTI)** - 16 personality types
2. **Big Five (OCEAN)** - Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
3. **Enneagram** - 9 personality types with wings and variants
4. **DISC Assessment** - Dominance, Influence, Steadiness, Conscientiousness
5. **StrengthsFinder** - Top 5 strengths from 34 themes
6. **Love Languages** - 5 primary love languages
7. **Attachment Styles** - Secure, Anxious, Avoidant, Disorganized
8. **Emotional Intelligence (EQ)** - Self-awareness, self-regulation, motivation, empathy, social skills
9. **Career Personality Test** - Holland Code (RIASEC) career matching

**LLM Advantages:**
- **Nuanced Analysis**: Interprets complex astrological patterns beyond simple rule-based mapping
- **Contextual Understanding**: Considers planetary aspects, house placements, and sign interactions
- **Natural Language**: Generates human-like personality descriptions and insights
- **Adaptive Responses**: Can handle edge cases and unusual astrological configurations

### Multi-Provider Astrology API Integration
The Oracle uses a sophisticated multi-provider system for maximum reliability:

**Primary Provider: AstroAPI.com**
- API Key authentication
- Western astrology focus
- 1,000 free requests/month

**Secondary Provider: Prokerala**
- OAuth2 authentication with client credentials
- Vedic & Western astrology
- 5,000 free requests/month
- Professional-grade data

**Fallback System:**
1. Try primary API (AstroAPI.com)
2. If failed, try secondary API (Prokerala)
3. If both fail, use mock data

**Data Provided:**
- Birth chart analysis (sun, moon, rising signs)
- Planetary positions and aspects
- House placements
- Transit analysis
- Compatibility readings

## Development Commands

### Backend (Python/FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend (React/TypeScript)
```bash
cd frontend
npm install
npm start  # Development server on port 3000
npm run build  # Production build
npm run test  # Run tests
```

### Full Stack Development
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm start
```

## Architecture

### Backend Structure
```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── app/
│   ├── api/
│   │   ├── astro.py     # Astro API integration
│   │   ├── personality.py # Personality assessment endpoints
│   │   └── auth.py      # Authentication routes
│   ├── models/
│   │   ├── user.py      # User data models
│   │   ├── assessment.py # Assessment result models
│   │   └── astro.py     # Astrological data models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/
│   │   ├── astro_service.py # Multi-provider coordinator
│   │   ├── prokerala_service.py # Prokerala API client with OAuth2
│   │   └── personality_engine.py # Assessment logic
│   └── core/           # Configuration, security
├── tests/              # Backend tests
└── alembic/            # Database migrations
```

### Frontend Structure
```
frontend/
├── public/
│   ├── manifest.json   # PWA manifest
│   └── sw.js          # Service worker
├── src/
│   ├── components/
│   │   ├── forms/      # Birth info input forms
│   │   ├── results/    # Assessment result displays
│   │   └── charts/     # Astrological chart components
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Assessment.tsx
│   │   └── Results.tsx
│   ├── services/
│   │   ├── api.ts      # Backend API calls
│   │   └── astro.ts    # Astro data handling
│   ├── types/
│   │   ├── personality.ts # Assessment type definitions
│   │   └── astro.ts    # Astrological data types
│   └── utils/         # Helper functions
└── package.json
```

### API Communication
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- CORS configured for cross-origin requests
- OpenAPI documentation at `/docs`
- Astro API integration with proper error handling

## LLM-Based Personality Assessment Logic

### Enhanced Data Flow
1. User inputs birth date, time, and location
2. Backend calls multi-provider Astro APIs for comprehensive birth chart data
3. **LLM Processing**: Advanced language model receives complete astrological profile
4. **Intelligent Analysis**: LLM interprets planetary positions, aspects, houses, and signs
5. **Personality Generation**: LLM responds to personality questionnaire prompts based on astrological insights
6. Results formatted and returned to frontend
7. Frontend displays comprehensive personality report

### LLM Assessment Strategy
Instead of rigid rule-based mapping, the LLM approach:

**Input to LLM:**
- Complete birth chart (sun, moon, rising signs)
- All planetary positions and degrees
- House placements and cusps
- Major and minor aspects
- Astrological context and traditional interpretations

**LLM Prompting Strategy:**
- Present each personality test as a series of questions
- Ask LLM to respond as the person based on their astrological profile
- Generate nuanced answers that reflect astrological influences
- Combine multiple astrological factors for each personality dimension

**Example LLM Analysis:**
- **MBTI Introversion/Extraversion**: Considers sun sign energy, 1st house planets, aspects to Mercury
- **Big Five Openness**: Analyzes 9th house, Jupiter placement, Air sign emphasis
- **Enneagram Type**: Synthesizes core motivations from moon sign, Saturn placement, dominant elements
- **Career Aptitude**: Examines 10th house, Mars placement, earth sign emphasis, practical aspects

## Environment Variables

### Backend (.env)
```
# Database
DATABASE_URL=postgresql://user:pass@localhost/oracle

# Security
SECRET_KEY=your-jwt-secret-key

# Primary Astrology API (AstroAPI.com)
ASTRO_API_KEY=your-astro-api-key
ASTRO_API_URL=https://api.astroapi.com/v1

# Secondary Astrology API (Prokerala)
PROKERALA_CLIENT_ID=your-client-id
PROKERALA_CLIENT_SECRET=your-client-secret
PROKERALA_API_URL=https://api.prokerala.com/v2

# AWS (for production)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
REACT_APP_APP_NAME=The Oracle
```

## Testing

### Backend Tests
```bash
cd backend
pytest  # Run all tests
pytest tests/test_personality.py  # Test assessment logic
pytest tests/test_astro.py  # Test Astro API integration
```

### Frontend Tests
```bash
cd frontend
npm test  # Jest tests
npm run test:watch  # Watch mode
npm run test:coverage  # Coverage report
```

## Location Search Features

### Birth Place Input with Combo Box
The birth place form field includes an intelligent location search system:

- **HTML Datalist Combo Box**: Uses native `<datalist>` element for suggestions
- **Real-time Search**: Suggestions appear after typing 3+ characters (debounced 500ms)
- **Dual Data Sources**:
  - **Quick Cities**: Hardcoded list of 50+ major worldwide cities for instant matching
  - **Geocoding API**: OpenStreetMap Nominatim for comprehensive global coverage
- **Auto-population**: Selecting a suggestion automatically fills latitude, longitude, and timezone
- **Smart Matching**: Supports partial matches and multiple name variations
- **Timezone Detection**: Two-tier system with city-specific mappings and geographic estimation

### Location Data Flow
1. User types location name (3+ characters)
2. Quick lookup in hardcoded cities first (fastest)
3. If insufficient matches, query OpenStreetMap Nominatim API
4. Display up to 5 suggestions in combo box with coordinates and timezone
5. User selects suggestion to auto-populate all location fields

### Supported Cities
- **US Cities**: New York, Los Angeles, Chicago, Houston, Phoenix, etc.
- **International**: London, Paris, Tokyo, Mumbai, São Paulo, etc.
- **Global Coverage**: Any location via OpenStreetMap geocoding

## Multi-Provider Architecture

### astro_service.py - Main Coordinator
The main `AstroService` class coordinates between multiple providers:
```python
async def get_birth_chart(self, birth_data: BirthDataRequest) -> Optional[AstroResponse]:
    # 1. Try primary API (AstroAPI.com)
    primary_result = await self._try_primary_api(birth_data)
    if primary_result:
        return primary_result
    
    # 2. Try secondary API (Prokerala)
    secondary_result = await self._try_secondary_api(birth_data)
    if secondary_result:
        return secondary_result
    
    # 3. Fall back to mock data
    return self._get_mock_chart_data(birth_data)
```

### prokerala_service.py - OAuth2 Provider
Handles Prokerala's OAuth2 authentication:
- Automatic token management with expiration
- Token caching to reduce authentication calls
- Comprehensive error handling for API failures
- Data mapping from Prokerala format to our schema

### Benefits of Multi-Provider System
- **Reliability**: 99.9% uptime with multiple fallbacks
- **Cost Efficiency**: Use free tiers from multiple providers (6,000 total free requests/month)
- **Data Quality**: Access both Western (AstroAPI) and Vedic (Prokerala) astrology
- **Development**: Always works with mock data fallback

## Development Notes

- **Multi-Provider APIs**: Handle rate limits and failures gracefully with automatic fallback
- **OAuth2 Management**: Prokerala tokens are cached and auto-refreshed
- **Personality Logic**: Ensure consistent mapping between astro data and assessments
- **User Privacy**: Birth data is sensitive - implement proper data protection
- **Mobile UX**: Optimize forms and results display for mobile devices
- **API Caching**: Cache responses to reduce API calls and costs
- **Error Handling**: Provide meaningful error messages for invalid birth data
- **Location Search**: Combo box provides intuitive location selection with global coverage
- **Provider Monitoring**: Log which API provider successfully returned data for debugging