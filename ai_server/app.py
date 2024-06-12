from flask import Flask, request, jsonify
import tensorflow as tf
from model import custom_load_model, get_labels
from image_processing import verify_image, preprocess_image
from predictions import filtered_predictions
from tensorflow.keras.applications.vgg16 import preprocess_input

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
    app.run(host='0.0.0.0', port=5500, debug=True)