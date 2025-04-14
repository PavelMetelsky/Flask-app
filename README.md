# Flask API with JWT Authentication

A modular Flask application with JWT authentication, Redis for visit counting, Swagger documentation, and Prometheus/Grafana monitoring.

```mermaid
flowchart TD
    classDef client fill:#9E9E9E,color:white,stroke:#333
    classDef nginx fill:#29B6F6,color:white,stroke:#333
    classDef flask fill:#4CAF50,color:white,stroke:#333
    classDef redis fill:#F44336,color:white,stroke:#333
    classDef prom fill:#FF9800,color:white,stroke:#333
    classDef grafana fill:#3F51B5,color:white,stroke:#333
    classDef volume fill:none,stroke:#333,stroke-dasharray: 5 5
    
    subgraph Docker["Docker Compose/Swarm Environment"]
        CLIENT[Client Browser/App]:::client
        
        subgraph NGINX["Nginx Reverse Proxy"]
            NGINX_PROXY["Static File Caching<br>Load Balancing<br>Port: 80"]:::nginx
        end
        
        subgraph FLASK_APPS["Flask Application Instances"]
            FLASK1["Flask App #1<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
            FLASK2["Flask App #2<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
            FLASK3["Flask App #3<br>API Routes (/ping, /count)<br>Auth Routes (/login)<br>JWT Authentication<br>Metrics Exporter"]:::flask
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
        NGINX_PROXY --> |Load Balance<br>Port: 5000| FLASK1
        NGINX_PROXY --> |Load Balance<br>Port: 5000| FLASK2
        NGINX_PROXY --> |Load Balance<br>Port: 5000| FLASK3
        
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
