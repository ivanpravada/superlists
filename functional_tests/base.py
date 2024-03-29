from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from .server_tools import reset_database
from datetime import datetime
import os
import time


SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

MAX_WAIT = 20

class FunctionalTest(StaticLiveServerTestCase):
    '''функциональный тест'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        '''демонтаж'''
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        '''тест не сработал'''

        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        '''сделать снимок экрана'''

        filename = self._get_filename() + '.png'
        print('screenshotting to ', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        '''выгрузить html'''

        filename = self._get_filename() + '.html'
        print('dumping page HTML to ', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        '''получить имя файла'''

        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.\
            format(
                folder=SCREEN_DUMP_LOCATION,
                classname=self.__class__.__name__,
                method=self._testMethodName,
                windowid=self._windowid,
                timestamp=timestamp
            )

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    @wait
    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        '''получить поле ввода для элемента'''

        return self.browser.find_element(By.ID, 'id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        '''ожидать входа в систему'''

        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Log out")
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        '''ожидать выхода из системы'''

        self.wait_for(
            lambda: self.browser.find_element(By.NAME, 'email')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text):
        '''добавить элемент списка'''

        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')