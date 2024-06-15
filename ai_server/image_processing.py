from io import BytesIO
from PIL import Image, UnidentifiedImageError
import numpy as np
from keras.preprocessing import image
import tensorflow as tf
import requests
from flask import abort

def verify_image(image_url):
    if not image_url:
        error_message = "Image URL is required"
        print(error_message)
        abort(400, description=error_message)

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            error_message = "Failed to download image"
            print(error_message)
            abort(400, description=error_message)

        img = Image.open(BytesIO(response.content))
        if img.format not in ['JPEG', 'PNG']:
            error_message = "Unsupported image format"
            print(error_message)
            abort(400, description=error_message)
        return img

    except requests.exceptions.RequestException as e:
        error_message = f"Request failed: {e}"
        print(error_message)
        abort(400, description=error_message)
    except UnidentifiedImageError:
        error_message = "Invalid image content"
        print(error_message)
        abort(400, description=error_message)
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        print(error_message)
        abort(500, description=error_message)

def preprocess_image(img):
    img = img.resize((224, 224))  # 이미지 로드 및 크기 조정
    img_array = image.img_to_array(img)  # 이미지를 numpy 배열로 변환
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    img_array = tf.keras.applications.vgg16.preprocess_input(img_array)  # 모델에 맞게 전처리
    return img_array