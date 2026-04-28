from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
import os
from dotenv import load_dotenv

from mysqlrepo import MySQLRepository

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SWAGGER"] = {
    "title": "Intelligent IoT Solutions API",
    "uiversion": 3,
}
swagger = Swagger(app)

repo = MySQLRepository(
    host=os.environ.get("DB_HOST", "127.0.0.1"),
    database=os.environ.get("DB_NAME", "iot_case_db"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "")
)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


@app.route("/turbines", methods=["GET"])
def get_turbines():
    """
    Get all turbines
    ---
    tags:
      - Turbines
    responses:
      200:
        description: A list of turbines
        schema:
          type: array
          items:
            $ref: '#/definitions/Turbine'
    definitions:
      Turbine:
        type: object
        properties:
          id:
            type: integer
            example: 1
          name:
            type: string
            example: Turbine A1
          location:
            type: string
            example: Offshore Park North
          status:
            type: string
            example: active
      Sensor:
        type: object
        properties:
          id:
            type: integer
            example: 1
          name:
            type: string
            example: Main Vibration Sensor
          type:
            type: string
            example: vibration
          status:
            type: string
            example: active
          location:
            type: string
            example: Gearbox housing
          threshold_value:
            type: number
            example: 80
          unit:
            type: string
            example: mm/s
          turbine_id:
            type: integer
            example: 1
      SensorReading:
        type: object
        properties:
          id:
            type: integer
          sensor_id:
            type: integer
          event_type:
            type: string
            example: SensorValueReceived
          reading_value:
            type: number
            example: 87.5
          recorded_at:
            type: string
            example: 2026-04-23 10:45:00
      Incident:
        type: object
        properties:
          id:
            type: integer
          sensor_id:
            type: integer
          reading_id:
            type: integer
          title:
            type: string
            example: Critical threshold exceeded
          message:
            type: string
            example: Sensor exceeded threshold
          severity:
            type: string
            example: high
          status:
            type: string
            example: open
          created_at:
            type: string
            example: 2026-04-23 10:45:01
    """
    return jsonify(repo.get_turbines())


@app.route("/turbines/<int:turbine_id>", methods=["GET"])
def get_turbine(turbine_id):
    """
    Get a turbine by id
    ---
    tags:
      - Turbines
    parameters:
      - name: turbine_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: The turbine
        schema:
          $ref: '#/definitions/Turbine'
      404:
        description: Turbine not found
    """
    turbine = repo.get_turbine_by_id(turbine_id)
    if turbine is None:
        return error_response("Turbine not found", 404)
    return jsonify(turbine)


@app.route("/turbines", methods=["POST"])
def create_turbine():
    """
    Create a new turbine
    ---
    tags:
      - Turbines
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            location:
              type: string
            status:
              type: string
          example:
            name: Turbine A1
            location: Offshore Park North
            status: active
    responses:
      201:
        description: Created turbine
        schema:
          $ref: '#/definitions/Turbine'
      400:
        description: Invalid payload
    """
    payload = request.get_json(silent=True)
    if payload is None or "name" not in payload:
        return error_response("Field 'name' is required", 400)

    turbine_id = repo.create_turbine(
        payload["name"],
        payload.get("location"),
        payload.get("status", "active")
    )
    return jsonify(repo.get_turbine_by_id(turbine_id)), 201


@app.route("/sensors", methods=["GET"])
def get_sensors():
    """
    Get all sensors
    ---
    tags:
      - Sensors
    responses:
      200:
        description: A list of sensors
        schema:
          type: array
          items:
            $ref: '#/definitions/Sensor'
    """
    return jsonify(repo.get_sensors())


@app.route("/sensors/<int:sensor_id>", methods=["GET"])
def get_sensor(sensor_id):
    """
    Get a sensor by id
    ---
    tags:
      - Sensors
    parameters:
      - name: sensor_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: The sensor
        schema:
          $ref: '#/definitions/Sensor'
      404:
        description: Sensor not found
    """
    sensor = repo.get_sensor_by_id(sensor_id)
    if sensor is None:
        return error_response("Sensor not found", 404)
    return jsonify(sensor)


