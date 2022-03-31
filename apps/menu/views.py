from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.userauth.models import UserProfile
from .models import Category, Restaurant
from rest_framework.authtoken.models import Token
from .forms import RestaurantForm
from address.models import Address

@login_required
def dashboard(request):
    context_dict = {}
    profile = UserProfile.objects.get(user=request.user)
    context_dict['profile'] = profile

    rest_owned = Restaurant.objects.filter(owner=profile)
    context_dict['rest_owned'] = rest_owned

    token_search = Token.objects.get_or_create(user=request.user)
    context_dict['auth_token'] = token_search[0]

    return render(request, 'menu/dashboard.html', context_dict)

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
def restaurant_read_categories(request, rest_id):
    context_dict = {}
    profile = UserProfile.objects.get(user=request.user)
    context_dict['profile'] = profile

    rest_owned = Restaurant.objects.get(id = rest_id)
    context_dict['rest_owned'] = rest_owned

    categories = Category.objects.filter(restaurant=rest_id)
    context_dict['categories'] = categories

    return render(request, 'menu/restaurant_read_categories.html', context_dict)

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
