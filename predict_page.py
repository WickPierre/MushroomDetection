import threading
import numpy as np
import os
from kivy.utils import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from PIL import Image as PILImage


if platform == 'android':
    from android.storage import primary_external_storage_path
    from jnius import autoclass

    File = autoclass('java.io.File')
    Interpreter = autoclass('org.tensorflow.lite.Interpreter')
    InterpreterOptions = autoclass('org.tensorflow.lite.Interpreter$Options')
    Tensor = autoclass('org.tensorflow.lite.Tensor')
    DataType = autoclass('org.tensorflow.lite.DataType')
    TensorBuffer = autoclass(
        'org.tensorflow.lite.support.tensorbuffer.TensorBuffer')
    ByteBuffer = autoclass('java.nio.ByteBuffer')
else:
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter


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
    img = PILImage.open(image_path).convert('RGB')
    img = img.resize((input_shape[1], input_shape[2]))
    img = np.array(img).astype(np.float32) # / 255.0 Нормализация
    # img = np.expand_dims(img, axis=0)  # Добавляем batch размерность
    return img


class TensorFlowModel():
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
        # assumes one input and one output for now
        input = ByteBuffer.wrap(x.tobytes())
        output = TensorBuffer.createFixedSize(self.output_shape,
                                              self.output_type)
        self.interpreter.run(input, output.getBuffer().rewind())
        return np.reshape(np.array(output.getFloatArray()),
                          self.output_shape)


class PredictMushroom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_path = os.path.join(os.getcwd(), 'model/model.tflite')
        self.labels_path = os.path.join(os.getcwd(), 'labels.txt')

        if platform == 'android':
            self.model = TensorFlowModel()
            self.model.load(self.model_path)
            self.image_path = os.path.join(primary_external_storage_path(), 'DCIM/MushroomDetection/photos/1.jpg')
        else:
            self.model = None
            self.image_path = 'photos/1.jpg'

        self.labels = load_labels(self.labels_path)

        self.layout = BoxLayout(orientation='vertical')

        self.image = Image()
        self.layout.add_widget(self.image)

        # Поле для текста
        self.result_label = TextInput(text='', readonly=True, size_hint=(1, 0.7))
        self.layout.add_widget(self.result_label)

        # Кнопка для распознавания
        btn_recognize = Button(text='Распознать', size_hint=(1, 0.15))
        btn_recognize.bind(on_press=self.start_classification)
        self.layout.add_widget(btn_recognize)

        # Кнопка для возврата на главный экран
        btn_back = Button(text='Назад', size_hint=(1, 0.15))
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_image()

    def start_classification(self, instance):
        self.result_label.text = "Classifying image..."
        threading.Thread(target=self.classify_image).start()

    def classify_image(self):
        input_shape = self.model.get_input_shape()
        img_array = preprocess_image(self.image_path, input_shape)

        y = self.model.pred(img_array)  # Predict img

        predicted_class = np.argmax(y)
        class_label = self.labels[predicted_class]
        Clock.schedule_once(lambda dt: self.update_result(class_label))

    def update_result(self, text):
        self.result_label.text = f"Результат: {text}"

    def update_image(self):
        self.image.source = self.image_path
        self.image.reload()

    def go_back(self, instance):
        delete_image(self.image_path)
        self.manager.current = 'main_page'
