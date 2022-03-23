from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from third.forms import RestaurantForm
from third.models import Restaurant

# Create your views here.
def list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 3)
    
    page = request.GET.get('page')
    items = paginator.get_page(page)
    pages = range(1,items.paginator.num_pages+1);
    
    context ={
        'restaurants': items,
        'page': pages,
    }
    
    return render(request, 'third/list.html',context)

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list/')
    
    form = RestaurantForm()
    return  render(request, 'third/create.html', {'form':form})


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        # item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant,pk=request.POST.get('id'))
        form = RestaurantForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            
    elif request.method == 'GET':
        item = get_object_or_404(Restaurant,pk=request.GET.get('id'))  # third/update?id=2 -> 이런식으로 데이터가 들어오는 경우
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html',{ 'form':form})
    
    return HttpResponseRedirect('/third/list/')

def detail(request):
    if 'id' in request.GET:
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        return render(request, 'third/detail.html', { 'item':item })
    
    return HttpResponseRedirect('third/list/')


def delete(request):
    if 'id' in request.GET:
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        item.delete()
    
    return HttpResponseRedirect('/third/list/')