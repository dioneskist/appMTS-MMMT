import unittest

from utils import combinations


class TestCombinations(unittest.TestCase):

    def setUp(self):
        pass

    def test_ordem_de(self):

        lst = combinations.get_de_ordem()
        self.assertEquals(len(lst), 18)
