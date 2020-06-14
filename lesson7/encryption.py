""" Сделать программу, которая шифрует введенный текст. """

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyEncryptionWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='Введите сообщение'))

        self.add_widget(Label(text='Зашифрованное сообщение'))

        box = BoxLayout(orientation='vertical')
        self.input_text = TextInput(font_size=20,
                                    # size_hint_y=None,
                                    # height=100
                                    )
        box.add_widget(self.input_text)
        box.add_widget(Button(text='Подтвердить',
                              on_press=lambda x: self.pass_encryption_text()))
        self.add_widget(box)

        self.output_text = Label()
        self.add_widget(self.output_text)

    def pass_encryption_text(self):
        default_text = self.input_text.text
        reversed_text = ''.join(reversed(default_text))
        encryption_text = ''

        for letter in reversed_text:
            if letter.lower() == 'z':
                encryption_text += chr(97)
            else:
                encryption_text += chr(ord(letter.lower()) + 1)

        self.output_text.text = encryption_text


class MyPaintApp(App):
    def build(self):
        return MyEncryptionWidget()


if __name__ == '__main__':
    MyPaintApp().run()
