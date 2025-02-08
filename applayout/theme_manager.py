from kivy.utils import get_color_from_hex


class ThemeManager:
    def __init__(self):
        self._current_theme = "light"

        self._themes = {
            "light": {
                "background_color": get_color_from_hex("#FFFFFF"),
                "button_color": get_color_from_hex("#008000"),
                "text_color": get_color_from_hex("#00000"),
            },
            "dark": {
                "background_color": get_color_from_hex("#2c3e50"),
                "button_color": get_color_from_hex("#008000"),
                "text_color": get_color_from_hex("#FFFFFF"),
            },
        }

    def get(self, key):
        return self._themes[self._current_theme].get(key)

    def toggle_theme(self):
        self._current_theme = "dark" if self._current_theme == "light" else "light"


theme_manager = ThemeManager()
