from django.test import TestCase
from lists.models import Item,List

# 测试1：views/home_page 不用了
class HomePageTest(TestCase):
    # 测试1.1：向主页发送request后跳转到list.html
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

# 测试2：views/view_list
class ListViewTest(TestCase):
    # 测试2.1：所有list有自己的url
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'list.html')
    # 测试2.2：显示所有某一个List的所有Items
    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 1', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')
    

# 测试3：views/new_list
class NewListTest(TestCase):
    # 测试：new_list能否成功将数据存入
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
    # 测试：重定向到/lists/{new_list.id}/
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',data={'item_text':'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')

# 测试4：models/List models/Item
class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
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
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'A new item for an exsiting list'}
        )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an exsiting list')
        self.assertEqual(new_item.list,correct_list)
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'A new item for an exsiting list'}
        )
        self.assertRedirects(response,f'/lists/{correct_list.id}/')
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list)
