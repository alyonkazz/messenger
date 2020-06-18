from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

Builder.load_string('''
<ChatWithContact>:
    viewclass: 'Label'
    
    RecycleBoxLayout:
        canvas:
            Color:
                rgba: 1, 0, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


class ChatWithContact(RecycleView):
    def __init__(self, **kwargs):
        super(ChatWithContact, self).__init__(**kwargs)
        chat_with_contact = ['hi', 'hey', '1', '2', '3']
        self.data = [{'text': str(x)} for x in chat_with_contact]


class TestApp(App):
    def build(self):
        return ChatWithContact()


if __name__ == '__main__':
    TestApp().run()
