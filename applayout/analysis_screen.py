import threading
import numpy as np
import os
from kivy.utils import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from applayout.models import RoundedButton
from PIL import Image as PILImage
import database as db
from kivy.lang import Builder

if platform == "android":
    from android.storage import primary_external_storage_path
    from jnius import autoclass

    File = autoclass("java.io.File")
    Interpreter = autoclass("org.tensorflow.lite.Interpreter")
    InterpreterOptions = autoclass("org.tensorflow.lite.Interpreter$Options")
    Tensor = autoclass("org.tensorflow.lite.Tensor")
    DataType = autoclass("org.tensorflow.lite.DataType")
    TensorBuffer = autoclass("org.tensorflow.lite.support.tensorbuffer.TensorBuffer")
    ByteBuffer = autoclass("java.nio.ByteBuffer")
else:
    import tensorflow as tf

    Interpreter = tf.lite.Interpreter

Builder.load_string(
    """
<PredictMushroom>:
    name: "predict_mushroom"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.26, 0.27, 0.33, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            id: image_display
            size_hint: (1, 0.8)
            allow_stretch: True
            keep_ratio: True

        Label:
            id: result_label
            text: "Classifying image..."
            size_hint: (1, 0.1)
            halign: "center"
            valign: "middle"
            color: (1, 1, 1, 1)

        BoxLayout:
            orientation: "vertical"
            size_hint: (1, 0.2)
            spacing: dp(5)
            
            RoundedButton:
                text: "Назад"
                size_hint: (0.9, 0.05)
                pos_hint: {"center_x": 0.5}
                on_release: root.go_back()
    """
)


class TensorFlowModel:
    def load(self, model_filename, num_threads=None):
        model = File(model_filename)
        options = InterpreterOptions()
        if num_threads is not None:
            options.setNumThreads(num_threads)
        self.interpreter = Interpreter(model, options)
        self.allocate_tensors()

    def allocate_tensors(self):
        self.interpreter.allocateTensors()
        self.input_shape = self.interpreter.getInputTensor(0).shape()
        self.output_shape = self.interpreter.getOutputTensor(0).shape()
        self.output_type = self.interpreter.getOutputTensor(0).dataType()

    def get_input_shape(self):
        return self.input_shape

    def resize_input(self, shape):
        if self.input_shape != shape:
            self.interpreter.resizeInput(0, shape)
            self.allocate_tensors()

    def pred(self, x):
        # Предполагается одна входная и одна выходная переменная
        input = ByteBuffer.wrap(x.tobytes())
        output = TensorBuffer.createFixedSize(self.output_shape, self.output_type)
        self.interpreter.run(input, output.getBuffer().rewind())
        return np.reshape(np.array(output.getFloatArray()), self.output_shape)


def delete_image(image_path):
    if os.path.exists(image_path):  # Проверяем, существует ли файл
        os.remove(image_path)  # Удаляем файл
        print(f"Файл {image_path} успешно удален.")
    else:
        print(f"Файл {image_path} не существует.")


# Загрузка меток классов
def load_labels(label_path):
    with open(label_path, "r") as f:
        return [line.strip() for line in f.readlines()]


# Преобразование изображения в формат, который принимает модель
def preprocess_image(image_path, input_shape):
    img = PILImage.open(image_path).convert("RGB")
    img = img.resize((input_shape[1], input_shape[2]))
    img = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
    # img = np.array(img).astype(np.float32)  # / 255.0 Нормализация
    # img = np.expand_dims(img, axis=0)  # Добавляем batch размерность
    return img


class PredictMushroom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_path = os.path.join(os.getcwd(), "model.tflite")
        self.labels_path = os.path.join(os.getcwd(), "labels.txt")
        self.labels = load_labels(self.labels_path)
        self.image_path = None

        if platform == "android":
            self.model = TensorFlowModel()
            self.model.load(self.model_path)
            self.image_for_classification_path = os.path.join(
                primary_external_storage_path(), "DCIM/MushroomDetection/photos/1.jpg"
            )
        else:
            self.model = None
            self.image_for_classification_path = "photos/1.jpg"

    def on_enter(self):
        self.start_classification()

    def on_pre_leave(self):
        delete_image(self.image_for_classification_path)
        self.ids.image_display.source = (
            ""  # Для того, чтобы кнопка заработала, пришлось сделать так
        )
        # self.image.clear_widgets()
        # self.image.reload()

    def update_rect(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size

    def start_classification(self):
        threading.Thread(target=self.classify_image).start()

    def classify_image(self):
        input_shape = self.model.get_input_shape()
        img_array = preprocess_image(self.image_for_classification_path, input_shape)

        y = self.model.pred(img_array)  # Предсказываем изображение

        predicted_index_of_class = np.argmax(
            y
        )  # Определяем индекс самого релевантного класса

        predicted_class = self.labels[predicted_index_of_class]
        mushroom_name = f"Гриб {predicted_class}"

        mushroom_description = f"Гриб распознан с индексом {predicted_index_of_class}"
        self.image_path = os.path.join(
            os.getcwd(), f"mushroom_picture/{predicted_class}.jpg"
        )  # Нужно убедиться, что все хорошо с нумерацией, т.к картинки начинаются с 2
        db.save_mushroom(mushroom_name, self.image_path, mushroom_description)
        # Обновляем результат на экране
        Clock.schedule_once(
            lambda dt: self.update_result(f"Результат: {predicted_class}")
        )

    def update_result(self, text):
        self.result_label.text = text
        self.update_image()

    def update_image(self):
        self.image.source = self.image_path
        self.image.reload()

    def go_back(self, instance=None):
        self.manager.current = "main_page"
