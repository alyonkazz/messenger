from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<ScreenRegistration>:
    name: 'registration'
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: None
            height: dp(40)
            text: 'Введите имя'
        TextInput:
            size_hint_y: None
            height: dp(40)
            text: app.data
            on_text: app.data = self.text
        Label:
            size_hint_y: None
            height: dp(40)
            text: 'Введите пароль'
        TextInput:
            size_hint_y: None
            height: dp(40)
            text: app.data
            on_text: app.data = self.text
        Label:
            size_hint_y: None
            height: dp(40)
            text: 'Введите пароль повторно'
        TextInput:
            size_hint_y: None
            height: dp(40)
            text: app.data
            on_text: app.data = self.text
        Button:
            text: 'Подключиться'
            on_press: app.root.ids['manager'].current = 'client_contacts'
''')


class ScreenRegistration(Screen):
    """ registration screen """


class TestThisApp(App):
    data = StringProperty('initial text')

    def build(self):
        return ScreenRegistration()


if __name__ == "__main__":
    TestThisApp().run()
