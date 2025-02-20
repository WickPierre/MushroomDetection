from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from applayout.models import RoundedButton  # Импортируем наш кастомный виджет

Builder.load_string(
    """
#:import dp kivy.metrics.dp
#:import os os
#:import get_color_from_hex kivy.utils.get_color_from_hex

<RoundedButton>:
    font_size: self.height * 0.15

<MainPage>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
                source: os.path.join('icons', 'back_of_design.jpg')

        AnchorLayout:
            anchor_y: 'bottom'
            size_hint_y: 0.25
            Label:
                text: "Mushroom Detector"
                font_name: os.path.join('icons', 'srift.ttf')
                font_size: dp(36)
                size_hint: None, None
                size: self.texture_size
                halign: 'center'
                color: (1, 1, 1, 1)
                canvas.before:
                    Color:
                        rgba: (0, 0, 0, 0.5)
                    RoundedRectangle:
                        pos: (self.x - dp(10), self.y - dp(10))
                        size: (self.width + dp(20), self.height + dp(20))
                        radius: [20]

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
