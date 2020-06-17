from kivy import app
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from client_contacts import RVClientContacts, SelectableLabel, SelectableRecycleBoxLayout, TestApp1

KV = '''
<MyButton>:
    

<SV>:


BoxLayout:
    MyButton:
        # on_press: 
    RV:
'''


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 40

    def on_press(self):
        print(self.ids['my_select'].text)


client_list = ['cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3',
               'cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3']

RV_c = RVClientContacts(client_list)


class RV(BoxLayout):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.orientation = "vertical"

        # MyButton.text = self.ge

        self.clients_list = RV_c

        self.add_widget(self.clients_list)


class TestApp(App):
    MY_NUMBER = 0

    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    TestApp().run()
