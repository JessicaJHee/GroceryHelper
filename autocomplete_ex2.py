from kivy.app import App
from kivy.properties import StringProperty, ListProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import Spinner


class AddressChooser(FocusBehavior, Spinner):
    addressfile = StringProperty()
    addresslist = ListProperty([])

    def __init__(self, **kwargs):
        self.addressfile = kwargs.pop('addressfile', '')
        self.sync_height = True
        super(AddressChooser, self).__init__(**kwargs)
        self.modifiers = []
        self.bind(addressfile=self.load_addresses)
        self.load_addresses()

    def on_parent(self, widget, parent):
        self.focus = True

    def load_addresses(self):
        if self.addressfile:
            with open(self.addressfile) as fd:
                for line in fd:
                    self.addresslist.append(line)
        else:
            self.addresslist = []
        self.values = []
        if len(self.text) > 0:
            self.on_text(self, self.text)

    def on_text(self, chooser, text):
        values = []
        for addr in self.addresslist:
            if addr.startswith(text):
                values.append(addr)
        self.values = values
        self.is_open = True

    def keyboard_on_key_up(self, window, keycode):
        if keycode[0] == 304:
            self.modifiers.remove('shift')
        super(AddressChooser, self).keyboard_on_key_up(window, keycode)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 304:   # shift
            self.modifiers.append('shift')
        elif keycode[0] == 8 and len(self.text) > 0:   # backspace
            self.text = self.text[:-1]
        else:
            if 'shift' in self.modifiers:
                self.text += text.upper()
            else:
                self.text += text
        super(AddressChooser, self).keyboard_on_key_down(window, keycode, text, modifiers)


class TestApp(App):
    def build(self):
        layout = RelativeLayout()
        chooser = AddressChooser(addressfile='adresses.txt', size_hint=(0.5,None), height=50, pos_hint={'center_x':0.5, 'center_y':0.5})
        layout.add_widget(chooser)
        return layout

if __name__ == '__main__':
    TestApp().run()