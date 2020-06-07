import io
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as kivyImage
from kivy.core.image import Image as kivyCoreImage

from kivy_mongo.mongo import MongoDB, HOST_DB, PORT_DB


class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        self.button_previous_image = Button(text="<<")
        self.button_previous_image.bind(on_press=lambda a: self.previous_image())
        self.add_widget(self.button_previous_image)

        self.image = kivyImage()
        self.find_image('1.png')
        self.add_widget(self.image)

        self.button_next_img = Button(text=">>")
        self.button_next_img.bind(on_press=lambda a: self.next_img())
        self.add_widget(self.button_next_img)

        self.doctors_num = 1

        if self.doctors_num == 1:
            self.button_previous_image.disabled = True

    def find_image(self, img_name):
            image_bytes_data = MongoDB(HOST_DB, PORT_DB).get_image(img_name)

            data = io.BytesIO(image_bytes_data)

            img = kivyCoreImage(data, ext="png").texture
            self.image.texture = img

    def previous_image(self):
        self.doctors_num -= 1
        self.find_image(f'{self.doctors_num}.png')
        self.button_next_img.disabled = False

        if self.doctors_num == 1:
            self.button_previous_image.disabled = True

    def next_img(self):
        self.doctors_num += 1
        self.find_image(f'{self.doctors_num}.png')
        self.button_previous_image.disabled = False

        img_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if self.doctors_num == len(os.listdir(img_dir_path)):
            self.button_next_img.disabled = True


class BuildApp(App):
    def build(self):
        v_layout = BoxLayout(orientation='vertical')
        label_input_text = Label(text='Знакомьтесь: Доктор Кто и его первые четыре регенерации')
        v_layout.add_widget(label_input_text)
        v_layout.add_widget(MainApp())

        return v_layout


if __name__ == '__main__':
    BuildApp().run()
