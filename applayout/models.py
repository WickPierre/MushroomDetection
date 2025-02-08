from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex


class RoundedButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = kwargs.get("padding", [20, 10])
        self.font_size = kwargs.get("font_size", "24sp")
        self.size_hint = kwargs.get("size_hint", (None, None))
        self.size = kwargs.get("size", (240, 100))
        self.halign = kwargs.get("halign", "center")
        self.valign = kwargs.get("valign", "middle")
        self.color = kwargs.get("color", get_color_from_hex("#ffffff"))
        bg_color = kwargs.get("background_color", get_color_from_hex("#008000"))
        radius = kwargs.get("radius", [30])
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(radius=radius, size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MushroomCard(BoxLayout):
    def __init__(self, name, date, image_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = 15
        self.padding = [10, 5]
        self.size_hint_y = None
        self.height = 100

        # Изображение гриба
        img = Image(
            source=image_path, size_hint=(None, 1), width=80, allow_stretch=True
        )
        self.add_widget(img)

        # Текстовая информация
        text_box = BoxLayout(orientation="vertical")
        text_box.add_widget(
            Label(text=name, font_size="16sp", halign="left", bold=True)
        )
        text_box.add_widget(
            Label(text=date, font_size="12sp", color=get_color_from_hex("#666666"))
        )
        self.add_widget(text_box)

        # Кнопка удаления заменена на RoundedButton с нужными параметрами:
        btn_delete = RoundedButton(
            text="×",
            font_size="24sp",
            size_hint=(None, None),
            size=(50, 50),
            color=get_color_from_hex("#ff0000"),
            padding=[0, 0],
            background_color=get_color_from_hex("#444444"),
            radius=[25],  # Радиус выбран так, чтобы кнопка выглядела округло
        )
        btn_delete.bind(on_release=lambda x: self.delete_card())
        self.add_widget(btn_delete)

    def delete_card(self):
        # Метод для удаления карточки
        if self.parent:
            self.parent.remove_widget(self)
