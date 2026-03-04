import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained model
model = load_model("model/fruit_model.h5")

# Dataset path to read class names
TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"

# Automatically load all fruit classes
classes = sorted(os.listdir(TRAIN_DIR))


def predict_fruit(img_path):

    # Load image
    img = image.load_img(img_path, target_size=(100, 100))
    img_array = image.img_to_array(img)

    # Normalize image
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)

    # Get highest probability index
    index = np.argmax(prediction)

    fruit = classes[index]
    confidence = float(prediction[0][index])

    return fruit, confidence