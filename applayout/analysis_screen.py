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
from database import Database  # Импортируем функцию сохранения


db = Database()

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

        if platform == "android":
            self.model = TensorFlowModel()
            self.model.load(self.model_path)
            self.image_path = os.path.join(
                primary_external_storage_path(), "DCIM/MushroomDetection/photos/1.jpg"
            )
        else:
            self.model = None
            self.image_path = "photos/1.jpg"

        # Основной вертикальный layout
        self.layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        with self.layout.canvas.before:
            Color(0.26, 0.27, 0.33, 1)
            self.bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=self.update_rect, size=self.update_rect)

        # Увеличиваем область для фотографии (около 80% экрана)
        self.image = Image(size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.image)

        # Результирующая метка – чуть меньше по высоте (примерно 10% экрана)
        self.result_label = Label(
            text="Результат: Ожидание",
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.result_label)

        # Горизонтальный layout для кнопок (оставшиеся 10% экрана)
        button_box = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.15), spacing=dp(10)
        )

        # Кнопка "Назад" – аналогично, занимает вторую половину
        btn_back = RoundedButton(text="Назад", size_hint=(1, 1))
        btn_back.bind(on_press=self.go_back)
        button_box.add_widget(btn_back)

        self.layout.add_widget(button_box)
        self.add_widget(self.layout)

    def on_enter(self):
        self.update_image()
        self.start_classification(None)

    def on_pre_leave(self):
        # delete_image(self.image_path)
        self.image.clear_widgets()
        self.image.reload()

    def update_rect(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size

    def start_classification(self, instance):
        self.result_label.text = "Classifying image..."
        threading.Thread(target=self.classify_image).start()

    def classify_image(self):
        input_shape = self.model.get_input_shape()
        img_array = preprocess_image(self.image_path, input_shape)

        y = self.model.pred(img_array)  # Предсказываем изображение

        predicted_class = np.argmax(y)  # Определяем индекс самого релевантного класса
        try:
            class_label = self.labels[predicted_class]
        except IndexError:
            print("ERROR")
            print(self.labels)
        mushroom_name = f"Гриб {class_label}"

        mushroom_description = f"Гриб распознан с индексом {predicted_class}"
        db.save_mushroom(mushroom_name, self.image_path, mushroom_description)
        # Обновляем результат на экране
        Clock.schedule_once(lambda dt: self.update_result(f"Результат: {class_label}"))

    def update_result(self, text):
        self.result_label.text = text
        self.btn_recognize.disabled = True

    def update_image(self):
        self.image.source = self.image_path
        self.image.reload()

    def go_back(self, instance):
        self.manager.current = "main_page"
