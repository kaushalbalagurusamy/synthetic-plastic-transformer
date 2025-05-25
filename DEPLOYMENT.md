# Deployment Guide

This guide covers the complete deployment process for the Synthetic Plastic Transformer project using the CI/CD pipeline.

## Overview

The project uses a comprehensive CI/CD pipeline with the following components:

- **GitHub Actions** for automated testing and deployment
- **Docker** for containerization
- **Docker Compose** for multi-service orchestration
- **PostgreSQL** for data storage
- **Redis** for caching and task queues
- **Nginx** for reverse proxy and load balancing
- **Prometheus + Grafana** for monitoring

## Prerequisites

### Required Software

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git 2.30+
- Python 3.8+ (for local development)

### Required Accounts/Services

- GitHub account with repository access
- Docker Hub account (optional, for custom registry)
- Domain name and SSL certificates (for production)

## Environment Setup

### 1. Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/synthetic-plastic-transformer.git
cd synthetic-plastic-transformer

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Start development environment
docker-compose up -d

# Access services
# - API: http://localhost:8000
# - Jupyter Lab: http://localhost:8888
# - Flower (Celery): http://localhost:5555
# - Database: localhost:5432
```

### 2. Staging Environment

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Or with specific options
./scripts/deploy.sh staging --force-rebuild --skip-tests
```

### 3. Production Environment

```bash
# Deploy to production (recommended with tests)
./scripts/deploy.sh production

# Emergency deployment (skip tests, not recommended)
SKIP_TESTS=true ./scripts/deploy.sh production --force-rebuild
```

## CI/CD Pipeline Configuration

### GitHub Actions Secrets

Configure the following secrets in your GitHub repository:

#### Required Secrets

```
# PyPI Publishing
PYPI_API_TOKEN=pypi-your-token-here
TEST_PYPI_API_TOKEN=pypi-your-test-token-here

# Docker Registry (if using custom registry)
DOCKER_REGISTRY_USERNAME=your-username
DOCKER_REGISTRY_PASSWORD=your-password

# Production Deployment (if using remote deployment)
PRODUCTION_SSH_KEY=your-private-ssh-key
PRODUCTION_HOST=your-production-server
PRODUCTION_USER=deployment-user
```

#### Optional Secrets

```
# Slack/Discord notifications
SLACK_WEBHOOK_URL=your-slack-webhook
DISCORD_WEBHOOK_URL=your-discord-webhook

# External monitoring
SENTRY_DSN=your-sentry-dsn
DATADOG_API_KEY=your-datadog-key
```

### Workflow Triggers

The CI/CD pipeline is triggered by:

1. **Push to main/develop branches** → Runs CI tests
2. **Pull requests** → Runs CI tests and security checks
3. **Git tags (v*)** → Runs full CD pipeline with deployment
4. **Manual trigger** → Can run specific jobs manually

### Pipeline Stages

#### CI Pipeline (`.github/workflows/ci.yml`)

1. **Code Quality**
   - Black formatting check
   - Flake8 linting
   - isort import sorting
   - mypy type checking
   - Bandit security scanning

2. **Testing**
   - Unit tests (Python 3.8-3.11)
   - Integration tests
   - Cross-platform testing (Ubuntu, Windows, macOS)
   - Code coverage reporting

3. **Docker Build**
   - Multi-stage Docker image build
   - Security scanning with Trivy
   - Image size optimization

4. **Documentation**
   - Sphinx/MkDocs documentation build
   - Link checking
   - API documentation generation

#### CD Pipeline (`.github/workflows/cd.yml`)

1. **Pre-deployment Testing**
   - Run full test suite
   - Performance benchmarks
   - Security scans

2. **Build and Publish**
   - PyPI package publishing
   - Docker image publishing to GHCR
   - Documentation deployment

3. **Deployment**
   - Automated deployment to staging
   - Manual approval for production
   - Database migrations
   - Health checks

4. **Post-deployment**
   - Monitoring alerts
   - Performance validation
   - Rollback procedures

## Docker Configuration

### Multi-stage Dockerfile

The project uses a multi-stage Dockerfile with the following targets:

