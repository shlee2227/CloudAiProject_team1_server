import csv
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

# 커스텀 layer CustomDataAugmentation 정의
class CustomDataAugmentation(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(CustomDataAugmentation, self).__init__(**kwargs)
        self.flip = tf.keras.layers.RandomFlip('horizontal')
        self.rotate = tf.keras.layers.RandomRotation(0.2)

    def call(self, inputs, training=None):
        if training:
            inputs = self.flip(inputs)
            inputs = self.rotate(inputs)
        return inputs

    def get_config(self):
        config = super(CustomDataAugmentation, self).get_config()
        return config


# 커스텀 layer precess_input_lambda 정의 
@tf.keras.utils.register_keras_serializable()
def preprocess_input_lambda(x):
    x = preprocess_input(x)
    return x

# 모델 Load
def custom_load_model():
    tf.keras.utils.register_keras_serializable()(CustomDataAugmentation)
    # 모델 불러오기 
    model_path = "/Users/leeshinhee/Documents/newdeal/project/Code/server/ai_server/dog_breed_model/model_13breed_tf2150_epoch200_adam_default.keras"
    model = tf.keras.models.load_model(model_path, custom_objects={
        'preprocess_input_lambda': preprocess_input_lambda,
        'CustomDataAugmentation': CustomDataAugmentation,
    }, safe_mode=False, compile=False)
    # 모델 불러올때 컴파일 하지 않았으므로 여기서 컴파일 (모델 load시 컴파일 하면 에러 뜸)
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])
    return model

# Load labels
def get_labels():
    labels_path = "ai_server/dog_breed_model/labels.csv"
    with open(labels_path, mode='r', encoding='UTF-8') as f:
        csv_reader = csv.reader(f)
        labels = {int(item[0]): item[1].strip() for item in csv_reader}
    return labels