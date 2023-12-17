import unittest
from os.path import exists

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class TestKivyFile(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_kivy_file_with_boxlayout(self):
        a = App()
        kv_file = 'kvs/simple_button.kv'
        self.assertEquals(True, exists(kv_file))

        a.load_kv(kv_file)
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root.ids._button.text, 'Button 1 for test')

    def test_load_kivy_file_with_screen(self):
        class Tela1(Screen):
            pass

        a = App()
        kv_file = 'kvs/simple_button_screen.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root.ids._button.text, 'Button 1 for test')
        self.assertEquals(a.root.name, 'tela1')
