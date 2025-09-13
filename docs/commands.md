# Command Reference

## 📋 Command Overview

This document provides a comprehensive reference for all available commands in the Luminis.AI Library Assistant project.

## 🛠️ Development Commands

### Project Setup
```bash
# Clone the repository
git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
cd Luminis_AI_Library_Chatbot

# Install all dependencies (Python + Node.js)
make install

# Alternative: Manual installation
npm install
pip install -r src/backend/requirements.txt
```

### Development Server
```bash
# Start both frontend and backend in development mode
make dev

# Start only backend server
make server
# or
python -m uvicorn src.backend.main_minimal:app --reload --port 5000 --host 0.0.0.0

# Start only frontend server
make client
# or
cd src/frontend && npm run dev
```

### Database Management
```bash
# Initialize database with sample data
make db:init

# Reset database (drop and recreate)
make db:reset

# Manual database initialization
python src/database/init_database.py

# Reset with confirmation prompt
python src/database/init_database.py --reset
```

## 🧪 Testing Commands

### Test Execution
```bash
# Run all tests with comprehensive reporting
make test

# Run comprehensive test suite with options
python tests/run_comprehensive_tests.py

# Run tests with coverage report
make test:coverage
python tests/run_comprehensive_tests.py --coverage

# Run tests with verbose output
make test:verbose
python tests/run_comprehensive_tests.py --verbose

# Run only backend tests
make test:backend
python tests/run_comprehensive_tests.py --backend-only

# Run only frontend tests
make test:frontend
python tests/run_comprehensive_tests.py --frontend-only
```

### Individual Test Suites
```bash
# Backend API endpoint tests
python -m pytest tests/test_backend_endpoints.py -v

# Frontend component tests
python -m pytest tests/test_frontend_components.py -v

# Service layer tests
python -m pytest tests/test_services.py -v

# Integration tests
python -m pytest tests/test_integration.py -v

# Basic functionality tests
python -m pytest tests/test_basic.py -v

# Audio processing tests
python -m pytest tests/test_audio.py -v
```

### Test Coverage
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Generate coverage badge
coverage-badge -o coverage.svg

# View coverage in terminal
pytest --cov=src --cov-report=term-missing

# Coverage with specific threshold
pytest --cov=src --cov-fail-under=85
```

## 🔍 Code Quality Commands

### Linting and Formatting
```bash
# Frontend linting
make lint
cd src/frontend && npm run lint

# Fix linting issues automatically
make lint:fix
cd src/frontend && npm run lint:fix

# Format code with Prettier
make format
cd src/frontend && npm run format

# Check code formatting
cd src/frontend && npm run format:check

# TypeScript type checking
make type-check
cd src/frontend && npm run type-check
```

### Python Code Quality
```bash
# Run Black formatter
black src/ tests/

# Run isort for import sorting
isort src/ tests/

# Run flake8 linter
flake8 src/ tests/

# Run mypy type checker
mypy src/

# Run all Python quality tools
make python:quality
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Security Scanning
```bash
# Python security scan
safety check
bandit -r src/

# Node.js security scan
cd src/frontend && npm audit

# Dependency vulnerability scan
pip-audit

# Container security scan
docker run --rm -v $(pwd):/src securecodewarrior/docker-security-scan
```

## 🐳 Docker Commands

### Docker Development
```bash
# Build and start all services
make docker-up
docker-compose up -d

# Build and start with logs
docker-compose up --build

# Stop all services
make docker-down
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Docker Management
```bash
# Build specific service
docker-compose build backend
docker-compose build frontend

# Rebuild and restart service
docker-compose up --build -d backend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container status
docker-compose ps

# Scale services
docker-compose up -d --scale backend=3
```

### Docker Production
```bash
# Build production images
docker build -t luminis-backend:latest -f docker/backend.Dockerfile .
docker build -t luminis-frontend:latest -f docker/frontend.Dockerfile .

# Tag for registry
docker tag luminis-backend:latest your-registry.com/luminis-backend:latest
docker tag luminis-frontend:latest your-registry.com/luminis-frontend:latest

# Push to registry
docker push your-registry.com/luminis-backend:latest
docker push your-registry.com/luminis-frontend:latest
```

## 🚀 Build and Deployment

### Build Commands
```bash
# Build frontend for production
make build
cd src/frontend && npm run build

# Preview production build locally
make preview
cd src/frontend && npm run preview

# Build with specific environment
NODE_ENV=production npm run build
```

### Deployment Scripts
```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production

# Health check after deployment
./scripts/health_check.sh

# Rollback deployment
./scripts/rollback.sh
```

## 🔧 Utility Commands

### Project Maintenance
```bash
# Clean up temporary files
make clean
rm -rf __pycache__/ .pytest_cache/ .coverage htmlcov/
rm -rf src/frontend/node_modules/.cache/
rm -rf src/frontend/dist/

