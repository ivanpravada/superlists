from lists.models import Item, List
from django.test import TestCase

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_uses_home_template(self):
        '''тест: используется домашний шаблон'''

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # def test_can_save_a_POST_request(self):
    #     '''тест: можно сохранить post-запрос'''

    #     response = self.client.post('/', data = {'item_text': 'A new list item'})

    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'A new list item')

    # def test_redirect_after_POST(self):
    #     '''тест: переадресует после post-запроса'''

    #     response = self.client.post('/', data = {'item_text': 'A new list item'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], '/lists/the_best_link/')

    # def test_only_saves_items_when_necessary(self):
    #     '''тест: сохраняет элементы, только когда нужно'''

    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)


class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элементов списка'''

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

    # def test_display_all_list_items(self):
    #     '''тест: отображаются все элементы списка'''

    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
        
    #     response = self.client.get('/')

    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())

class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        
        response = self.client.get('/lists/the_best_link/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        '''тест: отображаются все элементы списка'''

        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        
        response = self.client.get('/lists/the_best_link/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''

        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''тест: переадресует после post-запроса'''
        
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the_best_link/')

