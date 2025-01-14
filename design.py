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


Window.clearcolor = get_color_from_hex("#1e1e1e")


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


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=20, padding=[10, 20, 10, 20])

        camera_box = BoxLayout(size_hint=(1, 0.8), padding=0)
        self.camera = Camera(play=True)

        with camera_box.canvas.before:
            Color(*get_color_from_hex("#2d2d2d"))
            self.camera_frame = RoundedRectangle(radius=[10])

        camera_box.add_widget(self.camera)
        self.camera.bind(pos=self.update_camera_frame, size=self.update_camera_frame)
        layout.add_widget(camera_box)

        self.button = RoundedButton(text="Сделать фото")
        self.button.bind(on_press=self.take_photo)

        button_container = BoxLayout(size_hint=(1, 0.1), padding=10, spacing=10)
        button_container.add_widget(self.button)
        layout.add_widget(button_container)

        self.result_label = Label(
            text="",
            font_size="14sp",
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
            text_size=(Window.width * 0.9, None),
            color=get_color_from_hex("#ffffff"),
        )
        layout.add_widget(self.result_label)

        self.add_widget(layout)

        self.model = YOLO("best.pt")

    def update_camera_frame(self, *args):
        self.camera_frame.size = self.camera.size
        self.camera_frame.pos = self.camera.pos

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

        for result in results:
            result.save_txt("output.txt")

        processed_filename = os.path.join(
            "processed_photos",
            f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        )

        result = results[0]
        annotated_frame = result.plot()
        cv2.imwrite(processed_filename, annotated_frame)
        with open("output.txt", "r") as file:
            file = file.readline()
            self.result_label.text = str(file.strip())
            with open("output.txt", "w") as file:
                file.write("")


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name="main")

        self.sm.add_widget(self.main_screen)
        self.sm.current = "main"

        return self.sm


if __name__ == "__main__":
    MyApp().run()
