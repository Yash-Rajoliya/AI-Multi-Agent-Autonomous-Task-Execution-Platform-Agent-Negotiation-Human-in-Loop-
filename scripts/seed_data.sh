#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="logs/seed.log"

mkdir -p logs

log() {
  echo "[SEED][$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  exit 1
}

check_api() {
  curl -s http://localhost:8000/health >/dev/null || error_exit "API not running"
}

log "Seeding initial data..."

check_api

log "Creating default tenant..."
curl -X POST http://localhost:8000/v1/tenants \
  -H "Content-Type: application/json" \
  -d '{"name": "default", "plan": "enterprise"}'

log "Registering default agents..."
curl -X POST http://localhost:8000/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "planner", "type": "planner"}'

curl -X POST http://localhost:8000/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "executor", "type": "executor"}'

log "Creating sample workflow..."
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"name": "sample-workflow", "steps": []}'

log "Data seeding completed successfully!"