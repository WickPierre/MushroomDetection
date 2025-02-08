from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty, ColorProperty, StringProperty
from kivy.clock import Clock
from kivy.metrics import dp
from camera4kivy import Preview
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from datetime import datetime
import os
from applayout.toast import Toast

Builder.load_string(
    """
#:import dp kivy.metrics.dp
<CameraScreen>:
    photo_preview: preview
    FloatLayout:
        # Чёрный фон всего экрана
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # Камера без изменений
        Preview:
            id: preview
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}

        # Кнопка "Назад" – снизу слева, круглая красная с двойной обводкой
        Button:
            text: "Назад"
            size_hint: None, None
            size: dp(70), dp(70)  # увеличенные размеры
            pos_hint: {"x": 0.05, "y": 0.05}
            on_release: root.manager.current = "main_page"
            background_normal: ""
            background_color: 0, 0, 0, 0
            canvas.before:
                # Красный фон кнопки
                Color:
                    rgba: 0, 0, 0, 1
                Ellipse:
                    pos: self.pos
                    size: self.size
            canvas.after:
                # Первая, чёрная обводка
                Color:
                    rgba: 0, 0, 0, 1
                Line:
                    ellipse: (self.x, self.y, self.width, self.height)
                    width: 3
                # Внешняя, небольшая серая обводка
                Color:
                    rgba: 0.5, 0.5, 0.5, 1
                Line:
                    ellipse: (self.x - dp(1), self.y - dp(1), self.width + dp(2), self.height + dp(2))
                    width: 3
            color: 1, 1, 1, 1
            font_size: dp(16)

        # Кнопка "Сделать фото" – снизу по центру, увеличенная, без текста, с двойной обводкой
        Button:
            text: ""
            size_hint: None, None
            size: dp(90), dp(90)  # увеличенные размеры
            pos_hint: {"center_x": 0.5, "y": 0.03}
            on_release: root.capture_photo()
            background_normal: ""
            background_color: 0, 0, 0, 0
            canvas.before:
                # Белый фон кнопки
                Color:
                    rgba: 1, 1, 1, 1
                Ellipse:
                    pos: self.pos
                    size: self.size
            canvas.after:
                # Первая, чёрная обводка
                Color:
                    rgba: 0, 0, 0, 1
                Line:
                    ellipse: (self.x, self.y, self.width, self.height)
                    width: 5
                # Внешняя, небольшая серая обводка
                Color:
                    rgba: 0.5, 0.5, 0.5, 1
                Line:
                    ellipse: (self.x - dp(1), self.y - dp(1), self.width + dp(2), self.height + dp(2))
                    width: 2

        # Кнопка "Перевернуть камеру" – снизу справа, увеличенная, с изображением, обрезанным по контуру кнопки и двойной обводкой
        Button:
            size_hint: None, None
            size: dp(70), dp(70)  # увеличенные размеры
            pos_hint: {"right": 0.95, "y": 0.05}
            on_release: root.select_camera("toggle")
            background_normal: ""
            background_color: 0, 0, 0, 0
            canvas.before:
                # Черный круг – фон кнопки
                Color:
                    rgba: 0, 0, 0, 1
                Ellipse:
                    pos: self.pos
                    size: self.size
            canvas:
                # Используем stencil для обрезки изображения по форме круга
                StencilPush
                Ellipse:
                    pos: self.pos
                    size: self.size
                StencilUse
                Rectangle:
                    source:  'icons/camera_flip.png'
                    # Уменьшаем размер изображения на 10 единиц, отступ по 5 единиц с каждой стороны:
                    pos: (self.x + dp(5), self.y + dp(5))
                    size: (self.width - dp(10), self.height - dp(10))
                StencilUnUse
                Ellipse:
                    pos: self.pos
                    size: self.size
                StencilPop
            canvas.after:
                # Первая, чёрная обводка
                Color:
                    rgba: 0, 0, 0, 1
                Line:
                    ellipse: (self.x, self.y, self.width, self.height)
                    width: 3
                # Внешняя, небольшая серая обводка
                Color:
                    rgba: 0.5, 0.5, 0.5, 1
                Line:
                    ellipse: (self.x - dp(1), self.y - dp(1), self.width + dp(2), self.height + dp(2))
                    width: 3
    """
)


class CameraScreen(Screen):
    photo_preview = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.photo_preview.connect_camera(filepath_callback=self.open_pred)

    def on_pre_leave(self):
        self.photo_preview.disconnect_camera()

    def select_camera(self, facing):
        self.photo_preview.select_camera(facing)

    def capture_photo(self):
        self.photo_preview.capture_photo(location=".", subdir="photos", name="1")

    def open_pred(self, file_path):
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "analysis"), 0)
