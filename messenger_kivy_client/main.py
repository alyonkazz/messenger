from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from chat_window_msgs import ChatWithContact
from screen_registration import ScreenRegistration
from screen_settings import ScreenSetting
from client_database.client_database import DBController

kv = """
<SettingsImageButton>:
    source: 'static/settings.png'
    size: (50, 50)
    size_hint: (None, None)
    pos_hint: {'center_x': .7, 'center_y': .5}
    
<ClientSummaryLayout>:
    size_hint_y: None
    height: 100
    SettingsImageButton:
        on_press: app.root.ids['manager'].current = 'client_settings'
    Image:
        source: 'static/default_avatar.jpg'
        size_hint: (None, None)
    Status:
        text: 'Это статус'
        pos_hint: {'center_y': 1}
        padding: (10, 10)

<ClientContactsRowButton>:
    size_hint_y: None
    height: dp(40)
    opacity: 0.3
    on_press: app.root.ids['selected_contact'].text = 'Чат с контактом ' + self.text
    on_press: app.root.ids['manager'].current = 'chat_window'
    
<ClientContacts>:
    viewclass: 'ClientContactsRowButton'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False   

RootLayout:
    orientation: 'vertical'
    ScreenManager:
        id: manager
        Screen:
            name: 'login'
            BoxLayout:
                orientation: 'vertical'
                Label:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Введите IP-адрес'
                TextInput:
                    size_hint_y: None
                    height: dp(40)
                    text: '127.0.0.1'
                    # on_text: app.data = self.text
                Label:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Введите порт'
                TextInput:
                    size_hint_y: None
                    height: dp(40)
                    text: '7777'
                    # on_text: app.data = self.text
                Label:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Введите имя'
                TextInput:
                    id: client_name
                    size_hint_y: None
                    height: dp(40)
                    text: app.client_name
                    on_text: app.client_name = self.text
                Label:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Введите пароль'
                TextInput:
                    size_hint_y: None
                    height: dp(40)
                    text: app.data
                    on_text: app.data = self.text
                Button:
                    text: 'Подключиться'
                    on_press: app.connect_to_db()
                    on_press: manager.current = 'client_contacts'
                    on_release: rv.data = [{'text': str(x)} for x in app.client_list]
                Button:
                    text: 'Зарегистрироваться'
                    on_press: manager.current = 'registration'
        ScreenRegistration:
        Screen:
            name: 'client_contacts'
            BoxLayout:
                orientation: 'vertical'
                ClientSummaryLayout:
                TextInput:
                    size_hint_y: None
                    height: dp(40)
                    text: app.data
                    on_text: app.data = self.text
                # Button:
                #     on_press: rv.data = [{'text': str(x)} for x in app.client_list]
                ClientContacts:
                    id: rv
                    data: [{'text': str(x)} for x in app.client_list]
        Screen:
            name: 'chat_window'
            BoxLayout:
                orientation: 'vertical'
                ClientSummaryLayout:
                Button:
                    size_hint_y: None
                    height: dp(40)
                    background_color: [1, 0.517, 0.705, 1]
                    text: '<< в список контактов'
                    on_press: manager.current = 'client_contacts'
                Label:
                    id: selected_contact
                    size_hint_y: None
                    height: dp(40)
                ChatWithContact:
                TextInput:
                    size_hint_y: None
                    height: self.minimum_height
                    text: app.data
                    on_text: app.data = self.text
                Button:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Отправить'
                    # TODO add send
                    on_press:                                    
        ScreenSetting:
"""


class RootLayout(BoxLayout):
    def upd(self):
        self.ids['rv_btn'].text = '1111'


class ConnectButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def con(self, client_name):
        self.database = DBController(client_name)
        return self.database
        # test_db.add_contact('test2')
        # test_db.fill_contacts(['test3', 'test4'])
        # self.client_list = test_db.get_contacts()


class SettingsImageButton(ButtonBehavior, Image):
    """ button with image """


class Status(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.setter('text_size'))


class ClientSummaryLayout(BoxLayout):
    """ client settings, avatar, status """


class ClientContactsRowButton(RecycleDataViewBehavior, Button):
    """ button for contacts """


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class ClientContacts(RecycleView):
    """ RecycleView with client's contacts """


class ClientApp(App):
    data = StringProperty('initial text')
    client_name = StringProperty('client_name')
    client_list = ''

    def connect_to_db(self):
        self.test_db = DBController(self.client_name)
        self.test_db.add_contact('test2')
        self.test_db.save_message('test1', 'test2', 'in_msg')
        self.client_list = self.test_db.get_contacts()
        print(self.test_db.get_contacts())
        print(self.data)

    def build(self):
        self.bind(data=self.do_something)

        return Builder.load_string(kv)

    def do_something(self, *args):
        print('do_something got called because 1111 changed')
        ClientContacts().data = [{'text': 'str(x'}]


if __name__ == '__main__':
    ClientApp().run()
