import unittest
from utils import dec_sexagesimal_to_decimal, dec_decimal_to_sexagesimal


class UtilsTestCase(unittest.TestCase):

    def test_dec_sexagesimal_to_decimal(self):
        self.assertEqual(dec_sexagesimal_to_decimal(47, 11, 33.41481719999081), 47.192615227)

    def test_dec_decimal_to_sexagesimal(self):
        self.assertEqual((47, 11, 33.41481719999081), dec_decimal_to_sexagesimal(47.192615227))