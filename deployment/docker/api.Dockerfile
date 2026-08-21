FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["uvicorn", "apps.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]