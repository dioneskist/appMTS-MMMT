from kivy.uix.screenmanager import Screen
import logging

class TelaInstrucoes(Screen):

    def on_enter(self):
        if 'TT' in self.manager.letters:
            self.ids._instrucoes.text = """
Aparecerão figuras na tela. Você deve tocar sobre a figura à esquerda e arrastá-la até um dos retângulos com bordas cinza à direita. Cada figura à esquerda possui um par à direita. Dessa vez não haverá smiles indicando se você acertou ou não. Quando as tarefas terminarem, você será informado pelo programa.
"""
            logging.debug("Instrucoes printadas!!")
        else:
            self.ids._instrucoes.text = """
Aparecerão figuras na tela. Você deve tocar sobre as figuras à esquerda e arrastá-la até um dos retângulos com bordas cinza à direita. Cada figura à esquerda possui um par à direita. Se você acertar, um smile aparecerá na tela. Quando as tarefas terminarem você será informado pelo programa.
            """
            logging.debug("Instrucoes printadas!!")
