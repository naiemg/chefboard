from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.userauth.models import UserProfile
from .models import Category, Restaurant
from .forms import RestaurantForm, CategoryForm
from address.models import Address
from apps.menu.decorators import user_is_owner

@login_required
def dashboard(request):
    context_dict = {}
    profile = UserProfile.objects.get(user=request.user)
    context_dict['profile'] = profile

    rest_owned = Restaurant.objects.filter(owner=profile)
    context_dict['rest_owned'] = rest_owned

    return render(request, 'menu/dashboard.html', context_dict)

@login_required
def restaurant_create(request):
    context_dict = {}

    addresses = Address.objects.all()
    if settings.GOOGLE_API_KEY:
        google_api_key_set = True
    else:
        google_api_key_set = False

    
    profile = UserProfile.objects.get(user=request.user)
        
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = UserProfile.objects.get(user=request.user)
            post.save()
            return redirect('dashboard')
    else:
        form = RestaurantForm()
    
    context_dict = {
        "form": form,
        "google_api_key_set": google_api_key_set,
        "profile": profile,
        "addresses": addresses,
    }

    return render(request, 'menu/restaurant_create.html', context_dict)

@login_required
@user_is_owner
def restaurant_read_categories(request, rest_id):
    context_dict = {}
    profile = UserProfile.objects.get(user=request.user)
    context_dict['profile'] = profile

    rest_owned = Restaurant.objects.get(id = rest_id)
    context_dict['rest_owned'] = rest_owned

    categories = Category.objects.filter(restaurant=rest_id)
    context_dict['categories'] = categories

    return render(request, 'menu/restaurant_read_categories.html', context_dict)

@login_required
@user_is_owner
def restaurant_update(request, rest_id):
    context_dict = {}

    addresses = Address.objects.all()
    if settings.GOOGLE_API_KEY:
        google_api_key_set = True
    else:
        google_api_key_set = False

    restaurant = get_object_or_404(Restaurant, id=rest_id)
    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = UserProfile.objects.get(user=request.user)
            post.save()
            return redirect('dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    context_dict = {
        "form": form,
        "google_api_key_set": google_api_key_set,
        "addresses": addresses,
    }

    return render(request, 'menu/restaurant_update.html', context_dict)

@login_required
@user_is_owner
def restaurant_delete(request, rest_id):
    restaurant = get_object_or_404(Restaurant, id=rest_id)
    restaurant.delete()
    return redirect('dashboard')

@login_required
@user_is_owner
def category_create(request, rest_id):
    context_dict = {}

    restaurant = get_object_or_404(Restaurant, id=rest_id)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.restaurant = restaurant
            post.save()
            return redirect('restaurant_read_categories', rest_id=rest_id)
    else:
        form = CategoryForm()

    context_dict = {
        "form": form,
        "restaurant": restaurant,
    }

    return render(request, 'menu/category_create.html', context_dict)

@login_required
@user_is_owner
def category_read(request, rest_id, cat_id):
    context_dict = {}

    restaurant = get_object_or_404(Restaurant, id=rest_id)
    category = get_object_or_404(Category, id=cat_id)
    context_dict['restaurant'] = restaurant
    context_dict['category'] = category
    return render(request, 'menu/category_read.html', context_dict)

@login_required
@user_is_owner
def category_update(request, rest_id, cat_id):
    context_dict = {}

    restaurant = get_object_or_404(Restaurant, id=rest_id)
    category = get_object_or_404(Category, id=cat_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            post = form.save(commit=False)
            post.restaurant = restaurant
            post.save()
            return redirect('restaurant_read_categories', rest_id=rest_id)
    else:
        form = CategoryForm(instance=category)

    context_dict = {
        "form": form,
        "restaurant": restaurant,
    }

    return render(request, 'menu/category_update.html', context_dict)