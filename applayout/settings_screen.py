from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from applayout.models import RoundedButton
import database as db  # Импортируем функцию очистки истории


Builder.load_string(
    """
    #:import os os
<SettingsScreen>:
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
            source: os.path.join('icons', 'back_of_design.jpg')

    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"
        BoxLayout:
            orientation: "vertical"
            size_hint: (None, None)
            width: root.width * 0.8
            height: root.height * 0.35
            spacing: dp(20)
            
            RoundedButton:
                text: "Очистить историю"
                size_hint: (None, None)
                width: root.width * 0.8
                height: root.height * 0.15
                on_release: root.clear_history()
            RoundedButton:
                text: "Назад"
                size_hint: (None, None)
                width: root.width * 0.8
                height: root.height * 0.15
                on_release: root.manager.current = 'main_page'
"""
)


class SettingsScreen(Screen):
    def clear_history(self):
        # Очищает историю сканирований в базе данных.
        db.clear_history()
        print("История сканирований очищена")
