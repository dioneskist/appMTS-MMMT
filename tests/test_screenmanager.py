import unittest

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.clock import Clock
from kivy import lang


class TestScreeManager(unittest.TestCase):
    def setUp(self):
        pass
        s = Screen(name='teste_sm1')
        s.add_widget(Label(text='sm1'))

        sm = ScreenManager()
        sm.add_widget(s)

        s2 = Screen(name='teste_sm2')
        s2.add_widget(Label(text='sm2'))
        sm2 = ScreenManager()
        sm2.add_widget(s2)

        self.sm = sm
        self.sm2 = sm2

    def test_two_apps(self):
        lang._delayed_start = None
        a = App()
        a.root = self.sm
        Clock.schedule_once(a.stop, .1)
        a.run()

        b = App()
        b.root = self.sm2
        Clock.schedule_once(b.stop, .1)
        b.run()

    def test_two_sm(self):
        lang._delayed_start = None
        a = App()
        a.root = self.sm
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, self.sm)
        a.root = self.sm2
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, self.sm2)

    def test_two_sm_with_previous_saved(self):
        lang._delayed_start = None
        a = App()
        a.root = self.sm
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, self.sm)
        sm_previous = a.root
        a.root = self.sm2
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, self.sm2)

        a.root = sm_previous
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm_previous)

    def test_two_sm_with_diferente_screens(self):
        lang._delayed_start = None
        a = App()

        s1sm1 = Screen(name='s1sm1')
        s1sm2 = Screen(name='s1sm2')
        s2sm1 = Screen(name='s2sm1')
        s2sm2 = Screen(name='s2sm2')

        sm1 = ScreenManager()
        sm1.add_widget(s1sm1)
        sm1.add_widget(s1sm2)
        a.root = sm1
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm1)
        self.assertEquals(len(a.root.screens), 2)
        self.assertEquals(a.root.screen_names, [s1sm1.name, s1sm2.name])

        sm2 = ScreenManager()
        sm2.add_widget(s2sm1)
        sm2.add_widget(s2sm2)
        a.root = sm2
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm2)
        self.assertEquals(len(a.root.screens), 2)
        self.assertEquals(a.root.screen_names, [s2sm1.name, s2sm2.name])