@app.route("/sensors", methods=["POST"])
def create_sensor():
    """
    Create a new sensor
    ---
    tags:
      - Sensors
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - type
            - status
            - turbine_id
          properties:
            name:
              type: string
            type:
              type: string
            status:
              type: string
            location:
              type: string
            threshold_value:
              type: number
            unit:
              type: string
            turbine_id:
              type: integer
          example:
            name: Main Vibration Sensor
            type: vibration
            status: active
            location: Gearbox housing
            threshold_value: 80
            unit: mm/s
            turbine_id: 1
    responses:
      201:
        description: Created sensor
        schema:
          $ref: '#/definitions/Sensor'
      400:
        description: Invalid payload
      404:
        description: Turbine not found
    """
    payload = request.get_json(silent=True)
    if (
        payload is None
        or "name" not in payload
        or "type" not in payload
        or "status" not in payload
        or "turbine_id" not in payload
    ):
        return error_response("Fields 'name', 'type', 'status' and 'turbine_id' are required", 400)

    turbine_id = payload["turbine_id"]
    if repo.get_turbine_by_id(turbine_id) is None:
        return error_response("Turbine not found", 404)

    sensor_id = repo.create_sensor(
        payload["name"],
        payload["type"],
        payload["status"],
        payload.get("location"),
        payload.get("threshold_value", 80),
        payload.get("unit", "mm/s"),
        turbine_id
    )
    return jsonify(repo.get_sensor_by_id(sensor_id)), 201


@app.route("/turbines/<int:turbine_id>/sensors", methods=["GET"])
def get_turbine_sensors(turbine_id):
    """
    Get all sensors for a turbine
    ---
    tags:
      - Turbines
    parameters:
      - name: turbine_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Sensors belonging to the turbine
        schema:
          type: array
          items:
            $ref: '#/definitions/Sensor'
      404:
        description: Turbine not found
    """
    turbine = repo.get_turbine_by_id(turbine_id)
    if turbine is None:
        return error_response("Turbine not found", 404)
    return jsonify(repo.get_sensors_by_turbine(turbine_id))


@app.route("/sensor-data", methods=["POST"])
def create_sensor_data():
    """
    Receive sensor data and evaluate threshold
    ---
    tags:
      - Sensor Data
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - sensor_id
            - value
          properties:
            sensor_id:
              type: integer
            value:
              type: number
          example:
            sensor_id: 1
            value: 87.5
    responses:
      201:
        description: Sensor data processed
        schema:
          type: object
          properties:
            reading:
              $ref: '#/definitions/SensorReading'
            incident_created:
              type: boolean
            incident:
              $ref: '#/definitions/Incident'
      400:
        description: Invalid payload
      404:
        description: Sensor not found
    """
    payload = request.get_json(silent=True)
    if payload is None or "sensor_id" not in payload or "value" not in payload:
        return error_response("Fields 'sensor_id' and 'value' are required", 400)

    sensor = repo.get_sensor_by_id(payload["sensor_id"])
    if sensor is None:
        return error_response("Sensor not found", 404)

    try:
        reading_value = float(payload["value"])
    except (TypeError, ValueError):
        return error_response("Field 'value' must be numeric", 400)

    reading_id = repo.create_sensor_reading(sensor["id"], reading_value)
    reading = repo.get_sensor_reading_by_id(reading_id)

    incident = None
    incident_created = False
    threshold_value = float(sensor["threshold_value"])

    if reading_value > threshold_value:
        incident_id = repo.create_incident(
            sensor["id"],
            reading_id,
            "Critical threshold exceeded",
            (
                f"Sensor '{sensor['name']}' on turbine {sensor['turbine_id']} reported "
                f"{reading_value} {sensor['unit']}, which is above threshold "
                f"{threshold_value} {sensor['unit']}."
            ),
            severity="high",
            status="open"
        )
        incident = repo.get_incident_by_id(incident_id)
        incident_created = True

    return jsonify(
        {
            "reading": reading,
            "incident_created": incident_created,
            "incident": incident
        }
    ), 201


@app.route("/sensor-readings", methods=["GET"])
def get_sensor_readings():
    """
    Get all sensor readings
    ---
    tags:
      - Sensor Data
    responses:
      200:
        description: A list of sensor readings
        schema:
          type: array
          items:
            $ref: '#/definitions/SensorReading'
    """
    return jsonify(repo.get_sensor_readings())


@app.route("/incidents", methods=["GET"])
def get_incidents():
    """
    Get all incidents
    ---
    tags:
      - Incidents
    responses:
      200:
        description: A list of incidents
        schema:
          type: array
          items:
            $ref: '#/definitions/Incident'
    """
    return jsonify(repo.get_incidents())


@app.route("/incidents/<int:incident_id>", methods=["GET"])
def get_incident(incident_id):
    """
    Get an incident by id
    ---
    tags:
      - Incidents
    parameters:
      - name: incident_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: The incident
        schema:
          $ref: '#/definitions/Incident'
      404:
        description: Incident not found
    """
    incident = repo.get_incident_by_id(incident_id)
    if incident is None:
        return error_response("Incident not found", 404)
    return jsonify(incident)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
