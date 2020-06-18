from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<ScreenSetting>:
    name: 'client_settings'
    BoxLayout:
        Label:
            text: 'Здесь будут настройки'
        Button:
            text: '<< в список контактов'
            on_press: app.root.ids['manager'].current = 'client_contacts'
""")


class ScreenSetting(Screen):
    """ screen settings """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SettingScreen(App):

    def build(self):
        return ScreenSetting()


if __name__ == "__main__":
    SettingScreen().run()
