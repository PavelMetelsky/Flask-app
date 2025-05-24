#!/bin/bash

# Starting the full version of the project
echo "Starting the entire project infrastructure..."

# Option 1: Using a single full file
docker-compose -f compose/docker-compose.full.yaml up -d

# Option 2: Using multiple files
# docker-compose \
#   -f compose/docker-compose.yaml \
#   -f compose/docker-compose.nginx.yaml \
#   -f compose/docker-compose.monitoring.yaml \
#   up -d

echo "Checking the status of containers..."
docker-compose -f compose/docker-compose.full.yaml ps

echo "All services are up and running! The following URLs are available:"
echo "- Application: http://localhost"
echo "- Swagger documentation: http://localhost/swagger/"
echo "- Grafana: http://localhost:3000 (login: admin, password: admin)"
echo "- Prometheus: http://localhost:9090"
