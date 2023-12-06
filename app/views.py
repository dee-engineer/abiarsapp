from django.shortcuts import redirect, render
from .models import User, Category
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
import requests
from django.conf import settings
import logging
from django.views.decorators.csrf import csrf_exempt



logger = logging.getLogger(__name__)

def initiate_payment(request):
    if request.method == 'POST':
        try:
            payload = {
                "email": request.user.email,
                "amount": float(request.POST.get('amount'))*100,
                "reference": request.user.tax_id,
                "currency": "NGN",
                "callback_url": "https.google.com/",
            }

            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                f"{settings.PAYSTACK_PAYMENT_URL}/transaction/initialize",
                json=payload,
                headers=headers,
            )

            if response.status_code == 200:
                data = response.json()
                authorization_url = data.get('data', {}).get('authorization_url')
                if authorization_url:
                    return redirect(authorization_url)
                else:
                    logger.error('Authorization URL not found in Paystack response')
                    return render(request, 'error.html', {'message': 'Authorization URL not found'})
            else:
                logger.error(f'Failed to initiate payment: {response.status_code}')
                return render(request, 'error.html', {'message': 'Failed to initiate payment'})

        except Exception as e:
            logger.exception(f'Error during payment initiation: {e}')
            return render(request, 'error.html', {'message': 'An unexpected error occurred'})

    return render(request, 'payment_form.html')



@csrf_exempt
def payment_callback(request):
    transaction_reference = request.GET.get('reference')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"{settings.PAYSTACK_PAYMENT_URL}/transaction/verify/{transaction_reference}",
        headers=headers,
    )

    if response.status_code == 200:
        payment_data = response.json()
        status = payment_data.get('data', {}).get('status')
        if status == 'success':
            user = User.objects.get(tax_id=transaction_reference)
            user.is_paid = True
            user.save()

            print('Payment successful by ' + user.first_name)
            return redirect('home')



def paystack(request):
    return render(request, 'paystack.html')


def index(request):
    return render(request, 'index.html')


def userlogin(request):
    if request.method == 'POST':
        tax_id = request.POST.get('tax_id')
        password = request.POST.get('password')

        print(tax_id, password)
        user = authenticate(
            request,
            tax_id=tax_id,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('userlogin')
    return render(request, 'userlogin.html')


def userregister(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')
        gender = request.POST.get('gender')
        category = Category.objects.get(name=request.POST.get('category'))
        image = request.POST.get('image')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            gender=gender,
            category=category,
            image=image
        )
        user.set_password(password)
        user.save()
        authenticated_user = authenticate(request, tax_id=user.tax_id, password=password)
        if authenticated_user:
            login(request, authenticated_user)
            return redirect('home')

    categories = Category.objects.all()
    return render(request, 'register.html', {'categories': categories})


def home(request):
    return render(request, 'home.html')


def userlogout(request):
    logout(request)
    return redirect('index')
