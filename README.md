# Luminis.AI - Library Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue.svg)](https://github.com/features/actions)

> **AI-powered library assistant** - Intelligent book recommendations, voice interactions, and semantic search powered by OpenAI GPT-4 and LangChain.

[🇹🇷 Turkish README](docs/README_TR.md)

## 🚀 Live Demo

**Frontend:** https://luminis-frontend.onrender.com

**Backend API:** https://luminis-backend.onrender.com

## 🔧 API Endpoints

- **Health Check:** https://luminis-backend.onrender.com/api/health
- **Books:** https://luminis-backend.onrender.com/api/books
- **Chat:** https://luminis-backend.onrender.com/api/chat

## 🎯 Demo

![Luminis.AI Demo](docs/demo.gif)

## ✨ Features

- 🤖 **AI-Powered Recommendations** - Personalized book suggestions using OpenAI GPT-4
- 🎤 **Voice Interactions** - Natural voice communication with Whisper integration
- 🔍 **Semantic Search** - Smart book discovery with ChromaDB vector search
- 🌍 **Multi-language Support** - Turkish and English language support
- 📱 **Responsive Design** - Modern, minimalist interface that works on all devices
- 🚀 **Real-time Chat** - Instant AI responses with streaming capabilities
- 📚 **RAG System** - Retrieval-Augmented Generation for accurate information
- 🔐 **User Authentication** - Secure user management and chat history
- 🔑 **JWT Authentication** - Secure token-based authentication system
- 🌐 **OAuth 2.0 Integration** - Social login with Google, GitHub, and Microsoft
- 📚 **Open Library Integration** - Access millions of books from Open Library API
- 🔄 **Dynamic Book Database** - Real-time book data synchronization
- 🎯 **Advanced Genre Matching** - Smart categorization based on book genres and moods

## 🔍 Detailed Features

### Open Library Integration
1. **Comprehensive Book Database**
   - Access to millions of books from Open Library API
   - Real-time book information and publication dates
   - Multi-language book support

2. **Smart Genre Categorization**
   - 28 different book genres
   - Mood-based book recommendations
   - Automatic genre matching

3. **Dynamic Database Synchronization**
   - Automatic addition of new books
   - Book detail updates
   - Description and rating information

### Authentication and User Management
1. **Local Registration/Login**
   - Create accounts with username, email, and password
   - Secure password hashing with bcrypt
   - JWT token-based authentication

2. **OAuth 2.0 Social Login**
   - Google, GitHub, and Microsoft integration
   - Secure OAuth flow with state validation
   - Automatic account creation for OAuth users

3. **User Profile Management**
   - View and update profile information
   - Track login history and authentication provider
   - Secure token refresh mechanism

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
- **OpenAI Integration** - GPT-4, Whisper, and Embeddings
- **JWT & OAuth2** - Authentication and authorization services

### AI & ML
- **RAG Pipeline** - Retrieval-Augmented Generation
- **Vector Embeddings** - Semantic similarity search
- **Natural Language Processing** - Advanced text understanding
- **Speech Recognition** - Speech-to-text conversion

## 📁 Project Structure

```
Luminis_AI_Library_Chatbot/
├── .github/                     # GitHub Actions and templates
│   └── workflows/               # CI/CD YAML files
│
├── docs/                        # Project documentation
│   ├── README.md                # Main README (English)
│   ├── README_TR.md             # Turkish README
│   ├── CHANGELOG.md             # Change logs
│   ├── CODE_OF_CONDUCT.md       # Code of conduct
│   └── CONTRIBUTING.md          # Contributing guide
│
├── src/                         # Source code
│   ├── backend/                 # Backend (FastAPI)
│   │   ├── main_minimal.py      # Main minimal API
│   │   ├── main.py              # Full-featured API
│   │   └── enhanced_responses.py # Enhanced responses
│   │
│   ├── frontend/                # Frontend (React + Vite)
│   │   ├── components/          # React components
│   │   │   ├── AuthModal.tsx    # Authentication modal
│   │   │   └── OAuthCallback.tsx # OAuth callback handler
│   │   ├── stores/              # Zustand state management
│   │   │   └── authStore.ts     # Authentication state store
│   │   ├── services/            # API services
│   │   ├── hooks/               # Custom React hooks
│   │   ├── contexts/            # React contexts
│   │   └── assets/              # Static files
│   │
│   ├── database/                # Database management
│   │   ├── database.py          # Database connection
│   │   └── init_database.py     # Database initialization
│   │
│   └── services/                # Shared services
│       ├── auth_service.py      # JWT & OAuth2 authentication
│       ├── openlibrary_service.py # Open Library API integration
│       ├── rag_service.py       # RAG implementation
│       └── vector_service.py    # Vector search service
│
├── tests/                       # Test files
│   ├── test_backend.py          # Backend tests
│   ├── test_frontend.py         # Frontend tests
│   └── test_integration.py      # Integration tests
│
├── scripts/                     # Helper scripts
│   ├── create_real_audio.py     # Audio creation
│   └── debug_audio.py           # Audio debugging
│
├── docker/                      # Docker files
│
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── pyproject.toml               # Python packaging
├── setup.cfg                    # Python setup configuration
├── README.md                    # Project overview
├── LICENSE                      # License file
├── CONTRIBUTING.md              # Contributing guidelines
└── Makefile                     # Build/test/run commands
```

