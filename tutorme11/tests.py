from django.test import TestCase

from .models import CustomUser


class CustomerUserModelTests(TestCase):
    
    def test_custom_user_choices(self):
        USER_TYPE_CHOICES = (
            ('tutor', 'Tutor'),
            ('tutoree', 'Tutoree'),
        )
        custom_user = CustomUser()
        self.assertEquals(custom_user.USER_TYPE_CHOICES,USER_TYPE_CHOICES)

    def test_custom_user_user_type(self):
        custom_user0 = CustomUser()
        self.assertEquals(custom_user0.user_type,None)
        custom_user1 = CustomUser(user_type="tutor")
        self.assertEquals(custom_user1.user_type,"tutor")

