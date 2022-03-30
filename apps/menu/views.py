from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.userauth.models import UserProfile
from .models import Restaurant
from rest_framework.authtoken.models import Token

# Create your views here.
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
