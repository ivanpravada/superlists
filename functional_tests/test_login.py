from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from .base import FunctionalTest

TEST_EMAIL = 'edith@example_blabla.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    '''тест регистрации в системе'''

    def test_can_get_email_link_to_log_in(self):
        '''тест: можно получить ссылку по почте для регистрации'''
        # Эдит заходит на сайт суперсписков и замечает
        # раздел "войти" в навигационной панели.
        # Она вводит свой адрес электронной почты
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту
        # было выслано электронное письмо
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        # Эдит проверяет свою почту и находит сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдин нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )
        navbar =self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # Теперь она выходит из системы
        self.browser.find_element(By.LINK_TEXT, "Log out").click()

        # Она вышла из системы
        self.wait_for(
            lambda: self.browser.find_element(By.NAME, 'email')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)