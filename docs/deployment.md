# Deployment Guide

## 🚀 Deployment Overview

This guide provides comprehensive instructions for deploying the Luminis.AI Library Assistant in various environments, from local development to production.

## 🏗️ Deployment Architecture

### Production Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Application   │    │   Database      │
│   (Nginx)       │◄──►│   Servers       │◄──►│   (SQLite/      │
│                 │    │   (FastAPI)     │    │    PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN           │    │   Vector DB     │    │   File Storage  │
│   (Static       │    │   (ChromaDB)    │    │   (Audio/       │
│   Assets)       │    │                 │    │    Images)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🐳 Docker Deployment

### Docker Configuration

#### Dockerfile
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/backend/ .
COPY src/services/ ./services/

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

#### Frontend Dockerfile
```dockerfile
# Frontend Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY src/frontend/package*.json ./
RUN npm ci --only=production

# Copy source code and build
COPY src/frontend/ .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/backend.Dockerfile
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./luminis_library.db
      - CHROMA_PERSIST_DIRECTORY=/app/chroma_db
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    depends_on:
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: docker/frontend.Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  redis_data:
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Deployment
```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1d0 \
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-groups luminis-sg \
    --user-data file://user-data.sh
```

#### ECS Deployment
```yaml
# task-definition.json
{
  "family": "luminis-ai-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "luminis-backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/luminis-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "${OPENAI_API_KEY}"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/luminis-ai",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Cloud Run Deployment
```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: luminis-ai-backend
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containers:
      - image: gcr.io/PROJECT_ID/luminis-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-api-key
              key: api-key
        resources:
          limits:
            cpu: 1000m
            memory: 2Gi
```

#### Cloud SQL Integration
```python
# database.py for Cloud SQL
import os
from sqlalchemy import create_engine

def get_cloud_sql_connection():
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    
    return create_engine(
        f"postgresql://{db_user}:{db_pass}@/{db_name}"
        f"?host=/cloudsql/{cloud_sql_connection_name}"
    )
```

### Azure Deployment

#### Container Instances
```yaml
# azure-container-instance.yaml
apiVersion: 2021-09-01
location: eastus
name: luminis-ai-container
properties:
  containers:
  - name: luminis-backend
    properties:
      image: your-registry.azurecr.io/luminis-backend:latest
      ports:
      - port: 5000
      environmentVariables:
      - name: OPENAI_API_KEY
        secureValue: your-openai-api-key
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 5000
```

## 🔧 Environment Configuration

### Environment Variables

#### Production Environment
```bash
# .env.production
NODE_ENV=production
DEBUG=false

# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
API_RATE_LIMIT=1000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/luminis_prod
CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db

# Security
JWT_SECRET_KEY=your_very_strong_jwt_secret_key_here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=INFO

# Redis
REDIS_URL=redis://localhost:6379/0

# File Storage
UPLOAD_MAX_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=mp3,wav,m4a
```

#### Development Environment
```bash
# .env.development
NODE_ENV=development
DEBUG=true

# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
API_RATE_LIMIT=100

# Database
DATABASE_URL=sqlite:///./luminis_library.db
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Security (Use weaker keys for development)
JWT_SECRET_KEY=dev_secret_key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Monitoring
LOG_LEVEL=DEBUG
```

### Nginx Configuration

#### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name luminis-ai.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name luminis-ai.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # Security Headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API Routes
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend Routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static Files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## 📊 Monitoring and Logging

### Application Monitoring

#### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'luminis-ai-backend'
    static_configs:
      - targets: ['backend:5000']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'luminis-ai-frontend'
    static_configs:
      - targets: ['frontend:80']
    metrics_path: /metrics
```

#### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Luminis.AI Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### Logging Configuration

#### Structured Logging
```python
# logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔒 Security Deployment

### SSL/TLS Configuration

#### Let's Encrypt Setup
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d luminis-ai.com -d www.luminis-ai.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Security Headers
```python
# security_headers.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["luminis-ai.com", "*.luminis-ai.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://luminis-ai.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🚀 Deployment Scripts

### Automated Deployment

#### deploy.sh
```bash
#!/bin/bash
set -e

# Configuration
ENVIRONMENT=${1:-production}
DOCKER_REGISTRY="your-registry.com"
APP_NAME="luminis-ai"

echo "Deploying $APP_NAME to $ENVIRONMENT..."

# Build and push Docker images
docker build -t $DOCKER_REGISTRY/$APP_NAME-backend:latest -f docker/backend.Dockerfile .
docker build -t $DOCKER_REGISTRY/$APP_NAME-frontend:latest -f docker/frontend.Dockerfile .

docker push $DOCKER_REGISTRY/$APP_NAME-backend:latest
docker push $DOCKER_REGISTRY/$APP_NAME-frontend:latest

# Deploy to production
if [ "$ENVIRONMENT" = "production" ]; then
    # Update production deployment
    kubectl set image deployment/luminis-ai-backend backend=$DOCKER_REGISTRY/$APP_NAME-backend:latest
    kubectl set image deployment/luminis-ai-frontend frontend=$DOCKER_REGISTRY/$APP_NAME-frontend:latest
    
    # Wait for rollout
    kubectl rollout status deployment/luminis-ai-backend
    kubectl rollout status deployment/luminis-ai-frontend
    
    echo "Deployment completed successfully!"
fi
```

#### health_check.sh
```bash
#!/bin/bash

# Health check script
HEALTH_URL="https://luminis-ai.com/api/health"
MAX_ATTEMPTS=30
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Health check attempt $ATTEMPT/$MAX_ATTEMPTS"
    
    if curl -f -s $HEALTH_URL > /dev/null; then
        echo "Health check passed!"
        exit 0
    fi
    
    echo "Health check failed, waiting 10 seconds..."
    sleep 10
    ATTEMPT=$((ATTEMPT + 1))
done

echo "Health check failed after $MAX_ATTEMPTS attempts"
exit 1
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] All tests pass
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Performance tests passed
- [ ] Database migrations ready
- [ ] Environment variables configured
- [ ] SSL certificates valid
- [ ] Backup strategy in place

### Deployment
- [ ] Deploy to staging environment
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Verify health endpoints
- [ ] Check monitoring dashboards
- [ ] Test critical user journeys
- [ ] Verify SSL certificates
- [ ] Check error rates

### Post-deployment
- [ ] Monitor application metrics
- [ ] Check error logs
- [ ] Verify user feedback
- [ ] Performance monitoring
- [ ] Security monitoring
- [ ] Backup verification
- [ ] Documentation updates

## 🔄 Rollback Procedures

### Quick Rollback
```bash
# Kubernetes rollback
kubectl rollout undo deployment/luminis-ai-backend
kubectl rollout undo deployment/luminis-ai-frontend

# Docker Compose rollback
docker-compose down
docker-compose up -d --scale backend=0
docker-compose up -d backend:previous-version
```

### Database Rollback
```bash
# Database rollback script
python scripts/rollback_database.py --version previous-stable
```

This comprehensive deployment guide ensures reliable, secure, and scalable deployment of the Luminis.AI Library Assistant across various environments.
