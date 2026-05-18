#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="logs/worker.log"
WORKER_CONCURRENCY=4

mkdir -p logs

log() {
  echo "[WORKER][$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  exit 1
}

check_env() {
  [ -f ".env" ] || error_exit ".env file missing"
}

check_redis() {
  nc -z localhost 6379 || error_exit "Redis is not running"
}

log "Starting Worker Service..."

check_env
check_redis

log "Launching worker with concurrency=$WORKER_CONCURRENCY"

python apps/worker-service/worker.py \
  --concurrency "$WORKER_CONCURRENCY" \
  --log-level INFO | tee -a "$LOG_FILE"

log "Worker started successfully"