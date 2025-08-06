# FROM python:3.12.3-slim
#
# # Set env vars to avoid Python buffer issues & venv issues
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
# # Install curl and pip dependencies
# RUN apt-get update \
#     && apt-get install -y curl build-essential libpq-dev \
#     && apt-get clean
#
# # Install Poetry
# ENV POETRY_VERSION=2.1.3
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:$PATH"
#
# # Set working dir
# WORKDIR /app
#
# # Copy Poetry files first
# COPY pyproject.toml poetry.lock README.md ./
#
# # Install deps
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi
#
# # Copy rest of the app
# COPY . .
#
# # Set Flask run command
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


# Use official slim Python 3.12 image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy dependency files first
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies (don't install app itself yet)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the project
COPY . .

# (Optional) Install the project itself if needed
# RUN poetry install --only main

# Set default command
CMD ["poetry", "run", "python", "run.py"]
# # Expose the port the app runs on
# EXPOSE 5000