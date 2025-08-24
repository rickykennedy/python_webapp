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
DOCKER_COMPOSE = docker compose
DOCKER = docker

# Install dependencies using Poetry
init-env:
	source venv/bin/activate

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

docker-start:
	$(DOCKER) start my-webapp-container

docker-run:
	$(DOCKER) run -d -p 5000:5000 --name my-webapp-container python-webapp

docker-run-dev:
	#$(DOCKER) run --env-file .env python-webapp
	$(DOCKER) run -d -p 5000:5000 --name my-webapp-container --env-file .env python-webapp
	#$(DOCKER) run -d -p 5000:5000 --name my-webapp-container --env-file .env --network="host" python-webapp

docker-run-env:
	$(DOCKER) run -d  -p 5000:5000 --name my-webapp-container -e DATABASE_URL="postgresql+psycopg2://postgres:floricky@192.168.0.220:5432/postgres" python-webapp

docker-stop:
	$(DOCKER) stop my-webapp-container

docker-drop:
	$(DOCKER) stop my-webapp-container && $(DOCKER) rm my-webapp-container

docker-logs:
	$(DOCKER) logs -f my-webapp-container

docker-db-inspect:
	$(DOCKER) exec -it my-webapp-container sh -c 'nc -z db 5432 && echo "Database is up" || echo "Database is down"'
	#$(DOCKER) exec -it my-webapp-container env | grep DATABASE

docker-db-check:
	$(DOCKER) exec -it my-webapp-container sh

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
