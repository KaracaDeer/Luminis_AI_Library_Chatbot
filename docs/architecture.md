# Architecture Guide

## 🏗️ System Overview

Luminis.AI is built with a modern microservices architecture that separates concerns and enables scalability. The system consists of several key components working together to provide intelligent book recommendations.

## 📊 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (React)       │    │   (FastAPI)     │    │   Services      │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Chat UI     │ │◄──►│ │ API Gateway │ │◄──►│ │ OpenAI      │ │
│ │ Voice Input │ │    │ │ Auth Service│ │    │ │ Whisper     │ │
│ │ Book Search │ │    │ │ RAG Engine  │ │    │ │ GPT-4       │ │
│ └─────────────┘ │    │ │ Vector DB   │ │    │ │ ChromaDB    │ │
└─────────────────┘    │ └─────────────┘ │    │ └─────────────┘ │
                       └─────────────────┘    └─────────────────┘
```

## 🎯 Component Details

### Frontend Architecture

#### Technology Stack
- **React 18** - Modern UI framework with hooks and concurrent features
- **TypeScript** - Type-safe development with enhanced IDE support
- **TailwindCSS** - Utility-first CSS framework for rapid styling
- **Framer Motion** - Production-ready motion library for animations
- **Zustand** - Lightweight state management with persistence

#### Component Structure
```
src/frontend/
├── components/
│   ├── ChatInterface.tsx      # Main chat component
│   ├── BookSearch.tsx         # Book search functionality
│   ├── VoiceRecorder.tsx      # Voice input handling
│   ├── AuthModal.tsx          # Authentication modal
│   └── OAuthCallback.tsx      # OAuth callback handler
├── stores/
│   ├── authStore.ts           # Authentication state
│   ├── chatStore.ts           # Chat history and messages
│   └── bookStore.ts           # Book data and search results
├── services/
│   ├── api.ts                 # API client and interfaces
│   ├── authService.ts         # Authentication logic
│   └── voiceService.ts        # Voice processing utilities
├── hooks/
│   ├── useAuth.ts             # Authentication hook
│   ├── useChat.ts             # Chat functionality hook
│   └── useVoice.ts            # Voice recording hook
└── contexts/
    └── AuthContext.tsx        # Authentication context
```

#### Key Features
- **Real-time Chat Interface** - WebSocket-based live communication
- **Voice Integration** - Speech-to-text with OpenAI Whisper
- **Responsive Design** - Mobile-first approach with TailwindCSS
- **State Management** - Zustand for lightweight, persistent state
- **Authentication** - JWT + OAuth2 with social login support

### Backend Architecture

#### Technology Stack
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - SQL toolkit and ORM for database operations
- **ChromaDB** - AI-native vector database for semantic search
- **LangChain** - LLM application framework for RAG implementation
- **OpenAI Integration** - GPT-4, Whisper, and Embeddings API

#### Service Architecture
```
src/backend/
├── main.py                    # FastAPI application entry point
├── models/
│   ├── auth.py               # Authentication models
│   ├── chat.py               # Chat message models
│   ├── book.py               # Book data models
│   └── user.py               # User profile models
├── services/
│   ├── auth_service.py       # JWT & OAuth2 authentication
│   ├── rag_service.py        # RAG implementation
│   ├── vector_service.py     # ChromaDB vector operations
│   └── openlibrary_service.py # Open Library API integration
├── routes/
│   ├── auth.py               # Authentication endpoints
│   ├── chat.py               # Chat and AI endpoints
│   ├── books.py              # Book search and recommendations
│   └── voice.py              # Voice processing endpoints
└── database/
    ├── database.py           # Database connection and models
    └── init_database.py      # Database initialization
