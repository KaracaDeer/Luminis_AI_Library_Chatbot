# Luminis.AI Library Assistant - Makefile

.PHONY: help install dev build test clean lint format docker-build docker-run

# Default target
help:
	@echo "🌟 Luminis.AI Library Assistant - Available Commands:"
	@echo ""
	@echo "  📦 Setup & Installation:"
	@echo "    make install     - Install all dependencies"
	@echo "    make clean       - Clean build artifacts and cache"
	@echo ""
	@echo "  🚀 Development:"
	@echo "    make dev         - Start development server (backend + frontend)"
	@echo "    make backend     - Start only backend server"
	@echo "    make frontend    - Start only frontend server"
	@echo ""
	@echo "  🏗️  Build & Production:"
	@echo "    make build       - Build frontend for production"
	@echo "    make start       - Start production server"
	@echo ""
	@echo "  🧪 Testing & Quality:"
	@echo "    make test        - Run all tests"
	@echo "    make test-backend - Run backend tests"
	@echo "    make test-frontend - Run frontend tests"
	@echo "    make lint        - Run linters"
	@echo "    make format      - Format code"
	@echo ""
	@echo "  🐳 Docker:"
	@echo "    make docker-build - Build Docker images"
	@echo "    make docker-run   - Run with Docker"
	@echo ""
	@echo "  💾 Database:"
	@echo "    make db-init     - Initialize database"
	@echo "    make db-reset    - Reset database"
	@echo ""

# Installation
install:
	@echo "📦 Installing dependencies..."
	npm install
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Development
dev:
	@echo "🚀 Starting development servers..."
	npm run dev

backend:
	@echo "🔧 Starting backend server..."
	npm run server

frontend:
	@echo "⚛️  Starting frontend server..."
	npm run client

# Build
build:
	@echo "🏗️  Building for production..."
	npm run build

start:
	@echo "🚀 Starting production server..."
	npm run start

# Testing
test:
	@echo "🧪 Running all tests..."
	npm run test

test-backend:
	@echo "🧪 Running backend tests..."
	python -m pytest tests/ -v

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd src/frontend && npm test

# Code Quality
lint:
	@echo "🔍 Running linters..."
	cd src/frontend && npx eslint . --ext .ts,.tsx
	flake8 src/backend --max-line-length=100

format:
	@echo "✨ Formatting code..."
	cd src/frontend && npx prettier --write .
	black src/backend
	isort src/backend

# Database
db-init:
	@echo "💾 Initializing database..."
	npm run db:init

db-reset:
	@echo "💾 Resetting database..."
	npm run db:reset

# Docker
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose -f docker/docker-compose.yml build

docker-run:
	@echo "🐳 Running with Docker..."
	docker-compose -f docker/docker-compose.yml up -d

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose -f docker/docker-compose.yml down

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	rm -rf node_modules
	rm -rf src/frontend/node_modules
	rm -rf src/frontend/dist
	rm -rf src/frontend/build
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.d.ts" -delete
	find . -type f -name "*.js.map" -delete
	@echo "✅ Cleanup completed!"

# Development helpers
setup-dev: install db-init
	@echo "🎉 Development environment ready!"

quick-start: install dev

# Production helpers
deploy-prep: clean install build test
	@echo "🚀 Ready for deployment!"
