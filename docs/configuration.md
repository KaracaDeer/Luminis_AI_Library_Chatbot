# Configuration Guide

## ⚙️ Configuration Overview

This guide provides comprehensive information about configuring the Luminis.AI Library Assistant for different environments and use cases.

## 🔧 Environment Variables

### Core Configuration

#### API Configuration
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=500

# API Server Configuration
PORT=5000
HOST=127.0.0.1
API_RATE_LIMIT=100
API_TIMEOUT=30

# Environment
NODE_ENV=production  # development, staging, production
DEBUG=false
LOG_LEVEL=INFO
```

#### Database Configuration
```bash
# SQLite (Development)
DATABASE_URL=sqlite:///./luminis_library.db

# PostgreSQL (Production)
DATABASE_URL=postgresql://username:password@localhost:5432/luminis_library

# Database Pool Settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

#### Vector Database Configuration
```bash
# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=books
CHROMA_DISTANCE_METRIC=cosine
CHROMA_N_RESULTS=10
CHROMA_SIMILARITY_THRESHOLD=0.75

# Embedding Configuration
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_BATCH_SIZE=100
EMBEDDING_DIMENSIONS=1536
```

### Authentication Configuration

#### JWT Configuration
```bash
# JWT Settings
JWT_SECRET_KEY=your_very_strong_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_ISSUER=luminis-ai
JWT_AUDIENCE=luminis-ai-users
```

#### OAuth Configuration
```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:5173/auth/github/callback

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_REDIRECT_URI=http://localhost:5173/auth/microsoft/callback
MICROSOFT_TENANT_ID=common
```

### External Service Configuration

#### Open Library API
```bash
# Open Library Configuration
OPEN_LIBRARY_BASE_URL=https://openlibrary.org
OPEN_LIBRARY_API_VERSION=1.0
OPEN_LIBRARY_RATE_LIMIT=100
OPEN_LIBRARY_TIMEOUT=10
OPEN_LIBRARY_CACHE_TTL=3600
```

#### Redis Configuration
```bash
# Redis Settings
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password
REDIS_DB=0
REDIS_MAX_CONNECTIONS=20
REDIS_SOCKET_TIMEOUT=5
REDIS_SOCKET_CONNECT_TIMEOUT=5
```

#### File Storage Configuration
```bash
# File Upload Settings
UPLOAD_MAX_SIZE=10485760  # 10MB in bytes
UPLOAD_ALLOWED_EXTENSIONS=mp3,wav,m4a,ogg
UPLOAD_PATH=./uploads
TEMP_PATH=./temp

# Audio Processing
AUDIO_MAX_DURATION=300  # 5 minutes in seconds
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_FORMAT=wav
```

### Security Configuration

#### CORS Configuration
```bash
# CORS Settings
CORS_ORIGINS=["http://localhost:5173", "https://luminis-ai.com"]
CORS_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS=["*"]
CORS_CREDENTIALS=true
CORS_MAX_AGE=3600
```

#### Security Headers
```bash
# Security Configuration
SECURITY_HEADERS=true
HSTS_MAX_AGE=31536000
CSP_POLICY="default-src 'self'"
X_FRAME_OPTIONS=DENY
X_CONTENT_TYPE_OPTIONS=nosniff
X_XSS_PROTECTION=1; mode=block
```

#### Rate Limiting
```bash
# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # seconds
RATE_LIMIT_BURST=20
RATE_LIMIT_STORAGE=redis
```

## 🎯 Environment-Specific Configuration

### Development Environment
```bash
# .env.development
NODE_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG

# Development Database
DATABASE_URL=sqlite:///./luminis_library_dev.db
CHROMA_PERSIST_DIRECTORY=./chroma_db_dev

# Development API Keys (Use test keys)
OPENAI_API_KEY=your_openai_api_key_here

# Development CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Development Security (Relaxed)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
RATE_LIMIT_REQUESTS=1000
```

### Staging Environment
```bash
# .env.staging
NODE_ENV=staging
DEBUG=false
LOG_LEVEL=INFO

# Staging Database
DATABASE_URL=postgresql://user:pass@staging-db:5432/luminis_staging
CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db

# Staging API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Staging CORS
CORS_ORIGINS=["https://staging.luminis-ai.com"]

# Staging Security
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_REQUESTS=500
```

