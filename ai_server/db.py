import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_HOST =os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')


def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            # port=MYSQL_PORT, # 3306 아닌 경우에만 활성화
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def get_dog_info_by_id(connection, dog_id):
    query = f"SELECT * FROM dog WHERE dog_id = {dog_id}"
    print(query)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Query executed successfully")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# def fetch_dog_table(connection, query):
#     """Fetch data from the database."""
#     cursor = connection.cursor(dictionary=True)
#     result = None
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")
#         return None