System Dependencies using poetry
# Python Web Application
This is a Python web application that uses Flask as the web framework. It includes user authentication,
quote management, and contact message functionality. The application is designed to be run in a Docker container
and can be easily set up using Docker Compose.

To access the venv
```source venv/bin/activate```

Using docker
```sudo systemctl status docker```
```sudo systemctl start docker```
```sudo systemctl enable docker```

```docker compose up --build```


How to run the application directly via Python
```python3 run.py```

Running the Application via poetry
```poetry run python run.py```

## Running the Application via Poetry with main entry point
To run the application using Poetry with the main entry point, you can use the following command:
```poetry run run-webapp```

## Running the application via docker
build the docker image
```docker build -t python-webapp .```
run the docker container
```docker run -p 5000:5000 --env-file .env python-webapp```
```docker run -p 8000:8000 --name my-webapp-container my-webapp```
```docker stop my-webapp-container```
```docker rm my-webapp-container```
```docker stop my-webapp-container && docker rm my-webapp-container```
```docker run -d --name my-webapp-container your-image-name```

# Connecting to local mysql database from inside the container
## run the container with env file
```docker run -p 5000:5000 --env-file .env --name my-webapp-container python-webapp```
You can use --env-file in your docker run command:
This will load all variables from .env into the container without committing the file.

## Alternatively, you can use the following command to
```docker run -d --name myapp -e DATABASE_URL=postgresql://user:password@host:5432/dbname -p 8000:8000 myimage:latest```
This will set the DATABASE_URL environment variable inside the container.

### To verify the environment variable is set correctly, you can exec into the running container and print the variable:
```docker exec -it my-webapp-container /bin/bash```
```echo $DATABASE_URL```
#### Alternatively, you can use:
```docker exec -it myapp env | grep DATABASE_URL```


Stop and Remove the container at one go
```docker rm -f my-webapp-container```

```docker ps -a```
```docker logs my-webapp-container```
```docker exec -it my-webapp-container /bin/bash```

## Running the application via docker-compose
To run the application using Docker Compose, you can use the following command:
```docker-compose up --build```

## Running the Application via Poetry with Docker
To run the application using Poetry with Docker, you can use the following command:
```poetry run docker-compose up --build```

### Project Structure
The project is structured as follows:
```
python_webapp/
├── my_app/

## Running Tests