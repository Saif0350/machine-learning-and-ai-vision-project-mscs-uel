import os
import itertools
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam, RMSprop, SGD
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.regularizers import l2

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc
from sklearn.preprocessing import label_binarize
import seaborn as sns

# =========================
# PATHS
# =========================
TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"
TEST_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Test"

OUTPUT_DIR = "results"
MODEL_DIR = "model"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# =========================
# CONFIG
# =========================
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5  
LEARNING_RATE = 0.001
DROPOUT_RATE = 0.5

# =========================
# OPTIMIZER
# =========================
def get_optimizer(name, lr):
    if name == "adam":
        return Adam(learning_rate=lr)
    elif name == "rmsprop":
        return RMSprop(learning_rate=lr)
    else:
        return SGD(learning_rate=lr)

# =========================
# DATA
# =========================
def get_data():
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    test = ImageDataGenerator(rescale=1./255).flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train, val, test

# =========================
# RESNET MODEL
# =========================
def build_model(num_classes):

    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )

    # Freeze base
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)

    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation='relu', kernel_regularizer=l2(0.001))(x)
    x = layers.Dropout(DROPOUT_RATE)(x)

    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(DROPOUT_RATE)(x)

    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs=base_model.input, outputs=outputs)

    model.compile(
        optimizer=get_optimizer("adam", LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

# =========================
# TRAIN
# =========================
def train_model():
    train, val, test = get_data()

    model = build_model(train.num_classes)
    model.summary()

    model_path = os.path.join(MODEL_DIR, "resnet_model.h5")

    callbacks = [
        EarlyStopping(patience=3, restore_best_weights=True),
        ModelCheckpoint(model_path, save_best_only=True)
    ]

    history = model.fit(
        train,
        validation_data=val,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    return model, history, test

# =========================
# PLOTS
# =========================
def plot_history(history):
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='val')
    plt.title("Accuracy")
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='val')
    plt.title("Loss")
    plt.legend()

    plt.savefig(f"{OUTPUT_DIR}/training_graph.png")
    plt.show()

# =========================
# CONFUSION MATRIX
# =========================
def plot_confusion(model, test):
    y_true = test.classes
    y_pred = np.argmax(model.predict(test), axis=1)

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8,6))
    sns.heatmap(cm, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig(f"{OUTPUT_DIR}/confusion.png")
    plt.show()

# =========================
# METRICS
# =========================
def plot_metrics(model, test):
    y_true = test.classes
    y_pred = np.argmax(model.predict(test), axis=1)

    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')

    print("\nPrecision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

# =========================
# ROC
# =========================
def plot_roc(model, test):
    y_true = test.classes
    y_pred = model.predict(test)

    y_bin = label_binarize(y_true, classes=np.arange(test.num_classes))

    for i in range(3):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_pred[:, i])
        plt.plot(fpr, tpr, label=f'class {i}')

    plt.legend()
    plt.title("ROC Curve")
    plt.savefig(f"{OUTPUT_DIR}/roc.png")
    plt.show()

# =========================
# MAIN
# =========================
model, history, test = train_model()

loss, acc = model.evaluate(test)

print("\nFinal Accuracy:", acc * 100)

plot_history(history)
plot_confusion(model, test)
plot_metrics(model, test)
plot_roc(model, test)