### Production Environment
```bash
# .env.production
NODE_ENV=production
DEBUG=false
LOG_LEVEL=WARNING

# Production Database
DATABASE_URL=postgresql://user:pass@prod-db:5432/luminis_production
CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db

# Production API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Production CORS
CORS_ORIGINS=["https://luminis-ai.com", "https://www.luminis-ai.com"]

# Production Security (Strict)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
RATE_LIMIT_REQUESTS=100
SECURITY_HEADERS=true
```

## 🔐 Secrets Management

### Environment Variable Security
```bash
# Never commit these to version control
# Use environment variables or secrets management

# Generate strong JWT secret
JWT_SECRET_KEY=$(openssl rand -base64 32)

# Generate strong database password
DB_PASSWORD=$(openssl rand -base64 16)
```

### Docker Secrets
```yaml
# docker-compose.yml with secrets
version: '3.8'
services:
  backend:
    image: luminis-ai-backend:latest
    secrets:
      - openai_api_key
      - jwt_secret_key
      - db_password
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
      - JWT_SECRET_KEY_FILE=/run/secrets/jwt_secret_key
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  openai_api_key:
    external: true
  jwt_secret_key:
    external: true
  db_password:
    external: true
```

### Kubernetes Secrets
```yaml
# kubernetes-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: luminis-ai-secrets
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
  jwt-secret-key: <base64-encoded-secret>
  db-password: <base64-encoded-password>
```

## 📊 Monitoring Configuration

### Logging Configuration
```bash
# Logging Settings
LOG_FORMAT=json  # json, text
LOG_FILE_PATH=./logs/app.log
LOG_MAX_SIZE=100MB
LOG_BACKUP_COUNT=5
LOG_COMPRESS=true

# Log Levels
LOG_LEVEL_ROOT=INFO
LOG_LEVEL_APP=DEBUG
LOG_LEVEL_DATABASE=WARNING
LOG_LEVEL_EXTERNAL=INFO
```

### Metrics Configuration
```bash
# Prometheus Metrics
METRICS_ENABLED=true
METRICS_PORT=9090
METRICS_PATH=/metrics

# Application Metrics
METRICS_REQUEST_DURATION=true
METRICS_REQUEST_COUNT=true
METRICS_ERROR_RATE=true
METRICS_DATABASE_QUERIES=true
```

### Health Check Configuration
```bash
# Health Check Settings
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_PATH=/health
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=5

# Health Check Dependencies
HEALTH_CHECK_DATABASE=true
HEALTH_CHECK_REDIS=true
HEALTH_CHECK_OPENAI=true
HEALTH_CHECK_CHROMADB=true
```

## 🔄 Cache Configuration

### Redis Cache Settings
```bash
# Cache Configuration
CACHE_ENABLED=true
CACHE_BACKEND=redis
CACHE_TTL_DEFAULT=3600
CACHE_TTL_USER_SESSION=86400
CACHE_TTL_BOOK_DATA=604800
CACHE_TTL_EMBEDDINGS=86400
CACHE_TTL_API_RESPONSES=1800
```

### Application Cache
```bash
# In-Memory Cache
MEMORY_CACHE_ENABLED=true
MEMORY_CACHE_SIZE=1000
MEMORY_CACHE_TTL=300

# Browser Cache
BROWSER_CACHE_STATIC=31536000  # 1 year
BROWSER_CACHE_API=1800         # 30 minutes
BROWSER_CACHE_HTML=0           # No cache
```

## 🎵 Audio Configuration

### Audio Processing Settings
```bash
# Audio Configuration
AUDIO_ENABLED=true
AUDIO_MAX_DURATION=300
AUDIO_MIN_DURATION=1
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_BIT_DEPTH=16

# Supported Formats
AUDIO_FORMATS=["mp3", "wav", "m4a", "ogg", "flac"]
AUDIO_MAX_FILE_SIZE=10485760  # 10MB
```

### Whisper Configuration
```bash
# OpenAI Whisper Settings
WHISPER_MODEL=whisper-1
WHISPER_LANGUAGE=auto
WHISPER_RESPONSE_FORMAT=json
WHISPER_TEMPERATURE=0.0
WHISPER_TIMESTAMP_GRANULARITIES=["word"]
```

## 📚 Book Data Configuration

### Open Library Settings
```bash
# Open Library API
OPEN_LIBRARY_SEARCH_LIMIT=20
OPEN_LIBRARY_BOOK_LIMIT=100
OPEN_LIBRARY_CACHE_TTL=3600
OPEN_LIBRARY_RETRY_ATTEMPTS=3
OPEN_LIBRARY_RETRY_DELAY=1
```

