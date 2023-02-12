from django.conf import settings
from selenium.webdriver.common.by import By
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

class MyListsTest(FunctionalTest):
    '''тест приложения Мои Списки'''

    def create_pre_authenticated_session(self, email):
        '''создать предварительно аутентифицированный сеанс'''

        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## установить cookie, которые нужны для первого посещения домена.
        ## страницы 404 загружаются быстрее всего!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_are_saved_as_my_lists(self):
        '''тест: списки зарегистрированных пользователей сохраняются как "My lists"'''

        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_session('edith@example.com')

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # Она замечает ссылку на "My lists" в первый раз
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        # Она видит, что ее список находится там, и он назван
        # на основе первого элемента списка
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Reticulate splines')
        )
        self.browser.find_element(By.LINK_TEXT, 'Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает начать еще один список, чтобы только убедиться
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Под заголовком "My lists" появляется ее новый список
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Click cows')
        )
        self.browser.find_element(By.LINK_TEXT, 'Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция "My lists" исчезает
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements(By.LINK_TEXT, 'My lists'),
            []
        ))