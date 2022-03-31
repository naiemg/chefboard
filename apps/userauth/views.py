# django imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# model imports
from apps.userauth.models import UserProfile, StripeCustomer
from apps.userauth.forms import UserForm, UserProfileForm

import stripe

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

@login_required
def profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user=request.user)
    token_search = Token.objects.get_or_create(user=request.user)

    try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'userauth/profile.html', {
            'subscription': subscription,
            'product': product,
            'current_user': current_user,
            'profile': profile,
            'auth_token': token_search[0],
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'userauth/profile.html', {
            'current_user': current_user,
            'profile': profile,
            'auth_token': token_search[0],
    })

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required
def success(request):
    return render(request, 'userauth/success.html')

@login_required
def cancel(request):
    return render(request, 'userauth/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
