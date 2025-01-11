from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from datetime import datetime
import os
import cv2
from ultralytics import YOLO


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.camera = Camera(play=True)
        # self.camera.size = (640, 480) # размер камеры, у меня работает 640 480 в базе
        layout.add_widget(self.camera)

        self.button = Button(text="Сделать фото", size_hint=(1, 0.2))
        self.button.bind(on_press=self.take_photo)
        layout.add_widget(self.button)

        self.result_label = Label(
            text="", size_hint=(1, 0.2)
        )  # Нужно ввести итоговый результат в эту строку
        layout.add_widget(self.result_label)

        self.add_widget(layout)

        self.model = YOLO("best.pt")

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

        result = results[0]
        annotated_frame = result.plot()
        cv2.imwrite(processed_filename, annotated_frame)


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name="main")

        self.sm.add_widget(self.main_screen)
        self.sm.current = "main"

        return self.sm


if __name__ == "__main__":
    MyApp().run()
