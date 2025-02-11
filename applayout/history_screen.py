from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from applayout.theme_manager import theme_manager
from kivy.utils import get_color_from_hex
import database as db


Builder.load_string(
    """
#:import os os
<HistoryScreen>:
    name: "history"
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.26, 0.27, 0.33, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "История сканирований"
            size_hint_y: None
            height: dp(40)
            font_size: "20sp"
            halign: "center"
            color: (1, 1, 1, 1)

        ScrollView:
            size_hint_y: 1
            BoxLayout:
                id: history_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)

        Button:
            text: "Назад"
            size_hint_y: None
            height: root.height * 0.1
            on_release: root.manager.current = "main_page"
            background_color: (0.26, 0.27, 0.33, 1)
            color: 1, 1, 1, 1

<MushroomDetailScreen>:
    name: "mushroom_detail"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.26, 0.27, 0.33, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            id: mushroom_title
            text: root.mushroom_title
            size_hint_y: None
            height: dp(40)
            font_size: "20sp"
            halign: "center"
            background_color: (0.26, 0.27, 0.33, 1)
            color: (1, 1, 1, 1)

        Image:
            id: mushroom_image
            source: os.path.join(os.getcwd(), root.mushroom_photo)
            size_hint_y: 0.5
            allow_stretch: True
            keep_ratio: True

        ScrollView:
            size_hint_y: 0.4
            Label:
                id: mushroom_description
                text: root.mushroom_description
                size_hint_y: None
                height: self.texture_size[1]
                font_size: "16sp"
                halign: "left"
                valign: "top"
                text_size: self.width, None
                background_color: (0.26, 0.27, 0.33, 1)
                color: (1, 1, 1, 1)

        Button:
            text: "Назад"
            size_hint_y: None
            height: dp(40)
            on_release: root.manager.current = "history"
            background_color: (0.26, 0.27, 0.33, 1)
            color: (1, 1, 1, 1)
"""
)


class HistoryCard(ButtonBehavior, BoxLayout):
    """Карточка для отображения краткой информации о грибе в истории."""

    def __init__(self, mushroom, **kwargs):
        super().__init__(**kwargs)
        self.mushroom_data = mushroom
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.spacing = dp(5)

        with self.canvas.before:
            Color(get_color_from_hex("#002137"))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Отображаем название гриба (с выделением) и дату сканирования
        self.add_widget(
            Label(
                text=f"[b]{mushroom.get('name', 'Без названия')}[/b]",
                markup=True,
                size_hint_y=None,
                height=dp(30),
                color=theme_manager.get("text_color"),
                halign="left",
                valign="middle",
                font_size="16sp",
            )
        )
        self.add_widget(
            Label(
                text=f"Дата сканирования: {mushroom.get('scan_date', '')}",
                size_hint_y=None,
                height=dp(20),
                color=theme_manager.get("text_color"),
                halign="left",
                valign="middle",
                font_size="14sp",
            )
        )

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_release(self):
        """При нажатии переходим на экран с детальной информацией о выбранном грибе."""
        # Импортируем класс экрана деталей, если он ещё не добавлен в ScreenManager
        # from applayout.history_screen import MushroomDetailScreen

        app = App.get_running_app()
        if not app.root.has_screen("mushroom_detail"):
            app.root.add_widget(MushroomDetailScreen(name="mushroom_detail"))
        detail_screen = app.root.get_screen("mushroom_detail")
        detail_screen.set_details(self.mushroom_data)
        app.root.current = "mushroom_detail"


class HistoryScreen(Screen):
    def on_pre_enter(self):
        """Обновляет список истории при входе на экран."""
        self.update_history()

    def update_history(self):
        history_list = self.ids.history_list
        history_list.clear_widgets()
        mushrooms = db.get_saved_mushrooms()
        for mushroom in mushrooms:
            history_list.add_widget(HistoryCard(mushroom=mushroom))


class MushroomDetailScreen(Screen):
    mushroom_title = StringProperty("")
    mushroom_description = StringProperty("")
    mushroom_photo = StringProperty("")

    def set_details(self, mushroom):
        """Устанавливает данные для детального отображения выбранного гриба."""
        self.mushroom_title = mushroom.get("name", "Без названия")
        self.mushroom_description = mushroom.get("description", "Описание отсутствует.")
        self.mushroom_photo = mushroom.get("image_path", "default_image.png")
