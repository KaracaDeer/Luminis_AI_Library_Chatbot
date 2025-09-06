# Luminis.AI - Library Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue.svg)](https://github.com/features/actions)

> **AI-powered library assistant** - Intelligent book recommendations, voice interactions, and semantic search powered by OpenAI GPT-4 and LangChain.

[🇹🇷 Türkçe README](README_TR.md)

## 🎯 Demo

![Luminis.AI Demo](docs/demo.gif)


## ✨ Features

- 🤖 **AI-Powered Recommendations** - Personalized book suggestions using OpenAI GPT-4
- 🎤 **Voice Interaction** - Natural voice communication with Whisper integration
- 🔍 **Semantic Search** - Smart book discovery with ChromaDB vector search
- 🌍 **Multi-language Support** - Turkish and English language support
- 📱 **Responsive Design** - Modern, minimalist interface that works on all devices
- 🚀 **Real-time Chat** - Instant AI responses with streaming features
- 📚 **RAG System** - Retrieval-Augmented Generation for accurate information
- 🔐 **User Authentication** - Secure user management and chat history
- 🔑 **JWT Authentication** - Secure token-based authentication system
- 🌐 **OAuth 2.0 Integration** - Social login with Google, GitHub and Microsoft
- 📚 **Open Library Integration** - Access to millions of books from Open Library API
- 🔄 **Dynamic Book Database** - Real-time book data synchronization
- 🎯 **Advanced Genre Matching** - Smart categorization based on book genres and moods

## 🏗️ Technology Stack

### Frontend
- **React 18** + **TypeScript** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **TailwindCSS** - Utility-first CSS framework
- **Framer Motion** - Production-ready motion library
- **GSAP** - Professional-grade animations
- **Zustand** - Lightweight state management with persistence
- **React Router** - Declarative routing
- **Authentication Components** - Login/Register modals and OAuth integration

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **ChromaDB** - AI-native vector database
- **LangChain** - LLM application framework
- **OpenAI Integration** - GPT-4, Whisper and Embeddings
- **JWT & OAuth2** - Authentication and authorization services

### AI & ML
- **RAG Pipeline** - Retrieval-Augmented Generation
- **Vector Embeddings** - Semantic similarity search
- **Natural Language Processing** - Advanced text understanding
- **Speech Recognition** - Speech-to-text conversion

## 🚀 Quick Start

### Requirements
- **Node.js** 18+ 
- **Python** 3.11+
- **OpenAI API Key** for real AI

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
   cd Luminis_AI_Library_Chatbot
   ```

2. **Install dependencies**
   ```bash
   # Node.js dependencies
   npm install
   
   # Python dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your OpenAI API key
   ```

### Run & Test & Deploy

4. **Start the application**
    ```bash
    # Start both servers
    npm run dev
    
         # Or separately:
     npm run server    # Backend (port 8000)
     npm run client    # Frontend (port 5173)
    ```

5. **Access the application**
   - **Frontend (dev)**: http://localhost:5173
   - **Backend (dev)**: http://127.0.0.1:8000
   - **API Documentation (dev)**: http://127.0.0.1:8000/docs

6. **Quick commands**
   ```bash
   # Test
   npm test                    # Run all tests
   npm run test:python        # Backend tests
   npm run test:backend       # Backend service tests
   npm run test:integration   # Integration tests
   npm run test:build         # Build test

   # Database
   npm run db:init            # Initialize database
   npm run db:reset           # Reset database
   npm run db:test            # Test database connection

   # Development
   npm run build              # Frontend build
   npm run start              # Start production server
   npm run install-deps       # Install all dependencies
   
   # Docker
   docker-compose up -d
   ```

### Postman

1. Import files from the `docs/` folder:
   - `docs/Luminis_AI_Library_API.postman_collection.json`
   - `docs/Luminis_AI_Library_API.postman_environment.json`
2. Select the imported environment and set the `base_url` value:
   - Docker: `http://localhost:8000`
   - Local development: `http://127.0.0.1:8000`
3. Example requests:
   - GET `{{base_url}}/api/health`
   - POST `{{base_url}}/api/chat` body: `{ "message": "Can you recommend me a book?", "language": "en" }`
   - GET `{{base_url}}/api/books`

