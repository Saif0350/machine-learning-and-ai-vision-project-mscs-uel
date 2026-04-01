import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# =========================
# DATASET PATHS
# =========================
TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"
TEST_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Test"

# =========================
# CONFIGURATION
# =========================
IMG_SIZE = 64
BATCH_SIZE = 32
EPOCHS = 5
MODEL_NAME = "Custom CNN"

# =========================
# TECHNIQUES USED
# =========================
USE_BATCH_NORMALIZATION = True
USE_DROPOUT = True
DROPOUT_RATE = 0.5
USE_DATA_AUGMENTATION = True
USE_EARLY_STOPPING = True
USE_MODEL_CHECKPOINT = True

# =========================
# NEURONS / FILTERS
# =========================
CONV_FILTERS = [8, 16, 32, 64]
DENSE_NEURONS = 64

# =========================
# DATA AUGMENTATION SETTINGS
# =========================
ROTATION_RANGE = 25
ZOOM_RANGE = 0.2
WIDTH_SHIFT_RANGE = 0.1
HEIGHT_SHIFT_RANGE = 0.1
HORIZONTAL_FLIP = True

# =========================
# PRINT PROJECT SETTINGS
# =========================
print("\n========== PROJECT CONFIGURATION ==========")
print("Model Used:", MODEL_NAME)
print("Image Size:", IMG_SIZE)
print("Batch Size:", BATCH_SIZE)
print("Epochs:", EPOCHS)

print("\nTechniques Used:")
print("1. Rescaling (1./255)")
print(f"2. Data Augmentation: {USE_DATA_AUGMENTATION}")
print(f"3. Batch Normalization: {USE_BATCH_NORMALIZATION}")
print(f"4. Dropout: {USE_DROPOUT} (Rate = {DROPOUT_RATE})")
print(f"5. Early Stopping: {USE_EARLY_STOPPING}")
print(f"6. Model Checkpoint: {USE_MODEL_CHECKPOINT}")

print("\nArchitecture Details:")
print("Convolution Filters:", CONV_FILTERS)
print("Dense Neurons:", DENSE_NEURONS)
print("===========================================\n")

# =========================
# DATA GENERATORS
# =========================
if USE_DATA_AUGMENTATION:
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=ROTATION_RANGE,
        zoom_range=ZOOM_RANGE,
        width_shift_range=WIDTH_SHIFT_RANGE,
        height_shift_range=HEIGHT_SHIFT_RANGE,
        horizontal_flip=HORIZONTAL_FLIP
    )
else:
    train_datagen = ImageDataGenerator(rescale=1. / 255)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

print("Number of classes:", train_data.num_classes)

# =========================
# MODEL BUILDING
# =========================
model = models.Sequential()
model.add(layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)))

# Conv Block 1
model.add(layers.Conv2D(CONV_FILTERS[0], (3, 3), activation='relu'))
if USE_BATCH_NORMALIZATION:
    model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(2, 2))

# Conv Block 2
model.add(layers.Conv2D(CONV_FILTERS[1], (3, 3), activation='relu'))
if USE_BATCH_NORMALIZATION:
    model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(2, 2))

# Conv Block 3
model.add(layers.Conv2D(CONV_FILTERS[2], (3, 3), activation='relu'))
if USE_BATCH_NORMALIZATION:
    model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(2, 2))

# Conv Block 4
model.add(layers.Conv2D(CONV_FILTERS[3], (3, 3), activation='relu'))
if USE_BATCH_NORMALIZATION:
    model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(2, 2))

# Dense Layers
model.add(layers.Flatten())
model.add(layers.Dense(DENSE_NEURONS, activation='relu'))

if USE_DROPOUT:
    model.add(layers.Dropout(DROPOUT_RATE))

model.add(layers.Dense(train_data.num_classes, activation='softmax'))

# =========================
# COMPILE MODEL
# =========================
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# =========================
# CALLBACKS
# =========================
callbacks = []

if USE_EARLY_STOPPING:
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    callbacks.append(early_stop)

if USE_MODEL_CHECKPOINT:
    checkpoint = ModelCheckpoint(
        "model/fruit_model.h5",
        monitor="val_accuracy",
        save_best_only=True
    )
    callbacks.append(checkpoint)

# =========================
# TRAIN MODEL
# =========================
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=EPOCHS,
    callbacks=callbacks
)

# =========================
# EVALUATE MODEL
# =========================
test_loss, test_accuracy = model.evaluate(test_data)

print("\n========== FINAL RESULTS ==========")
print("Model Used:", MODEL_NAME)
print("Dense Neurons Used:", DENSE_NEURONS)
print("Conv Filters Used:", CONV_FILTERS)
print("Test Accuracy:", round(test_accuracy * 100, 2), "%")
print("===================================\n")

# =========================
# Accuracy Graph
plt.figure(figsize=(8, 5))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'])
plt.savefig("model_accuracy.png")
plt.show()

# Loss Graph
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'])
plt.savefig("model_loss.png")
plt.show()