import itertools
import logging
import unittest
from datetime import datetime
from os.path import exists

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from elements.models.ScreenHandlerTT import ScreenHandlerTT
from telas.telatestettab import TelaTesteTTAB
from elements.elements import SourcePicture, TargetPicture
from telas.telatestettde import TelaTesteTTDE
from telas.telatreinoab import TelaTreinoAB

from utils.screen_combinations import gerar_todas_combinacoes, preparar_combinacoes


class TestTelaTesteTT(unittest.TestCase):
    letters = 'TT BA/ED'

    def setUp(self):
        self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.letters)

    def test_load_screen_target_and_source(self):
        class Tela1(Screen):
            pass

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root.ids._ti1.source, 'figuras/ordem1/a_1.jpg')
        self.assertEquals(a.root.ids._t1.wid, 'wid-t1')

        self.assertEquals(a.root.ids._si1.source, 'figuras/ordem1/a_2.jpg')
        self.assertEquals(a.root.ids._s1.wid, 'wid-s1')

    def test_load_screenTelaTesteTTAB_target_and_source(self):
        class TelaTesteTTABTest(Screen):
            pass

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen2_ab.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root.ids._ti1.source, 'figuras/ordem1/a_1.jpg')
        self.assertEquals(a.root.ids._t1.wid, 'wid-t1')

        self.assertEquals(a.root.ids._si1.source, 'figuras/ordem1/a_2.jpg')
        self.assertEquals(a.root.ids._s1.wid, 'wid-s1')

        self.assertEquals(a.root.name, '')

    def test_load_screenTelaTesteTTAB_target_and_source_completos_ordem1(self):
        ordem = 'ordem1'
        screen_name = 'TelaTesteTTAB_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_ab.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTAB(name=screen_name,
                          combinacoes=self.all_combinacoes_XY[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_XY[0][3]
        combination_t2 = self.all_combinacoes_XY[0][4]
        combination_t3 = self.all_combinacoes_XY[0][5]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/ordem1/" + str(combination_t1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti2.source, "figuras/ordem1/" + str(combination_t2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti3.source, "figuras/ordem1/" + str(combination_t3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')
        self.assertEquals(a.root.current_screen.ids._t2.wid, 'wid-t2')
        self.assertEquals(a.root.current_screen.ids._t3.wid, 'wid-t3')

        combination_s1 = self.all_combinacoes_XY[0][0]
        combination_s2 = self.all_combinacoes_XY[0][1]
        combination_s3 = self.all_combinacoes_XY[0][2]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/ordem1/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/ordem1/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/ordem1/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_load_screenTelaTesteTTAB_target_and_source_completos_ordem2(self):
        ordem = 'ordem2'
        screen_name = 'TelaTesteTTAB_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_ab.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTAB(name=screen_name,
                          combinacoes=self.all_combinacoes_XY[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_XY[0][3]
        combination_t2 = self.all_combinacoes_XY[0][4]
        combination_t3 = self.all_combinacoes_XY[0][5]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/ordem2/" + str(combination_t1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti2.source, "figuras/ordem2/" + str(combination_t2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti3.source, "figuras/ordem2/" + str(combination_t3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')
        self.assertEquals(a.root.current_screen.ids._t2.wid, 'wid-t2')
        self.assertEquals(a.root.current_screen.ids._t3.wid, 'wid-t3')

        combination_s1 = self.all_combinacoes_XY[0][0]
        combination_s2 = self.all_combinacoes_XY[0][1]
        combination_s3 = self.all_combinacoes_XY[0][2]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/ordem2/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/ordem2/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/ordem2/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_load_screenTelaTesteTTAB_target_and_source_completos_ordemteste(self):
        ordem = 'teste'
        screen_name = 'TelaTesteTTAB_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_ab.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTAB(name=screen_name,
                          combinacoes=self.all_combinacoes_XY[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_XY[0][3]
        combination_t2 = self.all_combinacoes_XY[0][4]
        combination_t3 = self.all_combinacoes_XY[0][5]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/teste/" + str(combination_t1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti2.source, "figuras/teste/" + str(combination_t2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._ti3.source, "figuras/teste/" + str(combination_t3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')
        self.assertEquals(a.root.current_screen.ids._t2.wid, 'wid-t2')
        self.assertEquals(a.root.current_screen.ids._t3.wid, 'wid-t3')

        combination_s1 = self.all_combinacoes_XY[0][0]
        combination_s2 = self.all_combinacoes_XY[0][1]
        combination_s3 = self.all_combinacoes_XY[0][2]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/teste/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/teste/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/teste/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_load_screenTelaTesteTTDE_target_and_source(self):
        class TelaTesteTTDETest(Screen):
            pass

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen2_de.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        Clock.schedule_once(a.stop, .1)
        a.run()
        self.assertEquals(a.root.ids._ti1.source, 'figuras/ordem1/a_1.jpg')
        self.assertEquals(a.root.ids._t1.wid, 'wid-t1')

        self.assertEquals(a.root.ids._si1.source, 'figuras/ordem1/a_2.jpg')
        self.assertEquals(a.root.ids._s1.wid, 'wid-s1')

        self.assertEquals(a.root.name, '')

    def test_load_screenTelaTesteTTDE_target_and_source_completos_ordem1(self):
        ordem = 'ordem1'
        screen_name = 'TelaTesteTTDE_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_de.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTDE(name=screen_name,
                          combinacoes=self.all_combinacoes_ZW[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_ZW[0][0]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/ordem1/" + str(combination_t1) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')

        combination_s1 = self.all_combinacoes_ZW[0][1]
        combination_s2 = self.all_combinacoes_ZW[0][2]
        combination_s3 = self.all_combinacoes_ZW[0][3]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/ordem1/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/ordem1/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/ordem1/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_load_screenTelaTesteTTDE_target_and_source_completos_ordem2(self):
        ordem = 'ordem2'
        screen_name = 'TelaTesteTTDE_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_de.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTDE(name=screen_name,
                          combinacoes=self.all_combinacoes_ZW[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_ZW[0][0]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/ordem2/" + str(combination_t1) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')

        combination_s1 = self.all_combinacoes_ZW[0][1]
        combination_s2 = self.all_combinacoes_ZW[0][2]
        combination_s3 = self.all_combinacoes_ZW[0][3]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/ordem2/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/ordem2/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/ordem2/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_load_screenTelaTesteTTDEtarget_and_source_completos_ordemteste(self):
        ordem = 'teste'
        screen_name = 'TelaTesteTTDE_0'

        a = App()
        kv_file = 'kvs/test_targetsource_with_screen3_de.kv'
        self.assertEquals(True, exists(kv_file))
        a.load_kv(kv_file)

        sm = ScreenManager()
        s = TelaTesteTTDE(name=screen_name,
                          combinacoes=self.all_combinacoes_ZW[0],
                          ordem=ordem)
        sm.add_widget(s)
        a.root = sm

        Clock.schedule_once(a.stop, .1)
        a.run()

        combination_t1 = self.all_combinacoes_ZW[0][0]
        self.assertEquals(a.root.current_screen.ids._ti1.source, "figuras/teste/" + str(combination_t1) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._t1.wid, 'wid-t1')

        combination_s1 = self.all_combinacoes_ZW[0][1]
        combination_s2 = self.all_combinacoes_ZW[0][2]
        combination_s3 = self.all_combinacoes_ZW[0][3]
        self.assertEquals(a.root.current_screen.ids._si1.source, "figuras/teste/" + str(combination_s1) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si2.source, "figuras/teste/" + str(combination_s2) + ".jpg")
        self.assertEquals(a.root.current_screen.ids._si3.source, "figuras/teste/" + str(combination_s3) + ".jpg")

        self.assertEquals(a.root.current_screen.ids._s1.wid, 'wid-s1')
        self.assertEquals(a.root.current_screen.ids._s2.wid, 'wid-s2')
        self.assertEquals(a.root.current_screen.ids._s3.wid, 'wid-s3')

        self.assertEquals(a.root.current_screen.name, screen_name)

    def test_on_enter_and_on_leave(self):
        pass
