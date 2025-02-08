from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


import pathlib

dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
data_dir = tf.keras.utils.get_file('flower_photos.tar', origin=dataset_url, extract=True)
data_dir = pathlib.Path(data_dir).with_suffix('')

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
