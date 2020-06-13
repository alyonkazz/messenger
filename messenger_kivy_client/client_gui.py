# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
import ast
import sys
from datetime import datetime

from kivy.app import App

# The PageLayout class is used to create
# a simple multi-page layout,
# in a way that allows easy flipping from
# one page to another using borders.
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout

# creates the button in kivy
# if not imported shows the error
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from client_contacts import RVClientContacts, SelectableLabel


selected_id = ''


class SettingsImageButton(ButtonBehavior, Image):
    def on_press(self):
        print('settings')
        set_screen('client_settings')


class ClientSettings(Screen):
    def __init__(self, **kwargs):
        super(ClientSettings, self).__init__(**kwargs)

        box = BoxLayout(orientation='vertical')
        self.add_widget(box)

        # TODO add settings

        self.tmp_label = Label(text='Здесь будут настройки')
        box.add_widget(self.tmp_label)

        # TODO add carousel/swipe
        self.btn_back = Button(text='Назад',
                               on_press=lambda x: set_screen('menu_contacts')
                               )
        box.add_widget(self.btn_back)


class ClientSummaryInfo(BoxLayout):
    def __init__(self, **kwargs):
        super(ClientSummaryInfo, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.size = (Window.width, 120)
        self.size_hint = (None, None)
        self.padding = (0, 10)

        self.add_widget(SettingsImageButton(source='static/settings.png',
                                            size=(50, 50),
                                            size_hint=(None, None),
                                            # size_hint=(.2, .2),
                                            pos_hint={'center_x': .7, 'center_y': .5}
                                            ))

        self.avatar = Image(source='static/default_avatar.jpg',
                            size_hint=(None, None),
                            )
        self.add_widget(self.avatar)

        # TODO add status
        self.status = Label(text='Это статус',
                            pos_hint={'center_y': 1},
                            padding=(10, 10)
                            )
        self.status.bind(size=self.status.setter('text_size'))
        self.add_widget(self.status)


class ClientContacts(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PageMenuContacts(Screen):
    """
    Define class PageLayout here
    """

    def __init__(self, **kwargs):
        # The super function in Python can be
        # used to gain access to inherited methods
        # which is either from a parent or sibling class.
        super(PageMenuContacts, self).__init__(**kwargs)

        self.layout = BoxLayout()

        # page 1
        page1_box = BoxLayout(orientation="vertical")
        self.layout.add_widget(page1_box)

        page1_box.add_widget(ClientSummaryInfo())

        self.client_list = ['cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3',
                            'cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3']

        self.client_contacts = RecycleView()
        page1_box.add_widget(self.client_contacts)

        self.client_contacts_layout = GridLayout(cols=1, size_hint_y=None)
        self.client_contacts_layout.bind(minimum_height=self.client_contacts_layout.setter('height'),
                                         )
        self.client_contacts.add_widget(self.client_contacts_layout)

        for i in self.client_list:
            self.client_contacts_layout.add_widget(ClientButton(text=str(i),
                                                                id=str(i),
                                                                size_hint_y=None,
                                                                height=dp(40),
                                                                # on_press=
                                                                ))




        self.add_widget(self.layout)


class SelectedButton(Button):
    def __init__(self, selected_id_,**kwargs):
        super().__init__(**kwargs)

        # self.size_hint_y = None
        self.text = selected_id_


class ClientButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.size_hint_y = None
        # self.height = 40

    def on_press(self):
        print(self.text)


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(PageMenuContacts(name='menu_contacts'))
sm.add_widget(ClientSettings(name='client_settings'))


# creating the App class
class PageLayoutApp(App):
    """
    App class here
    """

    def build(self):
        """
        build function here
        """
        return sm


# Run the App
if __name__ == '__main__':
    PageLayoutApp().run()
