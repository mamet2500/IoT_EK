# MySQL repository for handling turbines, sensors, sensor readings and incidents
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class MySQLRepository:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"Error while executing query: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None

    def fetch_all(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except Error as e:
                print(f"Error while fetching data: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return []

    def fetch_one(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            except Error as e:
                print(f"Error while fetching data: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None

    def create_turbine(self, name, location, status):
        query = "INSERT INTO turbines (name, location, status) VALUES (%s, %s, %s)"
        return self.execute_query(query, (name, location, status))

    def get_turbines(self):
        query = "SELECT * FROM turbines ORDER BY id"
        return self.fetch_all(query)

    def get_turbine_by_id(self, turbine_id):
        query = "SELECT * FROM turbines WHERE id = %s"
        return self.fetch_one(query, (turbine_id,))

    def update_turbine(self, turbine_id, name, location, status):
        query = "UPDATE turbines SET name = %s, location = %s, status = %s WHERE id = %s"
        self.execute_query(query, (name, location, status, turbine_id))

    def delete_turbine(self, turbine_id):
        query = "DELETE FROM turbines WHERE id = %s"
        self.execute_query(query, (turbine_id,))

    def create_sensor(self, name, sensor_type, status, location, threshold_value, unit, turbine_id):
        query = """
            INSERT INTO sensors (name, type, status, location, threshold_value, unit, turbine_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query,
            (name, sensor_type, status, location, threshold_value, unit, turbine_id)
        )

    def get_sensors(self):
        query = "SELECT * FROM sensors ORDER BY id"
        return self.fetch_all(query)

    def get_sensor_by_id(self, sensor_id):
        query = "SELECT * FROM sensors WHERE id = %s"
        return self.fetch_one(query, (sensor_id,))

    def get_sensors_by_turbine(self, turbine_id):
        query = "SELECT * FROM sensors WHERE turbine_id = %s ORDER BY id"
        return self.fetch_all(query, (turbine_id,))

    def update_sensor(self, sensor_id, name, sensor_type, status, location, threshold_value, unit, turbine_id):
        query = """
            UPDATE sensors
            SET name = %s, type = %s, status = %s, location = %s,
                threshold_value = %s, unit = %s, turbine_id = %s
            WHERE id = %s
        """
        self.execute_query(
            query,
            (name, sensor_type, status, location, threshold_value, unit, turbine_id, sensor_id)
        )

    def delete_sensor(self, sensor_id):
        query = "DELETE FROM sensors WHERE id = %s"
        self.execute_query(query, (sensor_id,))

    def create_sensor_reading(self, sensor_id, reading_value, event_type="SensorValueReceived"):
        query = """
            INSERT INTO sensor_readings (sensor_id, event_type, reading_value)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(query, (sensor_id, event_type, reading_value))

    def get_sensor_reading_by_id(self, reading_id):
        query = "SELECT * FROM sensor_readings WHERE id = %s"
        return self.fetch_one(query, (reading_id,))

    def get_sensor_readings(self):
        query = "SELECT * FROM sensor_readings ORDER BY recorded_at DESC"
        return self.fetch_all(query)

    def create_incident(self, sensor_id, reading_id, title, message, severity="high", status="open"):
        query = """
            INSERT INTO incidents (sensor_id, reading_id, title, message, severity, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (sensor_id, reading_id, title, message, severity, status))

    def get_incidents(self):
        query = "SELECT * FROM incidents ORDER BY created_at DESC"
        return self.fetch_all(query)

    def get_incident_by_id(self, incident_id):
        query = "SELECT * FROM incidents WHERE id = %s"
        return self.fetch_one(query, (incident_id,))


if __name__ == "__main__":
    repo = MySQLRepository(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        database=os.environ.get("DB_NAME", "iot_case_db"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "")
    )

    print("Turbines:")
    print(repo.get_turbines())

    print("Sensors:")
    print(repo.get_sensors())

    print("Sensor readings:")
    print(repo.get_sensor_readings())

    print("Incidents:")
    print(repo.get_incidents())