- `base`: System dependencies and Python setup
- `dependencies`: Python package installation
- `app`: Application code and basic setup
- `development`: Development tools and Jupyter
- `production`: Optimized for production deployment

### Build Targets

```bash
# Development build
docker build --target development -t spt:dev .

# Production build
docker build --target production -t spt:prod .

# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t spt:py311 .
```

### Environment Variables

Configure the following environment variables:

#### Required Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://host:port/db

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Environment
ENVIRONMENT=production  # development, staging, production
DEBUG=false
```

#### Optional Variables

```env
# External Services
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true

# Resource Limits
MAX_WORKERS=4
MEMORY_LIMIT=2G
REQUEST_TIMEOUT=30

# Feature Flags
ENABLE_QUANTUM_DESCRIPTORS=true
ENABLE_GPU_ACCELERATION=false
```

## Monitoring and Observability

### Prometheus Metrics

The application exposes metrics at `/metrics`:

- Request latency and throughput
- Database connection pool status
- Model prediction accuracy
- Resource utilization

### Grafana Dashboards

Pre-configured dashboards include:

- Application performance
- Infrastructure monitoring
- Business metrics (predictions, accuracy)
- Alert management

### Health Checks

Multiple health check endpoints:

- `/health` - Basic application health
- `/health/deep` - Database and Redis connectivity
- `/health/ready` - Readiness for traffic
- `/health/live` - Liveness probe

### Logging

Structured logging with:

- JSON format for production
- Correlation IDs for request tracing
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Centralized log aggregation with ELK stack

## Database Management

### Migrations

```bash
# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback migrations
docker-compose exec api alembic downgrade -1
```

### Backup and Restore

```bash
# Backup database
docker-compose exec db pg_dump -U postgres spt_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres spt_db < backup.sql

# Automated backup (production)
docker-compose exec db pg_dump -U postgres spt_db | gzip > "backup_$(date +%Y%m%d_%H%M%S).sql.gz"
```

## Security Considerations

### SSL/TLS Configuration

```nginx
# Nginx SSL configuration (nginx.conf)
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
```

### Secrets Management

- Use environment variables for secrets
- Encrypt secrets at rest
- Rotate secrets regularly
- Use dedicated secret management tools (HashiCorp Vault, AWS Secrets Manager)

### Network Security

- Use firewalls to restrict access
- Enable fail2ban for SSH protection
- Use VPN for administrative access
- Implement rate limiting

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Clear Docker cache
   docker system prune -af
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

2. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose exec db pg_isready -U postgres
   
   # View database logs
   docker-compose logs db
   ```

3. **Memory Issues**
   ```bash
   # Monitor resource usage
   docker stats
   
   # Adjust memory limits in docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 4G
   ```

### Log Analysis

```bash
# View application logs
docker-compose logs -f api

# View specific service logs
docker-compose logs worker

# Search logs
docker-compose logs api | grep ERROR
```

### Performance Debugging

```bash
# Profile API requests
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/predict"

# Monitor database queries
docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

## Maintenance

### Regular Tasks

1. **Daily**
   - Monitor application health
   - Check error logs
   - Verify backup completion

2. **Weekly**
   - Update dependencies
   - Review security alerts
   - Performance analysis

3. **Monthly**
   - Security patches
   - Capacity planning
   - Disaster recovery testing

### Update Procedures

```bash
# Update application
git pull origin main
./scripts/deploy.sh production

# Update dependencies
pip-compile requirements.in
docker-compose build --no-cache

# Update infrastructure
docker-compose pull
docker-compose up -d
```

## Rollback Procedures

### Application Rollback

```bash
# Rollback to previous version
git checkout previous-tag
./scripts/deploy.sh production --skip-tests

# Database rollback
docker-compose exec api alembic downgrade -1
```

### Infrastructure Rollback

```bash
# Rollback Docker images
docker-compose down
docker tag backup-image:latest current-image:latest
docker-compose up -d
```

## Contact and Support

For deployment issues or questions:

- Create an issue in the GitHub repository
- Contact the development team
- Check the troubleshooting documentation

## References

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/) 