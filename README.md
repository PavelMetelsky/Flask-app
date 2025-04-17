# Flask API with JWT Authentication and Gunicorn

A high-performance modular Flask application with JWT authentication, Gunicorn WSGI server, Unix sockets for communication, Redis for visit counting, Swagger documentation, and comprehensive Prometheus/Grafana monitoring.

```mermaid
flowchart TD
    classDef client fill:#9E9E9E,color:white,stroke:#333
    classDef nginx fill:#29B6F6,color:white,stroke:#333
    classDef flask fill:#4CAF50,color:white,stroke:#333
    classDef redis fill:#F44336,color:white,stroke:#333
    classDef prom fill:#FF9800,color:white,stroke:#333
    classDef grafana fill:#3F51B5,color:white,stroke:#333
    classDef volume fill:none,stroke:#333,stroke-dasharray: 5 5
    classDef socket fill:#E91E63,color:white,stroke:#333
    
    subgraph Docker["Docker Compose/Swarm Environment"]
        CLIENT[Client Browser/App]:::client
        
        subgraph NGINX["Nginx Reverse Proxy"]
            NGINX_PROXY["Static File Caching<br>Gzip Compression<br>Load Balancing<br>Port: 80"]:::nginx
        end
        
        subgraph SOCKET["Unix Sockets"]
            UNIX_SOCKET["Gunicorn<br>Unix Sockets"]:::socket
        end
        
        subgraph FLASK_APPS["Flask Application Instances"]
            FLASK1["Flask App #1<br>With Gunicorn<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
            FLASK2["Flask App #2<br>With Gunicorn<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
            FLASK3["Flask App #3<br>With Gunicorn<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
        end
        
        subgraph REDIS_STORE["Data Storage"]
            REDIS["Redis<br>Visit Counter Storage<br>Port: 6379"]:::redis
            REDIS_VOL["Redis Volume"]:::volume
            REDIS_EXP["Redis Exporter<br>Port: 9121"]:::prom
        end
        
        subgraph MONITORING["Monitoring Stack"]
            PROM["Prometheus<br>Metrics Collection<br>Port: 9090"]:::prom
            GRAFANA["Grafana<br>Visualization<br>Port: 3000"]:::grafana
            GRAFANA_VOL["Grafana Volume"]:::volume
        end
        
        %% Connections
        CLIENT --> |HTTP Requests| NGINX_PROXY
        NGINX_PROXY --> |Unix Socket| UNIX_SOCKET
        UNIX_SOCKET --> FLASK1
        UNIX_SOCKET --> FLASK2
        UNIX_SOCKET --> FLASK3
        
        FLASK1 --> |Store/Retrieve Data| REDIS
        FLASK2 --> |Store/Retrieve Data| REDIS
        FLASK3 --> |Store/Retrieve Data| REDIS
        
        REDIS --> REDIS_VOL
        REDIS --- REDIS_EXP
        
        PROM -.->|Scrape Metrics| FLASK1
        PROM -.->|Scrape Metrics| FLASK2
        PROM -.->|Scrape Metrics| FLASK3
        PROM -.->|Scrape Metrics| REDIS_EXP
        
        PROM --> GRAFANA
        GRAFANA --> GRAFANA_VOL
    end
  ```

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
│   └── requirements.txt          # Dependencies with Gunicorn
│
├── docker/                       # Docker files
│   ├── Dockerfile                # Main Dockerfile
│   ├── Dockerfile.optimized      # Multi-stage optimized Dockerfile with Gunicorn
│   └── entrypoint.sh             # Entrypoint script with health checks
│
├── compose/                      # Docker Compose
│   ├── docker-compose.yaml       # Basic configuration
│   ├── docker-compose.full.yaml  # Full configuration with monitoring
│   ├── docker-compose.nginx.yaml # With Nginx
│   ├── docker-compose.monitoring.yaml # With monitoring
│   └── docker-compose.swarm.yaml # For Docker Swarm
│
├── config/                       # Configuration files
│   ├── nginx.conf                # Nginx configuration with Unix socket support
│   ├── prometheus.yml            # Prometheus configuration
│   └── gunicorn.conf.py          # Gunicorn WSGI server configuration
│
├── .env                          # Environment variables
├── static/                       # Static files directory
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

