from kivy.uix.screenmanager import Screen
import logging


class TelaInstrucoes(Screen):

    def on_enter(self):
        if 'TT' in self.manager.letters:
            self.ids._instrucoes.text = """
Continue fazendo como você aprendeu. Agora a carinha feliz não aparecerá e a figura não voltará para o lugar.
"""
            logging.debug("Instrucoes printadas!!")
        else:
            self.ids._instrucoes.text = """
Cada figura possui um par. Vamos descobrir quais são os pares?
Arraste e junte as figuras para formar os pares. Quando você acertar, uma carinha feliz aparecerá. Quando você errar, a figura voltará para o lugar.
            """
            logging.debug("Instrucoes printadas!!")
