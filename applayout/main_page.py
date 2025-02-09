from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from applayout.models import RoundedButton  # Импортируем наш кастомный виджет

Builder.load_string(
    """
#:import dp kivy.metrics.dp

<RoundedButton>:
    # Здесь можно задать дополнительные свойства,
    # не переопределяя логику отрисовки из Python.
    font_size: self.height * 0.15

<MainPage>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: (0.26, 0.27, 0.33, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        # Виджет для отступа сверху (30% высоты)
        Widget:
            size_hint_y: 0.3

        RoundedButton:
            text: "Распознать гриб"
            size_hint: (0.85, 0.15)
            pos_hint: {'center_x': 0.5}
            on_release: root.open_camera()

        RoundedButton:
            text: "История"
            size_hint: (0.85, 0.15)
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'history'

        RoundedButton:
            text: "Настройки"
            size_hint: (0.85, 0.15)
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'settings'
"""
)


class MainPage(Screen):
    def open_camera(self):
        self.manager.current = "camera"

    def go_to_history(self):
        self.manager.current = "history"

    def go_to_settings(self):
        self.manager.current = "settings"
