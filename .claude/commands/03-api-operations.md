# API Operations Commands

## Starting the API

### Development Server
```bash
# Start API server with hot reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Start with specific environment
ENVIRONMENT=development uvicorn src.api.main:app --reload

# Start with custom config
uvicorn src.api.main:app --reload --env-file .env.development
```

### Production Server
```bash
# Run API with Gunicorn (production)
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Run with specific bind and workers
gunicorn src.api.main:app \
  -w 8 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log

# Run with systemd
sudo systemctl start spt-api
sudo systemctl status spt-api
```

## Testing API Endpoints

### Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Check with details
curl http://localhost:8000/health/detailed
```

### Authentication Testing
```bash
# Get access token
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "test@example.com", "password": "password"}'

# Test authenticated endpoint
TOKEN="your-jwt-token"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/user/profile
```

### Prediction Endpoints
```bash
# Test prediction endpoint
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "target_properties": {
      "tensile_strength": 500.0,
      "elastic_modulus": 10.0
    },
    "constraints": {
      "require_organic": true
    }
  }'

# Batch prediction
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@polymers.csv" \
  -F "max_results=10"
```

## API Testing with pytest

### Run API Tests
```bash
# Test API endpoints
pytest tests/api/ -v --asyncio-mode=auto

# Test specific endpoint
pytest tests/api/test_predictions.py::test_predict_endpoint -v

# Test with coverage
pytest tests/api/ --cov=src.api --cov-report=html
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/test_api_integration.py -v

# Run with real database
TEST_DB=postgresql://user:pass@localhost/test_db \
  pytest tests/integration/ -v
```

## API Documentation

### Generate OpenAPI Schema
```bash
# Export OpenAPI schema
python -m src.api.export_schema > openapi.json

# Generate with specific version
python -m src.api.export_schema \
  --version 1.0.0 \
  --title "Synthetic Plastic Transformer API" \
  > docs/openapi.json
```

### Serve Documentation
```bash
# Access interactive docs
open http://localhost:8000/docs

# Access ReDoc
open http://localhost:8000/redoc

# Generate static docs
python -m src.api.generate_static_docs \
  --output docs/api/
```

## Performance Testing

### Load Testing
```bash
# Run load test with locust
locust -f tests/load/locustfile.py \
  --host http://localhost:8000 \
  --users 100 \
  --spawn-rate 10

# Run with specific scenario
locust -f tests/load/prediction_load.py \
  --host http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 5m
```

### Benchmark Endpoints
```bash
# Benchmark with Apache Bench
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/predict

# Benchmark with wrk
wrk -t4 -c100 -d30s \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/health
```

## API Monitoring

### Prometheus Metrics
```bash
# Access metrics endpoint
curl http://localhost:8000/metrics

# Query specific metrics
curl http://localhost:8000/metrics | grep http_requests_total
```

### Logging
```bash
# View API logs
tail -f logs/api.log

# View error logs only
tail -f logs/error.log | grep ERROR

# Search logs
grep "prediction_id" logs/api.log | tail -20
```

## API Management

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add prediction history table"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Cache Management
```bash
# Clear Redis cache
redis-cli FLUSHDB

# View cache statistics
python -m src.api.cache_stats

# Warm up cache
python -m src.api.cache_warmup \
  --endpoints predict fiber_properties
```

### Rate Limiting
```bash
# Check rate limit status
curl -I http://localhost:8000/api/v1/predict \
  -H "Authorization: Bearer $TOKEN"

# View rate limit headers
curl -v http://localhost:8000/api/v1/health 2>&1 | \
  grep -i "x-ratelimit"
```

## Deployment

### Docker Deployment
```bash
# Build API image
docker build -t spt-api:latest -f Dockerfile --target production .

# Run API container
docker run -d \
  --name spt-api \
  -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  -e REDIS_URL=$REDIS_URL \
  spt-api:latest

# View container logs
docker logs -f spt-api
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/api-deployment.yaml

# Scale API pods
kubectl scale deployment spt-api --replicas=5

# Check pod status
kubectl get pods -l app=spt-api
```

## Maintenance

### API Health Monitoring
```bash
# Run health check script
python -m src.api.health_monitor \
  --interval 60 \
  --alert-webhook $SLACK_WEBHOOK

# Check all endpoints
python -m src.api.smoke_test \
  --base-url http://localhost:8000 \
  --token $TEST_TOKEN
```

### Backup and Restore
```bash
# Backup API configuration
python -m src.api.backup_config \
  --output backups/api_config_$(date +%Y%m%d).json

# Restore configuration
python -m src.api.restore_config \
  --input backups/api_config_20240115.json
```