from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

kv = """
<ClientContactsRowButton>:
    on_press: app.root.ids['selected_contact'].text = 'Чат с контактом ' + self.text
    on_press: app.root.ids['manager'].current = 'chat_window'

RootLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 100
        SettingsImageButton:
            on_press: manager.current = 'client_settings'
        Image:
            source: 'static/default_avatar.jpg'
            size_hint: (None, None)
        Status:
            text: 'Это статус'
            pos_hint: {'center_y': 1}
            padding: (10, 10)
    ScreenManager:
        id: manager
        Screen:
            name: 'client_contacts'
            BoxLayout:
                orientation: 'vertical'
                TextInput:
                    size_hint_y: None
                    height: dp(40)
                    text: app.data
                    on_text: app.data = self.text
                ClientContacts:
                    id: rv
        Screen:
            name: 'chat_window'
            Button:
                on_press: root.upd()
            BoxLayout:
                orientation: 'vertical'
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
                TextInput:
                    text: app.data
                    on_text: app.data = self.text
                Button:
                    size_hint_y: None
                    height: dp(40)
                    text: 'Отправить'
                    # TODO add send
                    on_press:                                    
        Screen:
            name: 'client_settings'
            Label:
                text: 'Здесь будут настройки'
            Button:
                text: '<< в список контактов'
                on_press: manager.current = 'client_contacts'
"""


class RootLayout(BoxLayout):
    def upd(self):
        self.ids['rv_btn'].text = '1111'


class SettingsImageButton(ButtonBehavior, Image):
    """ button with image """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'static/settings.png'
        self.size = (50, 50)
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': .7, 'center_y': .5}


class Status(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.setter('text_size'))


class ClientContactsRowButton(RecycleDataViewBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(40)


class ClientContacts(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client_list = ['cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3',
                            'cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3']

        self.client_contacts_layout = GridLayout(cols=1, size_hint_y=None)
        self.client_contacts_layout.bind(minimum_height=self.client_contacts_layout.setter('height'),
                                         )
        self.add_widget(self.client_contacts_layout)

        for i in self.client_list:
            self.client_contacts_layout.add_widget(ClientContactsRowButton(text=str(i),
                                                                           id=str(i),
                                                                           ))


class ClientApp(App):
    data = StringProperty('initial text')

    def build(self):
        self.bind(data=self.do_something)

        return Builder.load_string(kv)

    def do_something(self, *args):
        print('do_something got called because 1111 changed')

    def selectionChange(self, inst, val):
        print('hey! select ', self.rv.data[val[0]]['text'])


if __name__ == '__main__':
    ClientApp().run()
