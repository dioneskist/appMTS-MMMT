import unittest

from utils import combinations


class TestWidgetTelasTRTT(unittest.TestCase):

    def setUp(self):
        self.ordem = 'ABDE'
        self.combinacoes = combinations.gerar_todas_combinacoes()

    def