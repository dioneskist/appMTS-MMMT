import ssl

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen


class Sm1(ScreenManager):
    pass


class Sm2(ScreenManager):
    pass


class MyButton(Button):

    def on_release(self):
        print('On')
        self.parent.parent.app


class Main(App):

    # def __init__(self):
    #     self.sm1 = Sm1()
    #     self.sm2 = Sm2()

    def build(self):
        self.title = 'teste'
        s = Screen(name="teste")
        la = Label(text='teste')
        b = MyButton(text='teste')
        b.on_release()
        s.add_widget(la)
        s.add_widget(b)
        sm = ScreenManager()
        sm.add_widget(s)
        return sm

    def troca(self):
        print('troquei')


Main().run()
