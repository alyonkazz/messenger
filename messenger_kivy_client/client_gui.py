# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
import sys

from kivy.app import App

# The PageLayout class is used to create
# a simple multi-page layout,
# in a way that allows easy flipping from
# one page to another using borders.
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout

# creates the button in kivy
# if not imported shows the error
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


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

        self.tmp_lable = Label(text='Здесь будут настройки')
        box.add_widget(self.tmp_lable)

        # TODO add carousel/swipe
        self.btn_back = Button(text='Назад',
                               on_press=lambda x: set_screen('menu_contacts')
                               )
        box.add_widget(self.btn_back)


class ClientSummaryInfo(BoxLayout):
    def __init__(self, **kwargs):
        super(ClientSummaryInfo, self).__init__(**kwargs)
        self.orientation = "horizontal"

        self.add_widget(SettingsImageButton(source='static/settings.png',
                                            size=(50, 50),
                                            size_hint=(None, None),
                                            # size_hint=(.2, .2),
                                            pos_hint={'center_x': .7, 'center_y': .5}
                                            ))

        self.avatar = Image(source='default_avatar.jpg',
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


class ClientContacts(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.add_widget(ClientSummaryInfo())

        self.image = Image(source='default_avatar.jpg', size=(100, 10), size_hint=(.7, 2))
        self.add_widget(self.image)

        self.label = Label(text='khlkhh')
        self.add_widget(self.label)

        b1 = Button(size_hint=(.2, .2),
                    pos_hint={'center_x': .7, 'center_y': .5},
                    text="pos_hint")

        # creating button
        # size of button is 20 % by hight and 50 % width of layout
        b2 = Button(size_hint=(.5, .2),
                    text="size_hint")

        # creating button
        # size of button is 20 % by hight and width of layout
        # position is 200, 200 from bottom left
        b3 = Button(size_hint=(.2, .2),
                    pos=(200, 200),
                    text="pos")

        # adding button to widget
        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)


class PageMenuContacts(Screen):
    """
    Define class PageLayout here
    """

    def __init__(self, **kwargs):
        # The super function in Python can be
        # used to gain access to inherited methods
        # which is either from a parent or sibling class.
        super(PageMenuContacts, self).__init__(**kwargs)

        self.layout = PageLayout()

        # creating buttons on diffent pages
        page1 = ClientContacts()

        btn2 = Button(text='Page 2')

        btn3 = Button(text='Page 3')

        # adding button on the screen
        # by add widget method
        self.layout.add_widget(page1)

        self.layout.add_widget(btn2)

        self.layout.add_widget(btn3)

        self.add_widget(self.layout)


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
