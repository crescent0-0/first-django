from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg

from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from third.models import Restaurant, Review

# Create your views here.
def list(request):
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
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
        password = request.POST.get('password','')
        form = UpdateRestaurantForm(request.POST, instance=item)
        
        if form.is_valid() and password == item.password:
            item = form.save()
            
    elif request.method == 'GET':
        item = get_object_or_404(Restaurant,pk=request.GET.get('id'))  # third/update?id=2 -> 이런식으로 데이터가 들어오는 경우
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html',{ 'form':form})
    
    return HttpResponseRedirect('/third/list/')


def detail(request, id):
    if 'id' is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        context={
            'item': item,
            'reviews': reviews,
        }
        
        return render(request, 'third/detail.html', context)
    
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail',id=id)
    
    return render(request, 'third/delete.html', { 'item':item })


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id=restaurant_id)
    
    item=get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    
    context ={
        'item': item,
        'form': form,
    }
    return render(request, 'third/review_create.html',context)


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()
    
    return redirect('restaurant-detail',id=restaurant_id)


def review_list(request):
    #reviews = Review.objects.all().order_by('-created_at')                   # join X : 리뷰 갯수만큼 쿼리가 요청됨
    reviews = Review.objects.all().select_related().order_by('-created_at')   # join O : 한번의 쿼리만 보내짐
    paginator = Paginator(reviews,3)
    
    page = request.GET.get('page')
    items = paginator.get_page(page)
    pages = range(1,paginator.num_pages+1);
    
    context = {
        'reviews': items,
        'page': pages,
    }
    
    return render(request,'third/review_list.html',context)