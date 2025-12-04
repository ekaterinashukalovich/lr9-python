import unittest
from models.user_currency import UserCurrency

class TestUserCurrencyModel(unittest.TestCase):

    def test_user_currency_valid(self):
        uc = UserCurrency(1, "USD")
        self.assertEqual(uc.user_id, 1)
        self.assertEqual(uc.currency_id, "USD")

    def test_invalid_user_id(self):
        with self.assertRaises(ValueError):
            UserCurrency(0, "USD")

    def test_invalid_currency_id(self):
        with self.assertRaises(ValueError):
            UserCurrency(1, "")     
        with self.assertRaises(ValueError):
            UserCurrency(1, "A")    
