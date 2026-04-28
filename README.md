# IoT_EK

Simple Flask REST API for the Intelligent IoT Solutions case.

## What the solution does

- creates turbines
- creates sensors
- receives sensor data
- checks threshold values
- creates incidents when a threshold is exceeded
- stores data in MySQL

## Local run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the API:

```powershell
python Intillegent-IoT-Solutions-Case.py
```

Swagger:

```text
http://127.0.0.1:5001/apidocs
```

## Docker

Build and run:

```powershell
docker compose up --build
```