### Book Processing
```bash
# Book Data Processing
BOOK_PROCESSING_BATCH_SIZE=50
BOOK_PROCESSING_CONCURRENT=5
BOOK_PROCESSING_TIMEOUT=30
BOOK_EMBEDDING_BATCH_SIZE=100
BOOK_INDEXING_INTERVAL=3600
```

## 🔧 Advanced Configuration

### Performance Tuning
```bash
# Performance Settings
WORKER_PROCESSES=4
WORKER_CONNECTIONS=1000
KEEP_ALIVE_TIMEOUT=65
KEEP_ALIVE_REQUESTS=100

# Database Pool
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_PRE_PING=true
DB_POOL_RECYCLE=3600

# Async Settings
ASYNC_WORKERS=10
ASYNC_QUEUE_SIZE=1000
ASYNC_TASK_TIMEOUT=300
```

### Feature Flags
```bash
# Feature Toggles
FEATURE_VOICE_ENABLED=true
FEATURE_OAUTH_ENABLED=true
FEATURE_RAG_ENABLED=true
FEATURE_VECTOR_SEARCH=true
FEATURE_ANALYTICS_ENABLED=false
FEATURE_DEBUG_MODE=false
```

## 📋 Configuration Validation

### Configuration Check Script
```python
# config_validation.py
import os
from typing import Dict, List, Optional

class ConfigValidator:
    def __init__(self):
        self.required_vars = [
            'OPENAI_API_KEY',
            'JWT_SECRET_KEY',
            'DATABASE_URL'
        ]
        
        self.optional_vars = [
            'REDIS_URL',
            'CHROMA_PERSIST_DIRECTORY',
            'CORS_ORIGINS'
        ]
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate configuration and return any issues."""
        issues = {
            'missing': [],
            'invalid': [],
            'warnings': []
        }
        
        # Check required variables
        for var in self.required_vars:
            if not os.getenv(var):
                issues['missing'].append(var)
        
        # Validate specific configurations
        self._validate_database_url(issues)
        self._validate_openai_key(issues)
        self._validate_jwt_secret(issues)
        
        return issues
    
    def _validate_database_url(self, issues: Dict[str, List[str]]):
        """Validate database URL format."""
        db_url = os.getenv('DATABASE_URL')
        if db_url and not db_url.startswith(('sqlite:///', 'postgresql://')):
            issues['invalid'].append('DATABASE_URL must start with sqlite:/// or postgresql://')
    
    def _validate_openai_key(self, issues: Dict[str, List[str]]):
        """Validate OpenAI API key format."""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and not api_key.startswith('sk-'):
            issues['invalid'].append('OPENAI_API_KEY must start with sk-')
    
    def _validate_jwt_secret(self, issues: Dict[str, List[str]]):
        """Validate JWT secret strength."""
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if jwt_secret and len(jwt_secret) < 32:
            issues['warnings'].append('JWT_SECRET_KEY should be at least 32 characters')

# Usage
if __name__ == "__main__":
    validator = ConfigValidator()
    issues = validator.validate_config()
    
    if issues['missing']:
        print("Missing required variables:", issues['missing'])
    
    if issues['invalid']:
        print("Invalid configurations:", issues['invalid'])
    
    if issues['warnings']:
        print("Configuration warnings:", issues['warnings'])
```

## 🔄 Configuration Management

### Configuration Loading
```python
# config.py
import os
from typing import Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    # Core settings
    openai_api_key: str
    jwt_secret_key: str
    database_url: str
    
    # Optional settings with defaults
    port: int = 5000
    host: str = "127.0.0.1"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database settings
    db_pool_size: int = 10
    db_max_overflow: int = 20
    
    # Cache settings
    redis_url: Optional[str] = None
    cache_enabled: bool = True
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'log_level must be one of {valid_levels}')
        return v.upper()
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
```

### Environment-Specific Loading
```python
# config_loader.py
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration based on environment."""
    env = os.getenv('NODE_ENV', 'development')
    
    config_files = {
        'development': '.env.development',
        'staging': '.env.staging',
        'production': '.env.production'
    }
    
    env_file = config_files.get(env, '.env')
    
    # Load environment-specific configuration
    if os.path.exists(env_file):
        load_dotenv(env_file)
    
    return {
        'environment': env,
        'config_file': env_file,
        'loaded': True
    }
```

This comprehensive configuration guide ensures proper setup and management of the Luminis.AI Library Assistant across all environments and deployment scenarios.
