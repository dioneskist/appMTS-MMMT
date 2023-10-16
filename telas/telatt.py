from kivy.uix.screenmanager import Screen


class TelaTT(Screen):
    def on_leave(self, *args):
        self.manager.comecar()