### Docker (Production Ready)
```bash
# Start all services
docker-compose up -d

# Or use scripts
./docker-scripts.sh start          # Linux/Mac
docker-scripts.bat start           # Windows

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Docker Features:**
- **Multi-stage builds** - Optimized images
- **Health checks** - Service monitoring
- **Volume persistence** - Database and ChromaDB persistence
- **Nginx reverse proxy** - With security headers
- **Redis caching** - Enhanced performance

## 📖 Usage

### Basic Chat
1. Navigate to the chat interface
2. Ask questions about books, authors, or genres
3. Get AI-powered recommendations and insights

### Voice Interaction
1. Click the microphone button
2. Speak your question naturally
3. Get instant speech-to-text conversion and AI responses

### Book Discovery
1. Use semantic search to find books
2. Explore recommendations based on your preferences
3. Discover similar titles and authors

### Open Library Integration
1. **Access to Millions of Books**
   - Real-time book search from Open Library API
   - Up-to-date book information and publication dates
   - Multi-language book support

2. **Smart Genre Categorization**
   - 28 different book genres
   - Book recommendations based on mood
   - Automatic genre matching

3. **Dynamic Database Synchronization**
   - Automatic addition of new books
   - Updating book details
   - Description and rating information

### Authentication and User Management
1. **Local Registration/Login**
   - Create account with username, email and password
   - Secure password hashing with Bcrypt
   - JWT token-based authentication

2. **OAuth 2.0 Social Login**
   - Google, GitHub and Microsoft integration
   - Secure OAuth flow with state verification
   - Automatic account creation for OAuth users

3. **User Profile Management**
   - View and update profile information
   - Track login history and authentication provider
   - Secure token refresh mechanism

## 🔧 Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=8000
HOST=127.0.0.1

# Development
NODE_ENV=development
VITE_API_URL=http://localhost:8000

# JWT Authentication
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth 2.0 Configuration
OAUTH2_CLIENT_ID=your_oauth2_client_id
OAUTH2_CLIENT_SECRET=your_oauth2_client_secret
OAUTH2_REDIRECT_URI=http://localhost:5173/auth/callback

# Optional: Provider-specific OAuth credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
```

### Database Setup
The application uses SQLite by default for development. For production, configure your preferred database in the environment variables.

### API Endpoints

#### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Access token refresh
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/logout` - User logout

#### OAuth 2.0 Endpoints
- `GET /api/auth/oauth/{provider}/url` - Get OAuth authorization URL
- `GET /api/auth/oauth/{provider}/callback` - Handle OAuth callback

#### Chat and Library Endpoints
- `POST /api/chat` - Send chat message
- `GET /api/books` - Get book recommendations
- `GET /api/search` - Search books semantically

#### Open Library API Endpoints
- `GET /api/openlibrary/search` - Search books in Open Library
- `GET /api/openlibrary/popular` - Get popular books
- `POST /api/openlibrary/sync` - Sync books to local database
- `GET /api/openlibrary/health` - Open Library API health check
- `GET /api/openlibrary/genres` - List available genres

## 📁 Project Structure

```
Luminis_AI_Library_Chatbot/
├── src/                    # Source code
│   ├── frontend/           # React frontend application
│   │   ├── components/     # React components
│   │   │   ├── AuthModal.tsx   # Authentication modal
│   │   │   └── OAuthCallback.tsx # OAuth callback handler
│   │   ├── stores/         # Zustand state management
│   │   │   └── authStore.ts    # Authentication state store
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom React hooks
│   │   └── contexts/       # React contexts
│   ├── backend/            # FastAPI backend application
│   │   ├── main.py         # Main application entry point
│   │   ├── enhanced_responses.py # Enhanced response handling
│   │   └── requirements.txt # Backend dependencies
│   ├── services/           # Backend services
│   │   ├── auth_service.py     # JWT & OAuth2 authentication
│   │   ├── rag_service.py      # RAG implementation
│   │   ├── vector_service.py   # Vector search service
│   │   └── openlibrary_service.py # Open Library API integration
│   └── database/           # Database configuration
│       ├── database.py     # Database models and connection
│       └── init_database.py # Database initialization
├── tests/                  # Test suite
├── scripts/                # Utility and deployment scripts
├── docker/                 # Docker configuration files
├── docs/                   # Documentation and API collections
├── src/backend/main.py     # FastAPI application (backend entry point)
└── requirements.txt        # Python dependencies
```

*For detailed structure see [Project Documentation](docs/) or [CONTRIBUTING.md](CONTRIBUTING.md)*

## 🔒 Security Features

### Authentication and Authorization
- **JWT Tokens**: Secure access and refresh token system
- **Password Security**: Bcrypt hashing with salt rounds
- **OAuth 2.0**: Industry standard social authentication
- **Token Refresh**: Automatic token refresh for seamless UX
- **Session Management**: Secure user session handling

### Data Protection
- **HTTPS Ready**: Secure communication protocols
- **Input Validation**: Comprehensive request validation
- **SQL Injection Protection**: SQLAlchemy ORM security
- **CORS Configuration**: Cross-origin resource sharing control

## 🤝 Contributing & Support

### Contributing
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Submit a pull request**

**See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guide**

### Support
- **Issues**: [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/discussions)
- **LinkedIn**: [Profile](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378)
- **Email**: fatmakaracaerdogan@gmail.com

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For providing the latest AI models
- **LangChain** - For the RAG framework
- **FastAPI** - For the high-performance backend framework
- **React Team** - For the amazing frontend library