## 🚀 Quick Start

### Requirements
- **Node.js** 18+
- **Python** 3.11+
- **OpenAI API Key** for real AI functionality

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
   cd Luminis_AI_Library_Chatbot
   ```

2. **Install dependencies**
   ```bash
   # Using Makefile (Recommended)
   make install

   # Or manually
   npm install
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp config/env.example .env
   # Edit .env file with your OpenAI API key
   ```

### Run & Test & Deploy

4. **Start the application**
   ```bash
   # Start both servers
   make dev
   # or
   npm run dev

   # Or separately:
   make backend     # Backend (port 5000)
   make frontend    # Frontend (port 5173)
   ```

5. **Access the application**
   - **Frontend (dev)**: http://localhost:5173
   - **Backend (dev)**: http://localhost:5000
   - **API Documentation (dev)**: http://localhost:5000/docs

### Postman API Testing

1. **Import Postman collection and environment:**
   - Collection: `docs/Luminis_AI_Library_API.postman_collection.json`
   - Environment: `docs/Luminis_AI_Library_API.postman_environment.json`

2. **Configure environment variables:**
   - Set `base_url` to your API endpoint:
     - Local development: `http://localhost:8000`
     - Docker: `http://localhost:8000`
     - Production: `https://your-domain.com`

3. **Test API endpoints:**
   - Health check: `GET {{base_url}}/api/health`
   - Chat with AI: `POST {{base_url}}/api/chat`
   - Get books: `GET {{base_url}}/api/books`
   - Authentication: `POST {{base_url}}/api/auth/login`

4. **Available collections:**
   - **Health & Status** - API health checks
   - **Authentication** - User registration, login, OAuth
   - **Chat & AI** - AI chat and audio transcription
   - **Books** - Book browsing and recommendations
   - **Open Library Integration** - External book database
   - **RAG** - Advanced AI capabilities
   - **Vector Search** - Semantic search functionality

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

# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

# Database
DATABASE_URL=sqlite:///./luminis_library.db

# Vector Database
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 📋 Available Commands

### Makefile Commands (Recommended)
- `make install` - Install all dependencies
- `make dev` - Start development servers
- `make build` - Production build
- `make test` - Run all tests
- `make lint` - Code linting
- `make clean` - Clean cache and build files

### NPM Commands
- `npm run dev` - Start backend + frontend together
- `npm run build` - Production build
- `npm run start` - Start production server
- `npm run test` - Run tests

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
1. **Access Millions of Books**
   - Real-time book search from Open Library API
   - Current book information and publication dates
   - Multi-language book support

2. **Smart Genre Categorization**
   - 28 different book genres
   - Mood-based book recommendations
   - Automatic genre matching

3. **Dynamic Database Synchronization**
   - Automatic addition of new books
   - Book detail updates
   - Description and rating information

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
```

## 🐳 Docker

### Quick Start
```bash
# Development mode (backend + frontend)
./docker-scripts.sh dev           # Linux/Mac
docker-scripts.bat dev            # Windows

# Production mode (all services + nginx)
./docker-scripts.sh prod          # Linux/Mac
docker-scripts.bat prod           # Windows
```

### Docker Commands
```bash
# Build all images
./docker-scripts.sh build

# Start services
./docker-scripts.sh start

# Stop services
./docker-scripts.sh stop

# View logs
./docker-scripts.sh logs

# Check health
./docker-scripts.sh health

# Clean up
./docker-scripts.sh clean
```

### Docker Services
- **Backend**: FastAPI on port 8000
- **Frontend**: React app on port 5173
- **Nginx**: Reverse proxy on port 80 (production)
- **Database**: SQLite with persistent volume
- **Vector DB**: ChromaDB with persistent storage

### Docker Compose
```bash
# Development
docker-compose up -d backend frontend

# Production
docker-compose --profile production up -d

# Stop all
docker-compose down
```

## 🤝 Contributing & Support

### Contributing
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Submit a pull request**

**For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)**

### Support
- **Issues**: [GitHub Issues](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot/discussions)
- **LinkedIn**: [Profile](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378)
- **Email**: fatmakaracaerdogan@gmail.com

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For providing state-of-the-art AI models
- **LangChain** - For the RAG framework
- **FastAPI** - For the high-performance backend framework
- **React Team** - For the amazing frontend library
