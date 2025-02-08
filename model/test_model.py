# from ultralytics import YOLO
# from PIL import Image as PILImage
#
#
# # Преобразование изображения в формат, который принимает модель
# def preprocess_image(image_path, input_shape):
#     img = PILImage.open('/Users/petrlutkin/Desktop/MushroomDetection/1.jpg').convert("RGB")
#     img = img.resize((input_shape[1], input_shape[2]))
#     # img = np.array(img).astype(np.float32)  # / 255.0 Нормализация
#     # # img = np.expand_dims(img, axis=0)  # Добавляем batch размерность
#     # return img
#
# model = YOLO('/Users/petrlutkin/Desktop/MushroomDetection/result/train2/weights/best.pt')
# # preprocess_image('1', (1, 512, 512, 3))z
# model.predict(
#     '1.jpg',
#     imgsz=512
# )

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import tensorflow as tf
import numpy as np
from PIL import Image as PILImage

# Загрузка меток классов
def load_labels(label_path):
    with open(label_path, "r") as f:
        return [line.strip() for line in f.readlines()]

# Размер входного изображения (зависит от вашей модели)
INPUT_SIZE = (224, 224)

# Список классов (пример для классификации)
class_names = load_labels("/Users/petrlutkin/Desktop/MushroomDetection/converted_tflite/labels.txt")


class ClassifierApp(App):
    def build(self):
        self.title = "Image Classifier"

        self.image_path = "/Users/petrlutkin/Desktop/MushroomDetection/3.jpeg"

        # Основной макет
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Виджет для отображения изображения
        self.image = Image(size_hint=(1, 0.5), source="")
        self.layout.add_widget(self.image)

        # Метка для отображения результата
        self.result_label = Label(text="Select an image to classify", size_hint=(1, 0.2), font_size="18sp")
        self.layout.add_widget(self.result_label)

        # Кнопка для классификации изображения
        self.classify_button = Button(text="Classify Image", size_hint=(1, 0.1), on_press=self.classify_image)
        self.layout.add_widget(self.classify_button)

        return self.layout

    def preprocess_image(self, image_path):
        # Загрузка изображения с использованием PIL
        image = PILImage.open(image_path).convert("RGB").resize(INPUT_SIZE)
        input_data = np.expand_dims(np.array(image, dtype=np.float32) / 255.0, axis=0)
        return input_data

    def classify_image(self, instance):
        if hasattr(self, "image_path"):
            # Предобработка изображения
            input_data = self.preprocess_image(self.image_path)

            # Инференс модели TFLite
            interpreter = tf.lite.Interpreter(model_path="/Users/petrlutkin/Desktop/MushroomDetection/model.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # Передача данных в модель
            interpreter.set_tensor(input_details[0]["index"], input_data)
            interpreter.invoke()

            # Получение результатов
            output_data = interpreter.get_tensor(output_details[0]["index"])
            predicted_class_idx = np.argmax(output_data)
            predicted_class_name = class_names[predicted_class_idx]
            predicted_probability = output_data[0, predicted_class_idx]

            # Обновление интерфейса с результатами
            self.result_label.text = f"Class: {predicted_class_name}\nProbability: {predicted_probability}"

        else:
            self.result_label.text = "No image selected!"


if __name__ == "__main__":
    ClassifierApp().run()