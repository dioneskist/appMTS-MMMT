import unittest
from os.path import exists

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from elements.models.ScreenHandlerTT import ScreenHandlerTT
from telas.telatestettab import TelaTesteTTAB
from telas.telatestettde import TelaTesteTTDE
from utils.screen_combinations import preparar_combinacoes


class TestScreenHandlerTT(unittest.TestCase):
    letters = 'TT BA/ED'

    def setUp(self):
        self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.letters)

    def test_create_screenhandler(self):
        a = App()
        sh = ScreenHandlerTT()
        a.root = sh
        Clock.schedule_once(a.stop, .1)
        a.run()

    def test_change_screenhandler_from_mainAPP(self):
        a = App()
        sm = ScreenManager()
        a.root = sm
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm)

        sh = ScreenHandlerTT()
        a.root = sh
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sh)

    def test_change_screenmanager_with_screens_and_back(self):
        s1 = Screen(name='tela1')
        sm1 = ScreenManager()
        sm1.add_widget(s1)

        s2 = Screen(name='tela2')
        sm2 = ScreenManager()
        sm2.add_widget(s2)

        sh1 = Screen(name='telash1')
        sh = ScreenHandlerTT()
        sh.add_widget(sh1)

        a = App()
        a.root = sm1
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm1)
        self.assertEquals(a.root.current_screen.name, s1.name)

        a.root = sh
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sh)
        self.assertEquals(a.root.current_screen.name, sh1.name)

        a.root = sm2
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sm2)
        self.assertEquals(a.root.current_screen.name, s2.name)

    def test_load_telatestettab(self):
        ordem = 'ordem1'
        screen_name = 'TelaTesteTTAB_0'
        a = App()
        kv_file = 'kvs/test_load_telatestettab.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)
        s = TelaTesteTTAB(name=screen_name,
                          combinacoes=self.all_combinacoes_XY[0],
                          ordem=ordem)
        sh = ScreenHandlerTT()
        sh.add_widget(s)
        a.root = sh
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sh)
        self.assertEquals(a.root.current_screen.name, s.name)

    def test_load_telatestettde(self):
        ordem = 'ordem1'
        screen_name = 'TelaTesteTTDE_0'
        a = App()
        kv_file = 'kvs/test_load_telatestettde.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)
        s = TelaTesteTTAB(name=screen_name,
                          combinacoes=self.all_combinacoes_ZW[0],
                          ordem=ordem)
        sh = ScreenHandlerTT()
        sh.add_widget(s)
        a.root = sh
        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root, sh)
        self.assertEquals(a.root.current_screen.name, s.name)

    def test_load_change_telas_AB_to_DE(self):
        ordem = 'ordem1'
        kv_file = 'kvs/test_load_telatestett_all_screens.kv'
        self.assertEquals(True, exists(kv_file))
        a = App()
        a.load_kv(kv_file)

        screen_name_sab = 'TelaTesteTTAB_0'
        sab = TelaTesteTTAB(name=screen_name_sab,
                            combinacoes=self.all_combinacoes_XY[0],
                            ordem=ordem)
        screen_name_sde = 'TelaTesteTTDE_0'
        sde = TelaTesteTTDE(name=screen_name_sde,
                            combinacoes=self.all_combinacoes_ZW[0],
                            ordem=ordem)
        sh = ScreenHandlerTT()
        sh.add_widget(sab)
        sh.add_widget(sde)

        a.root = sh
        Clock.schedule_once(a.stop, 1.1)
        a.run()

        a.root.current_screen = sab.name
        a.root.current_screen = sde.name
