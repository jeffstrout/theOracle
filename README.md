# The Oracle

A personality evaluation application that uses astrological data from Astro API to generate comprehensive personality assessments across the nine most popular personality tests in the United States.

## 🎯 Vision

The Oracle combines astrological insights with modern personality psychology to provide users with detailed, accurate personality evaluations. Built as a responsive web application that works seamlessly across devices, with the flexibility to deploy locally and scale to AWS production infrastructure.

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **External API**: Astro API integration for astrological data
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy with Alembic migrations
- **Personality Logic**: Custom algorithms mapping astro data to personality assessments
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: CSS Modules / Styled Components (TBD)
- **State Management**: React Context / Redux Toolkit (TBD)
- **Testing**: Jest, React Testing Library
- **Build Tool**: Create React App / Vite (TBD)

### Mobile & PWA
- **Progressive Web App**: Service workers, offline support
- **Responsive Design**: Mobile-first approach
- **Future**: React Native conversion for native iOS/Android apps

### Cloud Infrastructure (AWS)
- **API Hosting**: AWS Lambda + API Gateway (or ECS Fargate)
- **Frontend**: S3 + CloudFront CDN
- **Database**: RDS PostgreSQL
- **Authentication**: AWS Cognito integration
- **Storage**: S3 for file uploads

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (for production setup)

### Local Development Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd theOracle
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Mac/Linux
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run development servers**
   ```bash
   # Terminal 1 - Backend API
   cd backend && source venv/bin/activate && uvicorn main:app --reload

   # Terminal 2 - Frontend
   cd frontend && npm start
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📱 Mobile Development

### Progressive Web App (PWA)
The application includes PWA capabilities:
- **Offline Support**: Service worker caching
- **Home Screen Installation**: Add to home screen on mobile devices
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Touch Interactions**: Mobile-friendly UI components

### Web Clips (iOS/Android)
- iOS: Users can add the web app to home screen via Safari
- Android: Chrome will prompt to install the PWA
- Custom app icons and splash screens configured

### Future Mobile Apps
- React Native conversion planned for native iOS/Android applications
- Shared business logic between web and mobile versions
- Native device feature integration (camera, notifications, etc.)

## ☁️ AWS Deployment

### Production Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CloudFront    │───▶│   S3 Bucket      │    │   API Gateway   │
│   (CDN)         │    │   (Frontend)     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   AWS Lambda    │
                                               │   (Backend)     │
                                               └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   RDS           │
                                               │   (PostgreSQL)  │
                                               └─────────────────┘
```

### Deployment Process
1. **Backend**: Package FastAPI app for AWS Lambda with Mangum
2. **Frontend**: Build React app and deploy to S3 with CloudFront
3. **Database**: Set up RDS PostgreSQL instance
4. **Infrastructure**: Use AWS CDK or Terraform for infrastructure as code

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest                     # Run all tests
pytest tests/test_api.py   # Run specific test file
pytest --cov              # Run with coverage
```

### Frontend Tests
```bash
cd frontend
npm test                   # Run Jest tests
npm run test:watch         # Watch mode
npm run test:coverage      # Coverage report
```

## 📦 Project Structure

```
theOracle/
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── core/         # Configuration, security
│   │   ├── models/       # Database models
│   │   └── schemas/      # Pydantic schemas
│   ├── tests/            # Backend tests
│   ├── main.py           # FastAPI application entry
│   └── requirements.txt  # Python dependencies
├── frontend/             # React TypeScript frontend
│   ├── public/           # Static assets, PWA manifest
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page-level components
│   │   ├── services/     # API service layer
│   │   ├── hooks/        # Custom React hooks
│   │   └── types/        # TypeScript type definitions
│   └── package.json      # Node.js dependencies
├── docs/                 # Documentation
├── CLAUDE.md            # Claude Code guidance
└── README.md            # This file
```

## 🔧 Development Guidelines

### Code Style
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Use ESLint + Prettier
- **Git**: Conventional commit messages

### API Design
- RESTful endpoints with proper HTTP status codes
- OpenAPI documentation automatically generated
- Consistent error response format
- API versioning strategy

### Security
- JWT authentication with refresh tokens
- Input validation and sanitization
- CORS properly configured
- Environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support:
- Create an issue in the repository
- Review the [CLAUDE.md](./CLAUDE.md) file for development guidance