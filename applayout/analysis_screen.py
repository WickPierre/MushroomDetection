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
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import os os
<PredictMushroom>:
    name: "predict_mushroom"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
                source: os.path.join('icons', 'back_of_design.jpg')

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
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.8  # Белый фон с прозрачностью
                Rectangle:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            orientation: "vertical"
            size_hint: (1, 0.2)
            spacing: dp(5)
            
            RoundedButton:
                text: "Назад"
                size_hint: (0.85, 0.05)
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
        input = ByteBuffer.wrap(x.tobytes())
        output = TensorBuffer.createFixedSize(self.output_shape, self.output_type)
        self.interpreter.run(input, output.getBuffer().rewind())
        return np.reshape(np.array(output.getFloatArray()), self.output_shape)


def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Файл {image_path} успешно удален.")
    else:
        print(f"Файл {image_path} не существует.")


def load_labels(label_path):
    with open(label_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def preprocess_image(image_path, input_shape):
    img = PILImage.open(image_path).convert("RGB")
    img = img.resize((input_shape[1], input_shape[2]))
    img = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
    return img


class PredictMushroom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_path = os.path.join(os.getcwd(), "model.tflite")
        self.labels_path = os.path.join(os.getcwd(), "mushroom_names.txt")
        self.labels = load_labels(self.labels_path)
        self.image_path = None
        self.highlight_color = (1, 1, 1, 1)  # Белый по умолчанию

        self.edible = {
            "Грушевидный_дождевик",
            "Опёнок_северный",
            "Белый_гриб",
            "Боровик_сетчатый",
            "Лисичка_обыкновенная",
            "Опёнок_зимний",
            "Польский_гриб",
            "Опёнок_летний",
            "Рыжик_настоящий",
            "Волнушка_розовая",
            "Груздь_перечный",
            "Подосиновик_белоножковый",
            "Подосиновик_красный",
            "Подберёзовик_обыкновенный",
            "Подосиновик_жёлто-бурый",
            "Дождевик_жемчужный",
            "Гриб-зонтик_пёстрый",
            "Вёшенка_обыкновенная",
            "Вёшенка_лёгочная",
            "Маслёнок_зернистый",
            "Маслёнок_лиственничный",
            "Маслёнок_обыкновенный",
        }

        self.poisonous = {
            "Мухомор_поганковидный",
            "Мухомор_красный",
            "Мухомор_пантерный",
            "Мухомор_серо-розовый",
            "Трутовик_чешуйчатый",
            "Говорушка_дымчатая",
            "Кольтриция_многолетняя",
            "Навозник_рассеянный",
            "Навозник_мерцающий",
            "Навозник_серый",
            "Навозник_белый",
            "Дедалеопсис_бугристый",
            "Дедалеопсис_трёхцветный",
            "Трутовик_настоящий",
            "Трутовик_берёзовый",
            "Трутовик_окаймлённый",
            "Трутовик_плоский",
            "Строчок_обыкновенный",
            "Строчок_гигантский",
            "Строчок_остроконечный",
            "Ложная_лисичка",
            "Ложноопёнок_серно-жёлтый",
            "Ложноопёнок_кирпично-красный",
            "Трутовик_серно-жёлтый",
            "Леписта_голая",
            "Мерулиус_дрожащий",
            "Мутинус_Равенеля",
            "Панеллюс_вяжущий",
            "Свинушка_тонкая",
            "Весёлка_обыкновенная",
            "Трутовик_ложный",
            "Трутовик_осиновый",
            "Чешуйчатка_золотистая",
            "Чешуйчатка_обыкновенная",
            "Саркодонция_поздняя",
            "Саркосцифа_австрийская",
            "Саркосома_шаровидная",
            "Строфария_сине-зелёная",
            "Траметес_жёстковолосистый",
            "Траметес_охряный",
            "Траметес_разноцветный",
            "Дрожалка_оранжевая",
            "Трихаптум_двуформенный",
            "Рядовка_жёлто-красная",
            "Урнула_кратеровидная",
            "Сморчковая_шапочка",
        }

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
        self.ids.image_display.source = ""
        self.highlight_color = (1, 1, 1, 1)  # Сброс цвета

    def start_classification(self):
        threading.Thread(target=self.classify_image).start()

    def classify_image(self):
        try:
            input_shape = self.model.get_input_shape()
            img_array = preprocess_image(
                self.image_for_classification_path, input_shape
            )
            y = self.model.pred(img_array)
            predicted_index = np.argmax(y)

            if max(y[0]) < 0.3:
                predicted_class = "Гриб не распознан. Убедитесь, что он чётко виден!"
                self.image_path = os.path.join(
                    os.getcwd(), "mushroom_picture/nothing.jpg"
                )
                self.highlight_color = (1, 1, 0, 0.3)  # Желтый для неопределенности
            else:
                predicted_class = self.labels[predicted_index]
                self.image_path = os.path.join(
                    os.getcwd(), f"mushroom_picture/{predicted_class}.jpg"
                )
                db.save_mushroom_scan(predicted_class)

                # Определение цвета
                if predicted_class in self.edible:
                    self.highlight_color = (0, 1, 0, 0.3)  # Зеленый
                elif predicted_class in self.poisonous:
                    self.highlight_color = (1, 0, 0, 0.3)  # Красный
                else:
                    self.highlight_color = (1, 1, 1, 0.3)  # Светло-серый

            Clock.schedule_once(
                lambda dt: self.update_result(f"Результат: {predicted_class}")
            )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.update_result(f"Ошибка классификации: {str(e)}")
            )

    def update_result(self, text):
        self.ids.result_label.text = text
        self.update_background()
        self.update_image()
        # Привязка к изменениям размера/позиции
        self.ids.result_label.bind(
            pos=self.update_background, size=self.update_background
        )

    def update_background(self, *args):
        self.ids.result_label.canvas.before.clear()
        with self.ids.result_label.canvas.before:
            Color(*self.highlight_color)
            Rectangle(pos=self.ids.result_label.pos, size=self.ids.result_label.size)

    def update_image(self):
        self.ids.image_display.source = self.image_path
        self.ids.image_display.reload()

    def go_back(self, instance=None):
        self.manager.current = "main_page"
