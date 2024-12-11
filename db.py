import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try: 
        connection = mysql.connector.connect(
            host="localhost",
            user="BLG317E",
            password="Password12345*",
            database="euro"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None