# Start just the application with Nginx
docker-compose -f compose/docker-compose.nginx.yaml up -d

# Start with monitoring
docker-compose -f compose/docker-compose.monitoring.yaml up -d

# Check container status
docker-compose -f compose/docker-compose.full.yaml ps

# View logs
docker-compose -f compose/docker-compose.full.yaml logs -f

# Stop containers
docker-compose -f compose/docker-compose.full.yaml down

# Remove old images and free up resources
docker-compose -f compose/docker-compose.full.yaml down -v
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

# Run the application (development mode)
python src/run.py

# Run with Gunicorn (production mode)
gunicorn --config config/gunicorn.conf.py "run:app"
```

## Configuration

The project uses different configurations for different environments:

- **DevelopmentConfig**: for local development
- **ProductionConfig**: for production
- **TestingConfig**: for testing

Settings are stored in `src/app/config.py` and can be overridden through environment variables in the `.env` file.

## Key Environment Variables

- `SECRET_KEY`: secret key for JWT tokens (default: 'supersecretkey')
- `REDIS_URL`: URL for connecting to Redis (default: 'redis://redis:6379/0')
- `FLASK_ENV`: environment ('development' or 'production')
- `PROMETHEUS_MULTIPROC_DIR`: directory for Prometheus metrics in multi-process mode

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

- **flask-app**: main Flask application with Gunicorn
- **init-app**: initialization tasks (runs once and exits)
- **redis**: cache and data store
- **nginx**: reverse proxy server with Unix socket support
- **prometheus**: metrics collection
- **grafana**: metrics visualization
- **redis-exporter**: export Redis metrics to Prometheus

## Monitoring

After launching the full stack, the following URLs are available:

- **Application**: http://localhost/
- **Swagger**: http://localhost/swagger/
- **Grafana**: http://localhost:3000 (login: admin, password: admin)
- **Prometheus**: http://localhost:9090

## Performance Optimizations

- **Unix Sockets**: Faster communication between Nginx and Gunicorn (10-20% performance gain)
- **Multi-stage Docker builds**: Smaller images for faster deployments
- **Gunicorn Workers**: Multiple worker processes for better CPU utilization
- **Gzip Compression**: Reduces bandwidth usage and speeds up content delivery
- **Response Caching**: Aggressive caching for static content
- **Redis Persistence**: Data volume for Redis to ensure persistence
- **Shared Memory**: Temporary files in RAM for Gunicorn workers

## Security Enhancements

- **Non-root User**: Container runs as unprivileged user
- **Multi-stage Builds**: Reduced attack surface
- **Healthchecks**: Automatic handling of unhealthy services
- **Environment Variables**: Secrets managed through `.env` file
- **Unix Sockets**: Reduced network exposure compared to TCP

## Application Architecture

The application is built on a modular architecture using Flask Blueprints:

- **Factory Pattern**: application creation through the `create_app()` function
- **Blueprints**: modular organization of routes
- **Dependency Injection**: initializing extensions separately from their use
- **Config Classes**: separating configurations by environment
- **WSGI Server**: Gunicorn for production-grade performance

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

## Scaling

For horizontal scaling, you can use Docker Swarm:

```bash
# Initialize Docker Swarm
docker swarm init

# Deploy the stack in Swarm
docker stack deploy -c compose/docker-compose.swarm.yaml myapp

# Scale the application
docker service scale myapp_flask-app=5

# Check service status
docker service ls
```

## Troubleshooting

### Common Issues

- **Socket permissions**: If you encounter permission issues with Unix sockets, check the permissions on the `/run/gunicorn` directory
- **Container not starting**: Check the health checks with `docker-compose ps` and view logs with `docker-compose logs service-name`
- **Redis connection errors**: Ensure Redis is fully started before the Flask application attempts to connect

### Logs

To check logs for a specific service:

```bash
docker-compose -f compose/docker-compose.full.yaml logs -f flask-app
```

### Container Shell Access

For debugging, you can access a running container shell:

```bash
docker exec -it flask_app /bin/bash
```