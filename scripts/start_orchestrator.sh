#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="logs/orchestrator.log"

mkdir -p logs

log() {
  echo "[ORCHESTRATOR][$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  exit 1
}

check_env() {
  [ -f ".env" ] || error_exit ".env file missing"
}

check_dependencies() {
  nc -z localhost 6379 || error_exit "Redis not running"
}

log "Starting Orchestrator Service..."

check_env
check_dependencies

log "Launching orchestration engine..."

python apps/orchestrator-service/main.py | tee -a "$LOG_FILE"

log "Orchestrator started successfully"