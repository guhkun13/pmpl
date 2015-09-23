from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
#from lists.model import * #import all table

# Create your views here.
def home_page(request):
	
#	if request.method == 'POST':
#		Item.objects.create(text=request.POST['item_text'])
#		return redirect('/lists/the-only-list-in-the-world/')
	
	#items = Item.objects.all()
	# start of tutorial 2 
	#count_item = items.count()
	#message = ''
	#if count_item == 0:
	#	message = 'yey, waktunya berlibur'
	#elif count_item > 0 and count_item < 5 :
	#	message = 'sibuk tapi santai'
	#elif count_item > 4:
	#	message = 'oh tidak'
	
	# end of tutorial 2
	#content = { 'items':items, 'message':message }
	page = 'home.html'
	#return render(request, page, content)
	return render(request, page)

def view_list(request):
	items = Item.objects.all()
	content = { 'items':items }
	page = 'list.html'
	return render(request, page, content )
	

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list =  list_)
	return redirect('/lists/the-only-list-in-the-world/')
