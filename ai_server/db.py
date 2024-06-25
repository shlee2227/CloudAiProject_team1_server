import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

RDS_HOST =os.getenv('RDS_HOST')
RDS_PORT = os.getenv('RDS_PORT')
RDS_USERNAME = os.getenv('RDS_USERNAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DATABASE = os.getenv('RDS_DATABASE')


def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=RDS_HOST,
            # port=RDS_PORT, # 3306 아닌 경우에만 활성화
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
            # with connection.cursor() as cursor:
            #      # 예시 쿼리: 테이블 목록 가져오기
            #     cursor.execute("SHOW TABLES;")
            #     tables = cursor.fetchall()
            #     print("Tables in the database:")
            #     for table in tables:
            #         print(table)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def get_dog_info_by_id(connection, dog_id):
    query = f"SELECT * FROM dog WHERE dog_id = {dog_id}" # 컬럼명 명시 
    # print(query)
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