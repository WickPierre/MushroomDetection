from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from android_permissions import AndroidPermissions
from applayout.camera_page import CameraScreen
from applayout.main_page import MainPage
from applayout.analysis_screen import PredictMushroom
from applayout.history_screen import HistoryScreen
from applayout.settings_screen import SettingsScreen
from applayout.theme_manager import theme_manager
import os

if platform == "android":
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity

    View = autoclass("android.view.View")

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        if Window.width > Window.height:
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)

elif platform != "ios":
    from kivy.config import Config

    Config.set("input", "mouse", "mouse, disable_multitouch")


class MyApp(App):

    theme = theme_manager

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainPage(name="main_page"))
        self.sm.add_widget(CameraScreen(name="camera"))
        self.sm.add_widget(PredictMushroom(name="analysis"))
        self.sm.add_widget(HistoryScreen(name="history"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        if platform == "android":
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None


if __name__ == "__main__":
    MyApp().run()
