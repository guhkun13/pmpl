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
	#content = {'items':items}
	return render(request, 'home.html',{'items':items})
