FROM python:3.12.3-slim

# Set env vars to avoid Python buffer issues & venv issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl and pip dependencies
RUN apt-get update \
    && apt-get install -y curl build-essential libpq-dev \
    && apt-get clean

# Install Poetry
ENV POETRY_VERSION=2.1.3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working dir
WORKDIR /app

# Copy Poetry files first
COPY pyproject.toml poetry.lock README.md ./

# Install deps
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy rest of the app
COPY . .

# Set Flask run command
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
