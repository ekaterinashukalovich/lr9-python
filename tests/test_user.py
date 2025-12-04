import unittest
from models.user import User

class TestUserModel(unittest.TestCase):

    def test_user_valid(self):
        user = User(1, "Анна")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Анна")

    def test_user_invalid_id(self):
        with self.assertRaises(ValueError):
            User(-1, "Анна")

    def test_user_invalid_name(self):
        with self.assertRaises(ValueError):
            User(1, "")
        with self.assertRaises(ValueError):
            User(1, "A")  
