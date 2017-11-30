from django.test import TestCase
from django.test import Client
from .forms import *   # import all forms

class Setup_Class(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@mp.com", password="user", first_name="user", phone=12345678)

class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = UserForm(data={'email': "user@mp.com", 'password': "user", 'first_name': "user", 'phone': 12345678})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = UserForm(data={'email': "", 'password': "mp", 'first_name': "mp", 'phone': ""})
        self.assertFalse(form.is_valid())
