# django imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# model imports
from apps.userauth.models import UserProfile
from apps.userauth.forms import UserForm, UserProfileForm

def user_register(request):
    # If user already logged in, take user to dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        pass

    # registered flag indicating that a user has NOT been created
    registered = False

    # Two forms are utilized to process user registration
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)	# Handles authentication
        user_profile_form = UserProfileForm(data=request.POST) # Handles profile

        # If all three forms are valid, then post the data back to the database
        if user_form.is_valid() and user_profile_form.is_valid():
            usr = user_form.save()
            usr.set_password(usr.password)
            usr.save()

            profile = user_profile_form.save(commit=False)
            profile.user = usr
            profile.save()

            registered = True

            # Upon creating an account, redirect to the login page
            return HttpResponseRedirect('/login/')

        else:
            # display error message upon recieving bad input
            print(user_form.errors, user_profile_form.errors)

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context_dict = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'registered': registered,
    }
    return render(request, 'userauth/register.html', context_dict)

def user_login(request):
    # If already logged in, take user to dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        pass

    # Prompt user for login credentials
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return(HttpResponse("Your Account is disabled"))
        else:
            # Redirect to login page if information is incorrect
            # Prmpt users to re enter login information
            return render(request, "userauth/login.html", {'invalid': True })

    else:
        return render(request, 'userauth/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required
def dashboard(request):
    context_dict = {}

    current_user = request.user
    context_dict['current_user'] = current_user
    
    profile = UserProfile.objects.get(user=request.user)
    context_dict['profile'] = profile

    return render(request, 'userauth/dashboard.html', context_dict)
