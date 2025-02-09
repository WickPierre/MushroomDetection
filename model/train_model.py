import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os


print(tf.config.list_physical_devices("GPU"))  # Должен увидеть GPU

# Параметры модели
img_size = (224, 224)  # Размер входных изображений
batch_size = 32  # Размер батча
epochs = 10  # Количество эпох

# Путь к вашему датасету
dataset_path = "/Users/petrlutkin/Desktop/MushroomDetection/dataset_new"

# Загрузка тренировочного и валидационного датасета
train_ds = keras.preprocessing.image_dataset_from_directory(
    os.path.join(dataset_path, "train"),
    image_size=img_size,
    batch_size=batch_size,
    label_mode="int"
)

val_ds = keras.preprocessing.image_dataset_from_directory(
    os.path.join(dataset_path, "val"),
    image_size=img_size,
    batch_size=batch_size,
    label_mode="int"
)

# Получаем классы
class_names = train_ds.class_names
num_classes = len(class_names)
print("Классы:", class_names)


# Нормализация изображений
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Повышение производительности
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)


# Создание модели на основе MobileNetV2
base_model = keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,  # Убираем последний слой, чтобы обучить свой
    weights="imagenet"
)

base_model.trainable = False  # Замораживаем веса предобученной модели

# Добавляем свои слои
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation="softmax")  # Количество классов
])

# Компиляция модели
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Обучение модели
with tf.device("/GPU:0"):
    model.fit(train_ds, validation_data=val_ds, epochs=epochs)

# Сохранение модели
model.save("image_classifier.keras")

# model = tf.keras.models.load_model("image_classifier.h5")

# Конвертация в TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("../model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Обучение завершено! Модель сохранена в 'model.tflite'")




from ultralytics import YOLO

# # Загружаем предобученную модель YOLOv11
# model = YOLO('yolo11n-cls.pt')  # Выберите размер модели: n, s, m, l, x
#
# # Запускаем обучение
# model.train(
#     data='../dataset_new/',
#     epochs=20,
#     imgsz=512,
#     batch=32,
#     device='mps',
#     project='../result'
# )