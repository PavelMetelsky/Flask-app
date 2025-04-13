# Flask API with JWT Authentication

A modular Flask application with JWT authentication, Redis for visit counting, Swagger documentation, and Prometheus/Grafana monitoring.

## Project Structure

```
Task 3/
├── src/                          # Application source code
│   ├── app/                      # Main application package
│   │   ├── __init__.py           # Application factory
│   │   ├── config.py             # Configuration
│   │   ├── extensions.py         # Extensions initialization
│   │   ├── api/                  # API module
│   │   │   ├── __init__.py
│   │   │   └── routes.py         # API routes (/ping, /count)
│   │   └── auth/                 # Authentication module
│   │       ├── __init__.py
│   │       ├── decorators.py     # JWT decorator
│   │       └── routes.py         # Authentication routes (/login)
│   ├── run.py                    # Application entry point
│   └── requirements.txt          # Dependencies
│
├── docker/                       # Docker files
│   ├── Dockerfile                # Main Dockerfile
│   └── Dockerfile.optimized      # Optimized Dockerfile
│
├── compose/                      # Docker Compose
│   ├── docker-compose.yaml       # Basic configuration
│   ├── docker-compose.full.yaml  # Full configuration
│   ├── docker-compose.nginx.yaml # With Nginx
│   ├── docker-compose.monitoring.yaml # With monitoring
│   └── docker-compose.swarm.yaml # For Docker Swarm
│
├── config/                       # Configuration files
│   ├── nginx.conf                # Nginx configuration
│   └── prometheus.yml            # Prometheus configuration
│
├── start.bat                     # Windows startup script
├── start.sh                      # Linux startup script
└── README.md                     # Project documentation
```

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Installation and Startup

### Launching with Docker Compose

```bash
# Start the full stack (Flask, Redis, Nginx, Prometheus, Grafana)
docker-compose -f compose/docker-compose.full.yaml up -d

# Check container status
docker-compose -f compose/docker-compose.full.yaml ps

# Stop containers
docker-compose -f compose/docker-compose.full.yaml down

# Remove old images and free up resources
docker-compose -f compose/docker-compose.full.yaml rm -f
docker system prune -af --volumes
```

### Using the startup scripts

**Linux/Mac**:
```bash
./start.sh
```

**Windows**:
```
start.bat
```

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r src/requirements.txt

# Run the application
python src/run.py
```

## Configuration

The project uses different configurations for different environments:

- **DevelopmentConfig**: for local development
- **ProductionConfig**: for production
- **TestingConfig**: for testing

Settings are stored in `src/app/config.py` and can be overridden through environment variables.

## Key Environment Variables

- `SECRET_KEY`: secret key for JWT tokens (default: 'supersecretkey')
- `REDIS_URL`: URL for connecting to Redis (default: 'redis://redis:6379/0')
- `FLASK_ENV`: environment ('development' or 'production')

## API Endpoints

### Public Endpoints

- `GET /api/ping`: API availability check
  - Response: `{"status": "ok"}`

- `POST /auth/login`: obtain JWT token
  - Request: `{"username": "admin", "password": "password"}`
  - Response: `{"token": "<JWT_TOKEN>"}`

### Protected Endpoints (require JWT token)

- `GET /api/count`: visit counter
  - Header: `Authorization: Bearer <JWT_TOKEN>`
  - Response: `{"visits": <visit_count>}`

## Swagger Documentation

API documentation is available at `/swagger/` after starting the application.

## Docker Containers

### Services in the full configuration

- **flask-app**: main Flask application
- **redis**: cache and data store
- **nginx**: reverse proxy server
- **prometheus**: metrics collection
- **grafana**: metrics visualization
- **redis-exporter**: export Redis metrics to Prometheus

## Monitoring

After launching the full stack, the following URLs are available:

- **Application**: http://localhost/
- **Swagger**: http://localhost/swagger/
- **Grafana**: http://localhost:3000 (login: admin, password: admin)
- **Prometheus**: http://localhost:9090

## Application Architecture

The application is built on a modular architecture using Flask Blueprints:

- **Factory Pattern**: application creation through the `create_app()` function
- **Blueprints**: modular organization of routes
- **Dependency Injection**: initializing extensions separately from their use
- **Config Classes**: separating configurations by environment

## Development

### Adding new routes

To add new routes:

1. Create or select an existing blueprint
2. Add a route with the `@blueprint.route()` decorator
3. To protect a route, use the `@token_required` decorator

### Local testing

```bash
# Running tests
# TODO: add tests

# Checking API availability
curl http://localhost/api/ping

# Obtaining a JWT token
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "password"}' http://localhost/auth/login

# Accessing a protected route
curl -H "Authorization: Bearer <received_token>" http://localhost/api/count
```

## Additional Information

### Performance

- An optimized multi-stage Dockerfile is used to reduce image size
- Nginx is configured to cache static files
- Redis is used as a fast data store

### Scaling

For horizontal scaling, you can use Docker Swarm:

```bash
# Initialize Docker Swarm
docker swarm init

# Deploy the stack in Swarm
docker stack deploy -c compose/docker-compose.swarm.yaml myapp
```
