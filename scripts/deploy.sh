#!/bin/bash

# Synthetic Plastic Transformer Deployment Script
# Usage: ./scripts/deploy.sh [environment] [options]

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Default values
ENVIRONMENT="${1:-development}"
SKIP_TESTS="${SKIP_TESTS:-false}"
FORCE_REBUILD="${FORCE_REBUILD:-false}"
BACKUP_DATA="${BACKUP_DATA:-true}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print usage
usage() {
    cat << EOF
Usage: $0 [environment] [options]

Environments:
  development  - Deploy to development environment (default)
  staging      - Deploy to staging environment
  production   - Deploy to production environment

Options:
  --skip-tests     Skip running tests before deployment
  --force-rebuild  Force rebuild of Docker images
  --no-backup      Skip data backup (not recommended for production)
  --help          Show this help message

Examples:
  $0 development
  $0 production --skip-tests --force-rebuild
  $0 staging --no-backup

Environment Variables:
  SKIP_TESTS       Skip tests (true/false)
  FORCE_REBUILD    Force rebuild (true/false)
  BACKUP_DATA      Backup data (true/false)
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --force-rebuild)
            FORCE_REBUILD=true
            shift
            ;;
        --no-backup)
            BACKUP_DATA=false
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        development|staging|production)
            ENVIRONMENT=$1
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    log_error "Invalid environment: $ENVIRONMENT"
    usage
    exit 1
fi

log_info "Deploying to $ENVIRONMENT environment"

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Run tests
run_tests() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        log_warning "Skipping tests"
        return 0
    fi
    
    log_info "Running tests..."
    
    # Install test dependencies
    python -m pip install --upgrade pip
    pip install pytest pytest-cov pytest-asyncio
    
    # Run unit tests
    if ! pytest tests/unit/ -v --tb=short; then
        log_error "Unit tests failed"
        exit 1
    fi
    
    # Run integration tests for non-production environments
    if [[ "$ENVIRONMENT" != "production" ]]; then
        if ! pytest tests/integration/ -v --tb=short; then
            log_error "Integration tests failed"
            exit 1
        fi
    fi
    
    log_success "All tests passed"
}

# Backup data
backup_data() {
    if [[ "$BACKUP_DATA" == "false" ]]; then
        log_warning "Skipping data backup"
        return 0
    fi
    
    log_info "Creating data backup..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    if docker-compose ps db | grep -q "Up"; then
        log_info "Backing up database..."
        docker-compose exec -T db pg_dump -U postgres spt_db > "$BACKUP_DIR/database.sql"
    fi
    
    # Backup Redis data
    if docker-compose ps redis | grep -q "Up"; then
        log_info "Backing up Redis data..."
        docker-compose exec -T redis redis-cli --rdb - > "$BACKUP_DIR/redis.rdb"
    fi
    
    # Backup models and data directories
    if [[ -d "models" ]]; then
        cp -r models "$BACKUP_DIR/"
    fi
    
    if [[ -d "data/processed" ]]; then
        cp -r data/processed "$BACKUP_DIR/"
    fi
    
    log_success "Backup created: $BACKUP_DIR"
}

# Build and deploy
deploy() {
    log_info "Starting deployment..."
    
    # Set environment-specific variables
    case $ENVIRONMENT in
        development)
            COMPOSE_FILE="docker-compose.yml"
            COMPOSE_OVERRIDE=""
            ;;
        staging)
            COMPOSE_FILE="docker-compose.yml"
            COMPOSE_OVERRIDE="-f docker-compose.staging.yml"
            ;;
        production)
            COMPOSE_FILE="docker-compose.yml"
            COMPOSE_OVERRIDE="-f docker-compose.production.yml"
            ;;
    esac
    
    # Pull latest images or force rebuild
    if [[ "$FORCE_REBUILD" == "true" ]]; then
        log_info "Force rebuilding images..."
        docker-compose -f $COMPOSE_FILE $COMPOSE_OVERRIDE build --no-cache
    else
        log_info "Building images..."
        docker-compose -f $COMPOSE_FILE $COMPOSE_OVERRIDE build
    fi
    
    # Stop existing containers gracefully
    log_info "Stopping existing containers..."
    docker-compose -f $COMPOSE_FILE $COMPOSE_OVERRIDE down --timeout 60
    
    # Start services
    log_info "Starting services..."
    docker-compose -f $COMPOSE_FILE $COMPOSE_OVERRIDE up -d
    
    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 10
    
    # Run database migrations if needed
    if [[ "$ENVIRONMENT" != "development" ]]; then
        log_info "Running database migrations..."
        docker-compose -f $COMPOSE_FILE $COMPOSE_OVERRIDE exec -T api python -m alembic upgrade head
    fi
    
    # Health check
    health_check
    
    log_success "Deployment completed successfully!"
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:8080/health &> /dev/null; then
            log_success "API health check passed"
            break
        fi
        
        if [[ $attempt -eq $max_attempts ]]; then
            log_error "Health check failed after $max_attempts attempts"
            docker-compose logs api
            exit 1
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 5
        ((attempt++))
    done
    
    # Check database connection
    if docker-compose exec -T db pg_isready -U postgres &> /dev/null; then
        log_success "Database health check passed"
    else
        log_error "Database health check failed"
        exit 1
    fi
    
    # Check Redis connection
    if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
        log_success "Redis health check passed"
    else
        log_error "Redis health check failed"
        exit 1
    fi
}

# Cleanup old images and containers
cleanup() {
    log_info "Cleaning up old Docker resources..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes (be careful in production)
    if [[ "$ENVIRONMENT" == "development" ]]; then
        docker volume prune -f
    fi
    
    log_success "Cleanup completed"
}

# Post deployment tasks
post_deploy() {
    log_info "Running post-deployment tasks..."
    
    # Update documentation
    if [[ "$ENVIRONMENT" == "production" ]]; then
        log_info "Building and deploying documentation..."
        docker-compose exec -T api mkdocs build
    fi
    
    # Send notification (implement as needed)
    # send_notification "Deployment to $ENVIRONMENT completed successfully"
    
    log_success "Post-deployment tasks completed"
}

# Error handling
trap 'log_error "Deployment failed!"; exit 1' ERR

# Main execution
main() {
    log_info "Starting deployment process for $ENVIRONMENT environment"
    log_info "Configuration: SKIP_TESTS=$SKIP_TESTS, FORCE_REBUILD=$FORCE_REBUILD, BACKUP_DATA=$BACKUP_DATA"
    
    check_prerequisites
    run_tests
    backup_data
    deploy
    cleanup
    post_deploy
    
    log_success "🎉 Deployment to $ENVIRONMENT completed successfully!"
    log_info "Application is running at: http://localhost:8080"
    
    if [[ "$ENVIRONMENT" == "development" ]]; then
        log_info "Jupyter Lab is available at: http://localhost:8888"
        log_info "Flower (Celery monitoring) is available at: http://localhost:5555"
    fi
}

# Run main function
main "$@" 