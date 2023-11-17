import unittest

from kivy.uix.screenmanager import ScreenManager

from telas.telaTTbaed import TelaTTbaed


class ScreenTestCase(unittest.TestCase):

    def test_setUp(self):
        # import class and prepare everything here.
        pass

    def test_screen_created_from_abstraction(self):
        sm = ScreenManager()
        tela1 = TelaTTbaed()
        tela2 = TelaTTbaed()
        sm.add_widget(tela1)
        sm.add_widget(tela2)
        sm.current = tela1.name
        sm.current = tela2.name
        sm.remove_widget(tela1)
        print(sm.screens)
