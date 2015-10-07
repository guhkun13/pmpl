from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
#from lists.model import * #import all table

# Create your views here.
def home_page(request):
	
	content = {'message': 'yey, waktunya berlibur'}
	page = 'home.html'
	return render(request, page, content)

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	items = Item.objects.filter(list=list_)

#TUT2 komentar peri-badi
	#items_ = Item.objects.all()
	count_item = items.count()
	message = ''
	#if count_item == 0:
	#	message = 'yey, waktunya berlibur'
	if count_item > 0 and count_item < 5 :
		message = 'sibuk tapi santai'
	elif count_item > 4:
		message = 'oh tidak'
#end TUT2
	content = { 'list' : list_ , 'message' : message}
	page = 'list.html'
	return render(request, page, content )
	

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))
