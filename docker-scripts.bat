@echo off
REM Luminis.AI Library Assistant - Docker Management Scripts (Windows)
REM ================================================================

setlocal enabledelayedexpansion

REM Project name
set PROJECT_NAME=luminis-ai-library

REM Functions
:print_header
echo ================================
echo   Luminis.AI Library Assistant
echo   Docker Management Scripts
echo ================================
goto :eof

:print_success
echo ✅ %~1
goto :eof

:print_error
echo ❌ %~1
goto :eof

:print_warning
echo ⚠️  %~1
goto :eof

:print_info
echo ℹ️  %~1
goto :eof

REM Check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not running. Please start Docker and try again."
    exit /b 1
)
call :print_success "Docker is running"
goto :eof

REM Build all images
:build
call :print_header
call :print_info "Building Docker images..."

call :check_docker
if errorlevel 1 exit /b 1

REM Build backend
call :print_info "Building backend image..."
docker build -f docker/Dockerfile.backend -t %PROJECT_NAME%-backend .
if errorlevel 1 (
    call :print_error "Failed to build backend image"
    exit /b 1
)
call :print_success "Backend image built successfully"

REM Build frontend
call :print_info "Building frontend image..."
docker build -f docker/Dockerfile.frontend -t %PROJECT_NAME%-frontend .
if errorlevel 1 (
    call :print_error "Failed to build frontend image"
    exit /b 1
)
call :print_success "Frontend image built successfully"

call :print_success "All images built successfully!"
goto :eof

REM Start services
:start
call :print_header
call :print_info "Starting services..."

call :check_docker
if errorlevel 1 exit /b 1

docker-compose up -d
if errorlevel 1 (
    call :print_error "Failed to start services"
    exit /b 1
)

call :print_success "Services started successfully!"
call :print_info "Backend: http://localhost:8000"
call :print_info "Frontend: http://localhost:5173"
call :print_info "Nginx (if enabled): http://localhost:80"
goto :eof

REM Stop services
:stop
call :print_header
call :print_info "Stopping services..."

docker-compose down
call :print_success "Services stopped successfully!"
goto :eof

REM Restart services
:restart
call :print_header
call :print_info "Restarting services..."

call :stop
call :start
goto :eof

REM Show logs
:logs
call :print_header
call :print_info "Showing logs..."

if "%2"=="" (
    docker-compose logs -f
) else (
    docker-compose logs -f %2
)
goto :eof

REM Show status
:status
call :print_header
call :print_info "Service status:"

docker-compose ps
goto :eof

REM Clean up
:clean
call :print_header
call :print_warning "Cleaning up Docker resources..."

docker-compose down -v
docker rmi %PROJECT_NAME%-backend %PROJECT_NAME%-frontend 2>nul
docker volume prune -f

call :print_success "Cleanup completed!"
goto :eof

REM Development mode
:dev
call :print_header
call :print_info "Starting development mode..."

call :check_docker
if errorlevel 1 exit /b 1

docker-compose up -d backend frontend
if errorlevel 1 (
    call :print_error "Failed to start development services"
    exit /b 1
)

call :print_success "Development services started!"
call :print_info "Backend: http://localhost:8000"
call :print_info "Frontend: http://localhost:5173"
goto :eof

REM Production mode
:prod
call :print_header
call :print_info "Starting production mode..."

call :check_docker
if errorlevel 1 exit /b 1

docker-compose --profile production up -d
if errorlevel 1 (
    call :print_error "Failed to start production services"
    exit /b 1
)

call :print_success "Production services started!"
call :print_info "Application: http://localhost:80"
goto :eof

REM Health check
:health
call :print_header
call :print_info "Checking service health..."

REM Check backend
curl -f http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    call :print_error "Backend is not responding"
) else (
    call :print_success "Backend is healthy"
)

REM Check frontend
curl -f http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    call :print_error "Frontend is not responding"
) else (
    call :print_success "Frontend is healthy"
)

REM Check nginx (if running)
curl -f http://localhost:80/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Nginx is not running or not responding"
) else (
    call :print_success "Nginx is healthy"
)
goto :eof

REM Show help
:help
call :print_header
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   build     Build all Docker images
echo   start     Start all services
echo   stop      Stop all services
echo   restart   Restart all services
echo   logs      Show logs (optionally specify service name)
echo   status    Show service status
echo   clean     Clean up Docker resources
echo   dev       Start development mode (backend + frontend)
echo   prod      Start production mode (all services + nginx)
echo   health    Check service health
echo   help      Show this help message
echo.
echo Examples:
echo   %0 build
echo   %0 start
echo   %0 logs backend
echo   %0 dev
goto :eof

REM Main script logic
if "%1"=="build" goto build
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="status" goto status
if "%1"=="clean" goto clean
if "%1"=="dev" goto dev
if "%1"=="prod" goto prod
if "%1"=="health" goto health
if "%1"=="help" goto help
if "%1"=="--help" goto help
if "%1"=="-h" goto help
if "%1"=="" goto help

call :print_error "Unknown command: %1"
goto help
