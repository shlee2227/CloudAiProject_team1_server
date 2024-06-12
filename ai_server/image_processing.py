from io import BytesIO
from PIL import Image
import numpy as np
import requests
from keras.preprocessing import image
from flask import jsonify
import tensorflow as tf

def verify_image(image_url):
    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download image"}), 400

    img = Image.open(BytesIO(response.content))
    if img.format not in ['JPEG', 'PNG']:
        return jsonify({"error": "Unsupported image format"}), 400
    return img

def preprocess_image(img):
    img = img.resize((224, 224))  # 이미지 로드 및 크기 조정
    img_array = image.img_to_array(img)  # 이미지를 numpy 배열로 변환
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    img_array = tf.keras.applications.vgg16.preprocess_input(img_array)  # 모델에 맞게 전처리
    return img_array