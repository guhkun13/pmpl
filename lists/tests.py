from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()  
		response = home_page(request)

		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
## moved
#	def test_home_page_can_save_a_POST_request(self):
#		request = HttpRequest()  
#		request.method = 'POST'
#		request.POST['item_text'] = 'A new list item'

#		response = home_page(request) 
		
#		self.assertEqual(Item.objects.count(), 1) 	#check one new item saved
#		new_item = Item.objects.first() 		#get first item from new objects
#		self.assertEqual(new_item.text, 'A new list item') #check the content (text)


#	def test_home_page_redirects_after_POST(self):
#		request = HttpRequest()
#		request.method = 'POST'
#		request.POST['item_text'] = 'A new list item'
		
#		response = home_page(request)
		
#		self.assertEqual(response.status_code, 302)
#		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

		
##removed		
#	def test_home_page_only_saves_items_when_necessary(self):
#		request = HttpRequest()
#		home_page(request)
#		self.assertEqual(Item.objects.count(), 0)
	
# start of tutorial 2

#	def test_komentar_pribadi_gabut(self):
#		request = HttpRequest()
		#response = home_page(request)
#		response = view_list(request)
#		self.assertIn("yey, waktunya berlibur", response.content.decode())
	
#	def test_komentar_pribadi_santai(self):
#		Item.objects.create(text='itemey 1')
#		Item.objects.create(text='itemey 1')
#		Item.objects.create(text='itemey 1')
#		Item.objects.create(text='itemey 1')
		
#		request = HttpRequest()
		#response = home_page(request)
#		response = view_list(request)

#		self.assertIn("sibuk tapi santai", response.content.decode())

#	def test_komentar_pribadi_sibuk(self):
#		Item.objects.create(text='itemey 1')
#		Item.objects.create(text='itemey 2')
#		Item.objects.create(text='itemey 3')
#		Item.objects.create(text='itemey 4')
#		Item.objects.create(text='itemey 5')
		
#		request = HttpRequest()
		#response = home_page(request)
#		response = view_list(request)

#		self.assertIn("oh tidak", response.content.decode())

# end of tutorial 2

#class ItemModelTest(TestCase):
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
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)	
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		#response = self.client.get('/lists/the-only-list-in-the-world/')
		#self.assertTemplateUsed(response, 'list.html')
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')
	
	#def test_displays_all_items(self):
		
		#Item.objects.create(text='itemey 1')
		#Item.objects.create(text='itemey 2')
		
		#response = self.client.get('/lists/the-only-list-in-the-world/')
		
		#self.assertContains(response, 'itemey 1', status_code=200)
		#self.assertContains(response, 'itemey 2', status_code=200)
		#self.assertContains(response, 'itemey 1',)
		#self.assertContains(response, 'itemey 2',)

		#list_ = List.objects.create()
		#Item.objects.create(text='itemey 1', list = list_)
		#Item.objects.create(text='itemey 2', list = list_)
	
	def test_display_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list = correct_list)
		Item.objects.create(text='itemey 2', list = correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other item list 1', list = other_list)
		Item.objects.create(text='other item list 2', list = other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')




class NewListTest(TestCase):
	
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data = {'item_text':'A new list item'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		list_ = List.objects.create()
		new_item.list = list_
		
		self.assertEqual(new_item.text, 'A new list item')
		self.assertEqual(new_item.list, list_)

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'}
		)
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

		
class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			'lists/%d/add_item' % (correct_list.id,),
			data = {'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

		
	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text':'A new item for an existing list'}
		)
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
