from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()

class AuthenticateTest(TestCase):
    '''тест аутентификации'''

    def test_returns_None_if_no_such_token(self):
        '''тест: возвращает None, если нет такого токена'''

        result = PasswordlessAuthenticationBackend().authenticate(None,
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''тест: возвращается новый пользователь с правильной электронной почтой, если токен существует'''

        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        '''тест: возвращается существующий пользователь с правильной электронной почтой, если токен существует'''

        email = 'edith@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    '''тест получения пользователя'''

    def test_gets_user_by_email(self):
        '''тест: получает пользователя по адресу email'''

        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'edith@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        '''тест: возвращает None, если нет пользователя с таким email'''

        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('edith@example.com')
        )