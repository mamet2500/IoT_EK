# IoT_EK

Simple Flask REST API for the Intelligent IoT Solutions case.

## What the solution does

- creates turbines
- creates sensors
- receives sensor data
- checks threshold values
- creates incidents when a threshold is exceeded
- stores data in MySQL

## Project structure

Main files in the project:

- `Intillegent-IoT-Solutions-Case.py` - the Flask REST API
- `mysqlrepo.py` - database access layer
- `MySQL_undervisning.sql` - SQL schema for MySQL
- `docker-compose.yml` - starts API and MySQL with Docker
- `Dockerfile` - builds the API container
- `.github/workflows/ci.yml` - GitHub Actions CI workflow

## Local setup

Create a local `.env` file based on `.env.example` and set your database values, for example:

```env
DB_HOST=127.0.0.1
DB_NAME=iot_case_db
DB_USER=root
DB_PASSWORD=your_password_here
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run with Docker

Build and run the solution:

```powershell
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:5001/apidocs
```

Useful endpoints:

```text
http://127.0.0.1:5001/turbines
http://127.0.0.1:5001/sensors
http://127.0.0.1:5001/sensor-data
http://127.0.0.1:5001/incidents
```

## Reset the database

If you want to start completely from scratch:

```powershell
docker compose down -v
docker compose up --build
```

This removes the Docker database volume and recreates the database from the SQL file.

## Test flow

A simple demo/test sequence is:

1. Create a turbine
2. Create a sensor
3. Send a normal sensor value
4. Send a critical sensor value
5. Get incidents
6. Check MySQL Workbench

## MySQL Workbench

When using Docker, connect MySQL Workbench to:

- Host: `127.0.0.1`
- Port: `3307`
- User: `root`
- Password: your value from `.env`

Useful SQL queries:

```sql
USE iot_case_db;
SELECT * FROM turbines;
SELECT * FROM sensors;
SELECT * FROM sensor_readings;
SELECT * FROM incidents;
```

## GitHub

Commit and push changes:

```powershell
git add .
git commit -m "Your commit message"
git push
```

## GitHub Actions

The repository includes a simple CI workflow in `.github/workflows/ci.yml`.

It runs automatically on push and pull request to `main` and does three things:

- installs Python dependencies
- checks that the main Python files compile without syntax errors
- builds the Docker image

## Delivery use

This project can be demonstrated by showing:

- GitHub repository
- GitHub Actions workflow
- Docker running the API and MySQL
- Swagger or Postman requests
- persisted data in MySQL Workbench
