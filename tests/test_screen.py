import unittest


class ScreenTestCase(unittest.TestCase):

    def test_setUp(self):
        # import class and prepare everything here.
        pass

    def test_valida_screen_size(self):
        # place your test case here
        x = 1200
        y = 1200
        self.assertEqual(x, y)
