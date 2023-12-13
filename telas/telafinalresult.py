from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class TelaFinalResult(Screen):
    _result = StringProperty()

    def on_enter(self, *args):
        self._result = str(self.manager.result_log_human)