from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from datetime import datetime
import os
import cv2
from ultralytics import YOLO

Window.clearcolor = get_color_from_hex("#000000")


class RoundedButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = [20, 10]
        self.font_size = "16sp"
        self.size_hint = (None, None)
        self.size = (240, 60)
        self.halign = "center"
        self.valign = "middle"
        self.text_size = self.size
        self.color = get_color_from_hex("#ffffff")
        with self.canvas.before:
            Color(*get_color_from_hex("#444444"))
            self.rect = RoundedRectangle(radius=[30], size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MainMenuScreen(Screen):  # Первый экран, пока что с 2 кнопками
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        history_button = RoundedButton(text="История распознавания")
        recognize_button = RoundedButton(text="Распознать гриб")

        recognize_button.bind(on_press=self.go_to_camera)

        layout.add_widget(history_button)
        layout.add_widget(recognize_button)

        self.add_widget(layout)

    def go_to_camera(self, instance):
        self.manager.current = "camera"


class CameraScreen(Screen):  # Второй экран, камера + сделать фото
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        self.camera = Camera(play=True)
        layout.add_widget(self.camera)

        button_container = BoxLayout(size_hint=(1, 0.1), padding=10)
        self.capture_button = RoundedButton(text="Сфотографировать")
        self.capture_button.bind(on_press=self.take_photo)
        button_container.add_widget(self.capture_button)

        layout.add_widget(button_container)
        self.add_widget(layout)

        self.model = YOLO("/Users/petrlutkin/Desktop/MushroomDetection/result/train2/weights/best.pt")

    def take_photo(self, instance):
        if not os.path.exists("photos"):
            os.makedirs("photos")
        if not os.path.exists("processed_photos"):
            os.makedirs("processed_photos")

        filename = os.path.join(
            "photos", f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        self.camera.export_to_png(filename)

        results = self.model.predict(source=filename, save=False, save_txt=False)

        processed_filename = os.path.join(
            "processed_photos",
            f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        )
        with open("output.txt", "w") as file:
            file.write("")
        for result in results:
            result.save_txt("output.txt")

        result = results[0]
        annotated_frame = result.plot()
        cv2.imwrite(processed_filename, annotated_frame)

        self.manager.current = "results"


class ResultsScreen(
    Screen
):  # Чисто наброски, кнопка вернуться к фотографированию и вывод информации от нейронки
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        self.result_label = Label(
            text="",
            font_size="16sp",
            size_hint=(1, 0.8),
            halign="center",
            valign="middle",
            color=get_color_from_hex("#ffffff"),
        )
        layout.add_widget(self.result_label)

        back_button = RoundedButton(text="Сфотографировать еще раз")
        back_button.bind(on_press=self.go_back_to_camera)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        try:
            with open("output.txt", "r") as file:
                self.result_label.text = file.read().strip()
        except FileNotFoundError:
            self.result_label.text = "Результаты не найдены."

    def go_back_to_camera(self, instance):
        self.manager.current = "camera"


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.sm.add_widget(MainMenuScreen(name="menu"))
        self.sm.add_widget(CameraScreen(name="camera"))
        self.sm.add_widget(ResultsScreen(name="results"))

        self.sm.current = "menu"

        return self.sm


if __name__ == "__main__":
    MyApp().run()
