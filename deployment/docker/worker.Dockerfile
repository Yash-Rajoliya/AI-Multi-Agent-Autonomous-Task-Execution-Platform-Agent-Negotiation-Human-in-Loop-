FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["python", "-m", "apps.worker_service.worker"]