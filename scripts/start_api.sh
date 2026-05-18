#!/usr/bin/env bash

set -euo pipefail

SERVICE="api-gateway"
PORT=8000
LOG_FILE="logs/api.log"

mkdir -p logs

log() {
  echo "[API][$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  exit 1
}

check_env() {
  if [ ! -f ".env" ]; then
    error_exit ".env file not found. Run setup.sh first."
  fi
}

check_port() {
  if lsof -i :"$PORT" >/dev/null 2>&1; then
    error_exit "Port $PORT is already in use"
  fi
}

log "Starting API Gateway..."

check_env
check_port

log "Launching FastAPI server..."

uvicorn apps.api-gateway.main:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --workers 4 \
  --log-level info \
  --reload | tee -a "$LOG_FILE"

log "API Gateway started successfully"