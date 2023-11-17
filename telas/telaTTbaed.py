import logging
from abc import ABC

from kivy.uix.screenmanager import Screen

from telas.telaTT import TelaTT


class TelaTTbaed(TelaTT):

    def on_leave(self, *args):
        print('ON_ENTER')

    def popula_imagens_source(self):
        pass

    def popula_imagens_target(self):
        pass

    def on_enter(self, *args):
        print('ON_ENTER')


# def on_enter(self):
#     print('test')

# def on_leave(self, *args):
#     # if pretreino screen telatt will not be called
#     if self.manager.ordem != "pretreino":
#         logging.debug("Ordem select is {}".format(self.manager.ordem))
#         self.manager.comecar()