# Clean Docker resources
make docker:clean
docker system prune -f
docker volume prune -f

# Update dependencies
make update-deps
pip install -r src/backend/requirements.txt --upgrade
cd src/frontend && npm update
```

### Git Management
```bash
# Clean up git history (interactive)
./scripts/cleanup_git_history.sh

# Create release tag
./scripts/create_release.sh v1.0.0

# Generate changelog
./scripts/generate_changelog.sh
```

### Database Utilities
```bash
# Backup database
make db:backup
cp luminis_library.db backups/luminis_library_$(date +%Y%m%d_%H%M%S).db

# Restore database
make db:restore backups/luminis_library_20231201_120000.db

# Database migration
make db:migrate
python scripts/migrate_database.py

# Database seeding
make db:seed
python scripts/seed_database.py
```

## 📊 Monitoring Commands

### Health Checks
```bash
# Check service health
make health
curl -f http://localhost:5000/api/health

# Check all services
./scripts/check_all_services.sh

# Monitor logs
make logs
docker-compose logs -f

# Monitor specific service logs
make logs:backend
docker-compose logs -f backend
```

### Performance Monitoring
```bash
# Run performance tests
make perf:test
python scripts/performance_test.py

# Load testing
make perf:load
python scripts/load_test.py --users 100 --duration 300

# Memory profiling
make perf:memory
python scripts/memory_profile.py

# Database performance
make perf:db
python scripts/db_performance.py
```

## 🔍 Debugging Commands

### Debug Mode
```bash
# Start backend in debug mode
DEBUG=true python -m uvicorn src.backend.main_minimal:app --reload --port 5000

# Start with debugger
python -m debugpy --listen 5678 --wait-for-client -m uvicorn src.backend.main_minimal:app --reload

# Frontend debug mode
cd src/frontend && npm run dev -- --debug
```

### Log Analysis
```bash
# View application logs
tail -f logs/app.log

# Filter error logs
grep "ERROR" logs/app.log

# Monitor real-time logs
tail -f logs/app.log | grep -E "(ERROR|WARNING)"

# Analyze log patterns
python scripts/analyze_logs.py
```

### Database Debugging
```bash
# Connect to database
sqlite3 luminis_library.db

# Database queries
python scripts/db_queries.py

# Check database integrity
python scripts/check_db_integrity.py

# Export database schema
python scripts/export_schema.py
```

## 📱 API Testing Commands

### Manual API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI", "user_id": "test_user"}'

# Test books endpoint
curl http://localhost:5000/api/books?search=science+fiction

# Test authentication
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

### Postman Testing
```bash
# Import Postman collection
postman-cli import docs/Luminis_AI_Library_API.postman_collection.json

# Run Postman tests
postman-cli run docs/Luminis_AI_Library_API.postman_collection.json \
  --environment docs/Luminis_AI_Library_API.postman_environment.json
```

## 🔄 CI/CD Commands

### GitHub Actions
```bash
# Test GitHub Actions locally
act push

# Run specific workflow
act -W .github/workflows/test.yml

# List available workflows
act -l
```

### Local CI Simulation
```bash
# Run CI pipeline locally
make ci:local

# Run specific CI steps
make ci:lint
make ci:test
make ci:build
make ci:security
```

## 📋 Command Aliases

### Custom Aliases
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
alias ll="ls -la"
alias la="ls -A"
alias l="ls -CF"

# Project-specific aliases
alias luminis-dev="make dev"
alias luminis-test="make test"
alias luminis-build="make build"
alias luminis-clean="make clean"

# Docker aliases
alias dps="docker-compose ps"
alias dlog="docker-compose logs -f"
alias ddown="docker-compose down"
alias dup="docker-compose up -d"
```

### Makefile Targets
```makefile
# Available make targets
.PHONY: help install dev test build clean

help:           ## Show this help message
install:        ## Install all dependencies
dev:            ## Start development servers
test:           ## Run all tests
build:          ## Build for production
clean:          ## Clean temporary files
lint:           ## Run linting
format:         ## Format code
docker-up:      ## Start Docker services
docker-down:    ## Stop Docker services
health:         ## Check service health
```

## 🆘 Troubleshooting Commands

### Common Issues
```bash
# Fix permission issues
sudo chown -R $USER:$USER .

# Fix Node.js cache issues
cd src/frontend && rm -rf node_modules package-lock.json && npm install

# Fix Python cache issues
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Fix Docker issues
docker system prune -f
docker volume prune -f
docker network prune -f

# Reset to clean state
make clean && make install && make dev
```

### Diagnostic Commands
```bash
# Check system requirements
python scripts/check_requirements.py

# Check environment variables
python scripts/check_env.py

# Check port availability
python scripts/check_ports.py

# Check external dependencies
python scripts/check_dependencies.py
```

This comprehensive command reference provides all the tools needed to develop, test, deploy, and maintain the Luminis.AI Library Assistant project effectively.
