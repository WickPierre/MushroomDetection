from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, Label


class MainPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        open_camera_button = Button(
            text='Распознать гриб',
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        open_camera_button.bind(on_press=self.open_camera)
        self.text_label = Label(
            size_hint=(1, None),
        )

        layout.add_widget(open_camera_button)
        layout.add_widget(self.text_label)
        self.add_widget(layout)

    def open_camera(self, instance):
        self.manager.current = 'camera_page'
