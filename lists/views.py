from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    '''домашняя страница'''

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the_best_link/')

    return render(request, 'home.html')

def view_list(request):
    '''новый список'''
    
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})