from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


# Builder.load_string('''
kv = ('''
<SelectableLabel>:
    id: my_select
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RVClientContacts>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: False
        
BoxLayout:
    orientation: 'vertical'
    RVClientContacts:
    
    Button:
        id: btn_client_id
        text: 'UwU'
    
    Label:
        id: cl_n
        text: '9'
        
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, Label):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        self.nsme = rv.data[index]
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            print(self.text)
        else:
            print("selection removed for {0}".format(rv.data[index]))

    def get_text(self):
        return self.text


class RVClientContacts(RecycleView):
    def __init__(self, **kwargs):
        super(RVClientContacts, self).__init__(**kwargs)
        client_list = ['cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3',
                       'cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3']
        self.data = [{'text': str(x)} for x in client_list]


class TestApp1(App):
    def build(self):
        client_list = ['cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3',
                       'cl1', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3', 'cl2', 'cl3']
        # return RVClientContacts(client_list)
        return Builder.load_string(kv)


if __name__ == '__main__':
    TestApp1().run()
