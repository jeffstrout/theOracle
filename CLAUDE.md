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

### Personality Assessment Tests
The app generates results for these 9 popular assessments:
1. **Myers-Briggs Type Indicator (MBTI)** - 16 personality types
2. **Big Five (OCEAN)** - Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
3. **Enneagram** - 9 personality types with wings and variants
4. **DISC Assessment** - Dominance, Influence, Steadiness, Conscientiousness
5. **StrengthsFinder** - Top 5 strengths from 34 themes
6. **Love Languages** - 5 primary love languages
7. **Attachment Styles** - Secure, Anxious, Avoidant, Disorganized
8. **Emotional Intelligence (EQ)** - Self-awareness, self-regulation, motivation, empathy, social skills
9. **Career Personality Test** - Holland Code (RIASEC) career matching

### Astro API Integration
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
│   │   ├── astro_service.py # Astro API client
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

## Personality Assessment Logic

### Data Flow
1. User inputs birth date, time, and location
2. Backend calls Astro API for birth chart data
3. Personality engine maps astrological data to assessment results
4. Results stored in database and returned to frontend
5. Frontend displays comprehensive personality report

### Assessment Mapping
Each personality test has custom algorithms that analyze:
- Sun sign traits → Core personality (MBTI, Big Five)
- Moon sign → Emotional patterns (EQ, Attachment)
- Rising sign → Social presentation (DISC)
- Planetary aspects → Strengths and challenges
- House placements → Life themes and career aptitude

## Environment Variables

### Backend (.env)
```
# Database
DATABASE_URL=postgresql://user:pass@localhost/oracle

# Security
SECRET_KEY=your-jwt-secret-key

# Astro API
ASTRO_API_KEY=your-astro-api-key
ASTRO_API_URL=https://api.astro-api.com

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

## Development Notes

- **Astro API**: Handle rate limits and API failures gracefully
- **Personality Logic**: Ensure consistent mapping between astro data and assessments
- **User Privacy**: Birth data is sensitive - implement proper data protection
- **Mobile UX**: Optimize forms and results display for mobile devices
- **Caching**: Cache Astro API responses to reduce API calls
- **Error Handling**: Provide meaningful error messages for invalid birth data