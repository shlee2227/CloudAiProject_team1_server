from flask import Flask, request, jsonify
from model import custom_load_model, get_labels
from image_processing import verify_image, preprocess_image
from predictions import filtered_predictions
from tensorflow.keras.applications.vgg16 import preprocess_input

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

def execute_query(connection, query):
    """Execute a single query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def fetch_data(connection, query):
    """Fetch data from the database."""
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    

app = Flask(__name__)

# 모델 Load
model = custom_load_model()
labels = get_labels()
preprocess_input = preprocess_input

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        image_url = data.get('image_url')
        img = verify_image(image_url)
        img_arr = preprocess_image(img) 
        predictions = model.predict(img_arr)
        results = filtered_predictions(predictions)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    connection = create_connection()
    app.run(host='0.0.0.0', port=5500, debug=True)
    
    if connection:
        # Fetch data from the 'dog' table
        dog_query = "SELECT * FROM dog"
        dogs = fetch_data(connection, dog_query)
        print(dogs)

        # Fetch data from the 'dog_img' table
        dog_img_query = "SELECT * FROM dog_img"
        dog_images = fetch_data(connection, dog_img_query)
        print(dog_images)

        connection.close()
