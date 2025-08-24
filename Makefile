# .PHONY: install run dev test export-req
#
# install:
# 	poetry install
#
# run:
#     poetry run python app.py
# # 	poetry run flask run --host=0.0.0.0 --port=5000
# dev:
# 	poetry shell
#
# test:
# 	poetry run pytest
#
# export-req:
# 	poetry export --without-hashes -f requirements.txt -o requirements.txt   # spaces instead of tab


# Variables
PYTHON = python3
POETRY = poetry
DOCKER_COMPOSE = docker-compose
DOCKER = docker

# Install dependencies using Poetry
install:
	$(POETRY) install

# Run the app locally
run:
	$(POETRY) run $(PYTHON) run.py

# Format code using Black
format:
	$(POETRY) run black .

# Run tests
test:
	$(POETRY) run pytest

# Docker commands
docker-build:
	$(DOCKER) build -t python-webapp .
# docker-build:
#     docker build -t python-webapp .
# docker-build:
#     docker build -t python-webapp .
#
# docker-run:
#     docker run -d -p 5000--name my-webapp-container python-webapp
#
# docker-run-dev:
#     docker run --env-file .env python-webapp
#
docker-drop:
	docker stop my-webapp-container && docker rm my-webapp-container
# Build Docker image
docker-compose-build:
	$(DOCKER_COMPOSE) build

# Start services using Docker Compose
docker-compose-up:
	$(DOCKER_COMPOSE) up -d

# Stop services
docker-compose-down:
	$(DOCKER_COMPOSE) down

# Clean up caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
