from kivy.uix.screenmanager import Screen


class TelaFinalResult(Screen):
    def __enter__(self):
        self.ids._result.text = str(self.parent.result_log_human)
