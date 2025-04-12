@echo off
echo Starting the entire project infrastructure...

REM Running the full version with Docker Compose
docker-compose -f compose/docker-compose.full.yaml up -d

echo Checking the status of containers...
docker-compose -f compose/docker-compose.full.yaml ps

echo All services are up and running! The following URLs are available:
echo - Application: http://localhost
echo - Swagger documentation: http://localhost/swagger/
echo - Grafana: http://localhost:3000 (login: admin, password: admin)
echo - Prometheus: http://localhost:9090
