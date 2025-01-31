from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from android_permissions import AndroidPermissions
from applayout.camera_page import PhotoScreen1
from applayout.main_page import MainPage
from predict_page import PredictMushroom


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse, disable_multitouch')


class MyApp(App):
    def build(self):
        self.enable_swipe = False
        self.sm = ScreenManager()
        self.sm.add_widget(MainPage(name='main_page'))
        self.sm.add_widget(PhotoScreen1(name='camera_page'))
        self.sm.add_widget(PredictMushroom(name='predict_mushroom'))
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None


if __name__ == '__main__':
    MyApp().run()