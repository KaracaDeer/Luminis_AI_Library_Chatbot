#!/bin/bash

# Luminis.AI Library Assistant - Docker Management Scripts
# =======================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME="luminis-ai-library"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Luminis.AI Library Assistant${NC}"
    echo -e "${BLUE}  Docker Management Scripts${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Build all images
build() {
    print_header
    print_info "Building Docker images..."
    
    check_docker
    
    # Build backend
    print_info "Building backend image..."
    docker build -f docker/Dockerfile.backend -t ${PROJECT_NAME}-backend .
    print_success "Backend image built successfully"
    
    # Build frontend
    print_info "Building frontend image..."
    docker build -f docker/Dockerfile.frontend -t ${PROJECT_NAME}-frontend .
    print_success "Frontend image built successfully"
    
    print_success "All images built successfully!"
}

# Start services
start() {
    print_header
    print_info "Starting services..."
    
    check_docker
    
    # Start with docker-compose
    docker-compose up -d
    
    print_success "Services started successfully!"
    print_info "Backend: http://localhost:8000"
    print_info "Frontend: http://localhost:5173"
    print_info "Nginx (if enabled): http://localhost:80"
}

# Stop services
stop() {
    print_header
    print_info "Stopping services..."
    
    docker-compose down
    
    print_success "Services stopped successfully!"
}

# Restart services
restart() {
    print_header
    print_info "Restarting services..."
    
    stop
    start
}

# Show logs
logs() {
    print_header
    print_info "Showing logs..."
    
    if [ -n "$1" ]; then
        docker-compose logs -f "$1"
    else
        docker-compose logs -f
    fi
}

# Show status
status() {
    print_header
    print_info "Service status:"
    
    docker-compose ps
}

# Clean up
clean() {
    print_header
    print_warning "Cleaning up Docker resources..."
    
    # Stop and remove containers
    docker-compose down -v
    
    # Remove images
    docker rmi ${PROJECT_NAME}-backend ${PROJECT_NAME}-frontend 2>/dev/null || true
    
    # Remove unused volumes
    docker volume prune -f
    
    print_success "Cleanup completed!"
}

# Development mode
dev() {
    print_header
    print_info "Starting development mode..."
    
    check_docker
    
    # Start only backend and frontend (no nginx)
    docker-compose up -d backend frontend
    
    print_success "Development services started!"
    print_info "Backend: http://localhost:8000"
    print_info "Frontend: http://localhost:5173"
}

# Production mode
prod() {
    print_header
    print_info "Starting production mode..."
    
    check_docker
    
    # Start all services including nginx
    docker-compose --profile production up -d
    
    print_success "Production services started!"
    print_info "Application: http://localhost:80"
}

# Health check
health() {
    print_header
    print_info "Checking service health..."
    
    # Check backend
    if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend is not responding"
    fi
    
    # Check frontend
    if curl -f http://localhost:5173 > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend is not responding"
    fi
    
    # Check nginx (if running)
    if curl -f http://localhost:80/health > /dev/null 2>&1; then
        print_success "Nginx is healthy"
    else
        print_warning "Nginx is not running or not responding"
    fi
}

# Show help
help() {
    print_header
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build all Docker images"
    echo "  start     Start all services"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  logs      Show logs (optionally specify service name)"
    echo "  status    Show service status"
    echo "  clean     Clean up Docker resources"
    echo "  dev       Start development mode (backend + frontend)"
    echo "  prod      Start production mode (all services + nginx)"
    echo "  health    Check service health"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 start"
    echo "  $0 logs backend"
    echo "  $0 dev"
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "$2"
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    dev)
        dev
        ;;
    prod)
        prod
        ;;
    health)
        health
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "Unknown command: $1"
        help
        exit 1
        ;;
esac
