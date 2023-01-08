from django.test import TestCase

class SendLoginEmailViewTest(TestCase):
    '''тест представления, которое отправляет сообщение для входа в систему'''

    def test_redirects_to_home_page(self):
        '''тест: переадресация на домашнюю страницу'''

        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')