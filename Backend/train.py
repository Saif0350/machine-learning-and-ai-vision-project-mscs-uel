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
from tensorflow.keras.models import load_model

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# =========================
# DATASET PATHS
# =========================
TRAIN_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Training"
TEST_DIR = "dataset/fruits-dataset/fruits-360_100x100/fruits-360/Test"

# =========================
# OUTPUT PATHS
# =========================
OUTPUT_DIR = "results"
MODEL_DIR = "model"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# =========================
# MAIN CONFIGURATION
# =========================
IMG_SIZE = 64
MODEL_NAME = "Custom CNN"

# Default experiment settings
DEFAULT_BATCH_SIZE = 32
DEFAULT_EPOCHS = 5
DEFAULT_LEARNING_RATE = 0.001
DEFAULT_DROPOUT_RATE = 0.5
DEFAULT_OPTIMIZER = "adam"

# Techniques
USE_BATCH_NORMALIZATION = True
USE_DROPOUT = True
USE_DATA_AUGMENTATION = True
USE_EARLY_STOPPING = True
USE_MODEL_CHECKPOINT = True

# Architecture
CONV_FILTERS = [8, 16, 32, 64]
DENSE_NEURONS = 64

# Data augmentation
ROTATION_RANGE = 25
ZOOM_RANGE = 0.2
WIDTH_SHIFT_RANGE = 0.1
HEIGHT_SHIFT_RANGE = 0.1
HORIZONTAL_FLIP = True

# Validation split from training data
VALIDATION_SPLIT = 0.2
SEED = 42

# =========================
# PRINT CONFIGURATION
# =========================
print("\n========== PROJECT CONFIGURATION ==========")
print("Model Used:", MODEL_NAME)
print("Image Size:", IMG_SIZE)
print("Default Batch Size:", DEFAULT_BATCH_SIZE)
print("Default Epochs:", DEFAULT_EPOCHS)
print("Default Learning Rate:", DEFAULT_LEARNING_RATE)
print("Default Dropout Rate:", DEFAULT_DROPOUT_RATE)
print("Default Optimizer:", DEFAULT_OPTIMIZER)

print("\nTechniques Used:")
print("1. Rescaling (1./255)")
print(f"2. Data Augmentation: {USE_DATA_AUGMENTATION}")
print(f"3. Batch Normalization: {USE_BATCH_NORMALIZATION}")
print(f"4. Dropout: {USE_DROPOUT}")
print(f"5. Early Stopping: {USE_EARLY_STOPPING}")
print(f"6. Model Checkpoint: {USE_MODEL_CHECKPOINT}")

print("\nArchitecture Details:")
print("Convolution Filters:", CONV_FILTERS)
print("Dense Neurons:", DENSE_NEURONS)
print("===========================================\n")


# =========================
# OPTIMIZER FUNCTION
# =========================
def get_optimizer(name, learning_rate):
    name = name.lower()
    if name == "adam":
        return Adam(learning_rate=learning_rate)
    elif name == "rmsprop":
        return RMSprop(learning_rate=learning_rate)
    elif name == "sgd":
        return SGD(learning_rate=learning_rate)
    else:
        raise ValueError(f"Unsupported optimizer: {name}")


# =========================
# DATA GENERATORS
# =========================
def create_data_generators(batch_size):
    if USE_DATA_AUGMENTATION:
        train_val_datagen = ImageDataGenerator(
            rescale=1. / 255,
            rotation_range=ROTATION_RANGE,
            zoom_range=ZOOM_RANGE,
            width_shift_range=WIDTH_SHIFT_RANGE,
            height_shift_range=HEIGHT_SHIFT_RANGE,
            horizontal_flip=HORIZONTAL_FLIP,
            validation_split=VALIDATION_SPLIT
        )
    else:
        train_val_datagen = ImageDataGenerator(
            rescale=1. / 255,
            validation_split=VALIDATION_SPLIT
        )

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_data = train_val_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=SEED
    )

    val_data = train_val_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=True,
        seed=SEED
    )

    test_data = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    return train_data, val_data, test_data


# =========================
# MODEL BUILDING FUNCTION
# =========================
def build_model(num_classes, dropout_rate, learning_rate, optimizer_name):
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

    # Dense
    model.add(layers.Flatten())
    model.add(layers.Dense(DENSE_NEURONS, activation='relu'))

    if USE_DROPOUT:
        model.add(layers.Dropout(dropout_rate))

    model.add(layers.Dense(num_classes, activation='softmax'))

    optimizer = get_optimizer(optimizer_name, learning_rate)

    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


