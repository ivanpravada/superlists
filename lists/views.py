from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List

User = get_user_model()

def home_page(request):
    '''домашняя страница'''

    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    '''представление список'''
    
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    '''новый список 2'''
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

def my_lists(request, email):
    '''Мои списки'''

    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})