from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item
#from lists.model import * #import all table

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		#new_item_text = request.POST['item_text']
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	
	items = Item.objects.all()
	# start of tutorial 2 
	count_item = items.count()
	message = ''
	if count_item == 0:
		message = 'yey, waktunya berlibur'
	elif count_item > 0 and count_item < 5 :
		message = 'sibuk tapi santai'
	elif count_item > 4:
		message = 'oh tidak'
	
	# end of tutorial 2
	return render(request, 'home.html' ,{ 'items':items, 'message':message })
