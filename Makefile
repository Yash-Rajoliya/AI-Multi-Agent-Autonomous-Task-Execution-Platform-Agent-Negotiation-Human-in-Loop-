.PHONY: help setup run-api run-worker run-orchestrator test lint format clean

help:
	@echo "Available commands:"
	@echo "  setup              Install dependencies & setup env"
	@echo "  run-api            Start API Gateway"
	@echo "  run-worker         Start Worker Service"
	@echo "  run-orchestrator   Start Orchestrator Service"
	@echo "  test               Run all tests"
	@echo "  lint               Run lint checks"
	@echo "  format             Format code"
	@echo "  clean              Cleanup cache files"

setup:
	@echo "Setting up project..."
	poetry install
	cp -n .env.example .env || true

run-api:
	bash scripts/start_api.sh

run-worker:
	bash scripts/start_worker.sh

run-orchestrator:
	bash scripts/start_orchestrator.sh

test:
	pytest -v --cov=.

lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy .
	bandit -r .

format:
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete