import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"
TEST_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Test"

IMG_SIZE = 100
BATCH_SIZE = 32

# Data Augmentation (important for CNN performance)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

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

# CNN Model
model = models.Sequential([

    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE,IMG_SIZE,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(256,activation='relu'),
    layers.Dropout(0.5),

    layers.Dense(train_data.num_classes,activation='softmax')

])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Callbacks
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    "model/fruit_model.h5",
    monitor="val_accuracy",
    save_best_only=True
)

# Train model
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=10,
    callbacks=[early_stop, checkpoint]
)

# Evaluate model
test_loss, test_accuracy = model.evaluate(test_data)

print("Test Accuracy:", test_accuracy)