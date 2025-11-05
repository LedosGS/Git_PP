import unittest

from main import *


class TestHexRegex(unittest.TestCase):
    def setUp(self):
        self.hex_re = hex_re
    def test_hex_valid(self):
        self.assertTrue(hex_bool("#123"))
        self.assertTrue(hex_bool("#139"))
        self.assertTrue(hex_bool("#A96"))
        self.assertTrue(hex_bool("#FFFFE0"))
        self.assertTrue(hex_bool("#FF4500"))
        self.assertTrue(hex_bool("#0123"))
        self.assertTrue(hex_bool("#852A"))
        self.assertTrue(hex_bool("#800080"))
        self.assertTrue(hex_bool("#AA34FF54"))
        self.assertTrue(hex_bool("#FE375F01"))

    def test_hex_invalid(self):
        self.assertFalse(hex_bool("#h23"))       # знак h
        self.assertFalse(hex_bool("#-+h23"))     # знаки сложения и вычитания
        self.assertFalse(hex_bool("#$%^"))       # не подходящие знаки
        self.assertFalse(hex_bool("#FFFFEп"))    # русский символ


    def test_boundary_hex(self):
        self.assertFalse(hex_bool("#"))         # 1 число
        self.assertFalse(hex_bool("#1"))        # 0 чисел
        self.assertFalse(hex_bool("#12"))       # 2 числа
        self.assertFalse(hex_bool("#13978"))    # 5 чисел
        self.assertFalse(hex_bool("#FF45001"))  # 7 знаков
        self.assertFalse(hex_bool("#AA34FF549"))# 9 знаков

def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestHexRegex))
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)



