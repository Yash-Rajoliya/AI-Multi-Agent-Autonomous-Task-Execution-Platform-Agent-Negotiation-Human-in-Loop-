#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="setup.log"

log() {
  echo "[SETUP][$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  exit 1
}

check_command() {
  command -v "$1" >/dev/null 2>&1 || error_exit "$1 is not installed"
}

log "Starting environment setup..."

# Check dependencies
check_command python3
check_command pip
check_command docker
check_command docker-compose

log "Installing Python dependencies..."

pip install --upgrade pip
pip install poetry || error_exit "Failed to install poetry"

log "Installing project dependencies..."
poetry install || error_exit "Poetry install failed"

# Create .env if not exists
if [ ! -f ".env" ]; then
  log "Creating .env from template..."
  cp .env.example .env
fi

log "Starting infrastructure services..."
docker-compose -f deployments/docker/docker-compose.yml up -d

log "Waiting for services to be healthy..."
sleep 10

log "Setup completed successfully!"