```

#### API Endpoints
- **Authentication**: `/api/auth/*` - Login, register, OAuth callbacks
- **Chat**: `/api/chat` - AI conversation and recommendations
- **Books**: `/api/books` - Book search and data retrieval
- **Voice**: `/api/transcribe` - Speech-to-text processing
- **RAG**: `/api/rag/*` - Advanced AI capabilities
- **Vector**: `/api/vector/*` - Semantic search operations

### AI/ML Architecture

#### RAG (Retrieval-Augmented Generation) Pipeline
```
User Query → Vector Embedding → ChromaDB Search → Context Retrieval → GPT-4 → Response
     ↓              ↓                ↓                ↓              ↓        ↓
  "AI books"    [0.1,0.3,...]    Similar Books    Book Contexts   AI Model   Answer
```

#### Vector Database Schema
```python
# ChromaDB Collections
collections = {
    "books": {
        "metadata": ["title", "author", "genre", "description", "rating"],
        "embeddings": "text-embedding-ada-002",
        "dimensions": 1536
    },
    "conversations": {
        "metadata": ["user_id", "timestamp", "context"],
        "embeddings": "text-embedding-ada-002", 
        "dimensions": 1536
    }
}
```

#### Model Integration
- **OpenAI GPT-4** - Primary language model for conversations
- **OpenAI Whisper** - Speech-to-text conversion
- **OpenAI Embeddings** - Text vectorization for semantic search
- **ChromaDB** - Vector storage and similarity search
- **LangChain** - LLM orchestration and prompt management

### Database Architecture

#### SQLite Schema
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Chat sessions table
CREATE TABLE chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    session_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON
);

-- User preferences table
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    preferred_genres JSON,
    reading_level VARCHAR(20),
    language_preference VARCHAR(10),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Data Flow

### 1. User Authentication Flow
```
User Login → OAuth/JWT → Auth Service → User Session → Protected Routes
```

### 2. Chat Interaction Flow
```
User Message → Frontend → API Gateway → RAG Service → Vector Search → GPT-4 → Response
```

### 3. Voice Processing Flow
```
Audio Input → Whisper API → Text → Chat Processing → AI Response → Text-to-Speech
```

### 4. Book Search Flow
```
Search Query → Vector Embedding → ChromaDB → Similar Books → Open Library API → Results
```

## 🚀 Scalability Considerations

### Horizontal Scaling
- **Stateless Backend** - FastAPI services can be scaled horizontally
- **Database Sharding** - Vector database can be partitioned by user/region
- **CDN Integration** - Static assets served via CDN
- **Load Balancing** - Multiple backend instances behind load balancer

### Performance Optimization
- **Caching Strategy** - Redis for session data and API responses
- **Connection Pooling** - Database connection optimization
- **Async Processing** - Non-blocking I/O for better concurrency
- **Vector Indexing** - Optimized ChromaDB indices for fast search

### Security Architecture
- **JWT Tokens** - Stateless authentication with configurable expiration
- **OAuth2 Integration** - Secure social login with Google, GitHub, Microsoft
- **API Rate Limiting** - Prevent abuse and ensure fair usage
- **Input Validation** - Pydantic models for request/response validation
- **CORS Configuration** - Controlled cross-origin resource sharing

## 🔧 Development Architecture

### Local Development
```bash
# Frontend Development Server
npm run dev          # Vite dev server on port 5173

# Backend Development Server  
make dev             # FastAPI with auto-reload on port 5000

# Database
make db:init         # Initialize SQLite database
make db:reset        # Reset database with sample data
```

### Testing Architecture
```
tests/
├── test_backend_endpoints.py    # API endpoint testing
├── test_frontend_components.py  # React component testing
├── test_services.py             # Service layer testing
├── test_integration.py          # End-to-end testing
└── run_comprehensive_tests.py   # Test runner with coverage
```

### CI/CD Pipeline
```yaml
# GitHub Actions Workflow
stages:
  - lint: Code quality checks
  - test: Comprehensive test suite
  - build: Docker image creation
  - deploy: Production deployment
```

## 📊 Monitoring and Observability

### Logging Strategy
- **Structured Logging** - JSON format for easy parsing
- **Log Levels** - DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Request Tracing** - Correlation IDs for request tracking
- **Performance Metrics** - Response times and error rates

### Health Checks
- **API Health** - `/api/health` endpoint for service status
- **Database Health** - Connection and query performance monitoring
- **External Dependencies** - OpenAI API and Open Library availability
- **Resource Monitoring** - CPU, memory, and disk usage

## 🔒 Security Architecture

### Authentication Flow
```
User → OAuth Provider → Callback → JWT Generation → Session Management
```

### Data Protection
- **Encryption at Rest** - Database and file system encryption
- **Encryption in Transit** - HTTPS/TLS for all communications
- **API Key Management** - Secure storage of OpenAI and OAuth keys
- **Input Sanitization** - Protection against injection attacks

### Privacy Considerations
- **Data Minimization** - Only collect necessary user data
- **User Consent** - Clear privacy policy and consent mechanisms
- **Data Retention** - Configurable data retention policies
- **Right to Deletion** - User data deletion capabilities

This architecture provides a solid foundation for the Luminis.AI Library Assistant, enabling scalability, maintainability, and security while delivering an excellent user experience.
