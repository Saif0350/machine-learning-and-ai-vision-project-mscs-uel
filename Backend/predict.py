import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

IMG_SIZE = 64
MODEL_PATH = "model/main_experiment.h5"
TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"

# Load trained model
model = load_model(MODEL_PATH)

# Load only actual class folders
classes = sorted([
    folder for folder in os.listdir(TRAIN_DIR)
    if os.path.isdir(os.path.join(TRAIN_DIR, folder))
])

print("Loaded model:", MODEL_PATH)
print("Number of classes:", len(classes))


def predict_fruit(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)

    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array, verbose=0)
    index = int(np.argmax(prediction[0]))

    fruit = classes[index]
    confidence = float(prediction[0][index]) * 100

    return fruit, round(confidence, 2)