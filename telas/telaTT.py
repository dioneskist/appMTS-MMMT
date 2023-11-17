import logging
from abc import ABC, abstractmethod
from kivy.uix.screenmanager import Screen


class TelaTT(Screen):

    @abstractmethod
    def on_enter(self):
        pass
    @abstractmethod
    def on_leave(self, *args):
        print('on_leave: {} com ids: {}'.format(self.name, self.ids))

    @abstractmethod
    def popula_imagens_source(self):
        pass

    @abstractmethod
    def popula_imagens_target(self):
        pass