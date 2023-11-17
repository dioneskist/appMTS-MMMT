from kivy.uix.screenmanager import Screen


class TelaNomeParticipante(Screen):
    def on_leave(self, *args):
        self.manager.participant_name = self.ids._input.text
