from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

width = 1200
height = 1920


class BlankTela(Screen):

    def on_enter(self, *args):
        # add blank screen for 1.5 seconds
        blank_label = Label()

        with blank_label.canvas:
            Color(1, 0.5, 0.5)
            Rectangle(pos=(0, 0), size=(width, height))
        self.add_widget(Label())
