import mysql.connector
from util.PropertyUtil import get_property_string

def get_connection():
    try:
        props = get_property_string("db.properties")
        c = mysql.connector.connect(
            host=props["host"],
            port=int(props["port"]),
            user=props["user"],
            password=props["password"],
            database=props["database"]
        )
        print("Database connection successful")
        return c
    except KeyError as ke:
        print(" Missing key in db.properties: {ke}")
        raise
    except mysql.connector.Error as err:
        print("MySQL Connection Error: {err}")
        raise
    except Exception as e:
        print("connection is unsuccesful: {e}")
        raise