# =========================
# PLOT TRAINING HISTORY
# =========================
def plot_training_history(history, experiment_name):
    plt.figure(figsize=(12, 5))

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], 'b-o', label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], 'r-o', label='Validation Accuracy')
    plt.title('Training & Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], 'b-o', label='Training Loss')
    plt.plot(history.history['val_loss'], 'r-o', label='Validation Loss')
    plt.title('Training & Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{experiment_name}_final_graph.png", dpi=300)
    plt.show()
# CONFUSION MATRIX
# =========================
from sklearn.metrics import confusion_matrix
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_confusion_matrix(model, test_data, experiment_name):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import confusion_matrix
    import os

    y_true = test_data.classes
    y_pred_probs = model.predict(test_data, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # 🔥 ONLY TAKE FIRST 5 CLASSES
    selected_classes = [0, 1, 2, 3, 4]

    mask = np.isin(y_true, selected_classes)
    y_true_small = y_true[mask]
    y_pred_small = y_pred[mask]

    cm = confusion_matrix(
        y_true_small,
        y_pred_small,
        labels=selected_classes
    )

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        cbar=True,
        xticklabels=selected_classes,
        yticklabels=selected_classes
    )

    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    plt.tight_layout()

    cm_path = os.path.join(OUTPUT_DIR, f"{experiment_name}_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.show()

    print(f"Saved confusion matrix: {cm_path}")



def plot_classification_metrics(model, test_data, experiment_name):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import precision_score, recall_score, f1_score
    import os

    y_true = test_data.classes
    y_pred_probs = model.predict(test_data, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # 🔥 Only show first 5 classes (clean like your slide)
    selected_classes = [0, 1, 2, 3, 4]

    precision = precision_score(y_true, y_pred, average=None, zero_division=0)
    recall = recall_score(y_true, y_pred, average=None, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=None, zero_division=0)

    precision = precision[selected_classes]
    recall = recall[selected_classes]
    f1 = f1[selected_classes]

    x = np.arange(len(selected_classes))
    width = 0.25

    plt.figure(figsize=(10, 6))

    plt.bar(x - width, precision, width, label='Precision')
    plt.bar(x, recall, width, label='Recall')
    plt.bar(x + width, f1, width, label='F1-Score')

    plt.xlabel("Class")
    plt.ylabel("Score")
    plt.title("Per-Class Precision, Recall, and F1-Score")
    plt.xticks(x, selected_classes)
    plt.legend()
    plt.grid(axis='y')

    path = os.path.join(OUTPUT_DIR, f"{experiment_name}_classification_metrics.png")
    plt.savefig(path, dpi=300)
    plt.show()

    print(f"Saved classification metrics graph: {path}")







def plot_roc_curve(model, test_data, experiment_name):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc
    from sklearn.preprocessing import label_binarize
    import os

    y_true = test_data.classes
    y_pred_probs = model.predict(test_data, verbose=1)

    n_classes = test_data.num_classes

    # 🔥 Only take first 5 classes
    selected_classes = [0, 1, 2, 3, 4]

    y_true_bin = label_binarize(y_true, classes=np.arange(n_classes))

    plt.figure(figsize=(8, 6))

    for i in selected_classes:
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred_probs[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'Class {i} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid(True)

    path = os.path.join(OUTPUT_DIR, f"{experiment_name}_roc_curve.png")
    plt.savefig(path, dpi=300)
    plt.show()

    print(f"Saved ROC curve: {path}")

# =========================
# TRAIN SINGLE EXPERIMENT
# =========================
def run_experiment(batch_size, epochs, learning_rate, dropout_rate, optimizer_name, experiment_name):
    print(f"\n========== RUNNING: {experiment_name} ==========")
    print(f"Batch Size: {batch_size}")
    print(f"Epochs: {epochs}")
    print(f"Learning Rate: {learning_rate}")
    print(f"Dropout Rate: {dropout_rate}")
    print(f"Optimizer: {optimizer_name}")
    print("=========================================\n")

    model_path = os.path.join(MODEL_DIR, f"{experiment_name}.h5")

    # =========================
    # LOAD OR TRAIN MODEL
    # =========================
    if os.path.exists(model_path):
        print(f"\nLoading existing model: {model_path}")

        from tensorflow.keras.models import load_model
        model = load_model(model_path)

        # Load data for evaluation
        train_data, val_data, test_data = create_data_generators(batch_size)
        history = None

    else:
        print(f"\nTraining new model: {experiment_name}")

        train_data, val_data, test_data = create_data_generators(batch_size)

        model = build_model(
            num_classes=train_data.num_classes,
            dropout_rate=dropout_rate,
            learning_rate=learning_rate,
            optimizer_name=optimizer_name
        )

        model.summary()

        callbacks = []

        if USE_EARLY_STOPPING:
            early_stop = EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            )
            callbacks.append(early_stop)

        if USE_MODEL_CHECKPOINT:
            checkpoint = ModelCheckpoint(
                model_path,
                monitor="val_accuracy",
                save_best_only=True
            )
            callbacks.append(checkpoint)

        history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks
        )

    # =========================
    # EVALUATE MODEL
    # =========================
    test_loss, test_accuracy = model.evaluate(test_data, verbose=1)

    print("\n========== FINAL RESULTS ==========")
    print("Experiment:", experiment_name)
    print("Test Loss:", round(test_loss, 4))
    print("Test Accuracy:", round(test_accuracy * 100, 2), "%")
    print("===================================\n")

    # =========================
    # PLOTS
    # =========================
    if history is not None:
        plot_training_history(history, experiment_name)
        best_val_accuracy = round(max(history.history['val_accuracy']) * 100, 2)
        best_val_loss = round(min(history.history['val_loss']), 4)
    else:
        print("Skipping training graphs because model was loaded.")
        best_val_accuracy = None
        best_val_loss = None

    plot_confusion_matrix(model, test_data, experiment_name)
    plot_classification_metrics(model, test_data, experiment_name)
    plot_roc_curve(model, test_data, experiment_name)
    return {
        "Experiment": experiment_name,
        "Learning Rate": learning_rate,
        "Dropout Ratio": dropout_rate,
        "Optimizer": optimizer_name,
        "Batch Size": batch_size,
        "Epochs": epochs,
        "Test Accuracy": round(test_accuracy * 100, 2),
        "Test Loss": round(test_loss, 4),
        "Best Val Accuracy": best_val_accuracy,
        "Best Val Loss": best_val_loss
    }


# =========================
# MAIN TRAINING
# =========================
main_result = run_experiment(
    batch_size=DEFAULT_BATCH_SIZE,
    epochs=DEFAULT_EPOCHS,
    learning_rate=DEFAULT_LEARNING_RATE,
    dropout_rate=DEFAULT_DROPOUT_RATE,
    optimizer_name=DEFAULT_OPTIMIZER,
    experiment_name="main_experiment"
)

print("\nMain experiment result:")
print(main_result)


# =========================
# COMPARATIVE ANALYSIS
# =========================
learning_rates = [0.001, 0.0001]
dropout_rates = [0.3, 0.5]
optimizers = ["adam", "rmsprop"]
batch_sizes = [32, 64]
epochs_list = [5]

comparison_results = []

all_combinations = list(itertools.product(
    learning_rates,
    dropout_rates,
    optimizers,
    batch_sizes,
    epochs_list
))

print(f"\nTotal comparative experiments: {len(all_combinations)}\n")

for i, (lr, dr, opt, bs, ep) in enumerate(all_combinations, start=1):
    exp_name = f"exp_{i}_lr{lr}_dr{dr}_{opt}_bs{bs}_ep{ep}".replace(".", "_")

    try:
        result = run_experiment(
            batch_size=bs,
            epochs=ep,
            learning_rate=lr,
            dropout_rate=dr,
            optimizer_name=opt,
            experiment_name=exp_name
        )
        comparison_results.append(result)

    except Exception as e:
        print(f"Experiment {exp_name} failed: {e}")


# =========================
# SAVE COMPARATIVE ANALYSIS
# =========================
if comparison_results:
    df = pd.DataFrame(comparison_results)
    df = df.sort_values(by="Test Accuracy", ascending=False)

    comparison_csv = os.path.join(OUTPUT_DIR, "comparative_analysis.csv")
    df.to_csv(comparison_csv, index=False)

    print("\n========== COMPARATIVE ANALYSIS ==========")
    print(df)
    print("==========================================")
    print(f"Comparative analysis saved to: {comparison_csv}")
else:
    print("No comparison results were generated.")