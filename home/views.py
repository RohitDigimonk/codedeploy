from django.shortcuts import render
from django.conf import settings
# from account.forms import User_Form,AR_USER_Form
from django.core.mail import send_mail
import smtplib
import email.message
# Create your views here.

def login_page(request):
    return render(request, 'web/home/index.html', {'home_active': "active", 'BASE_URL': settings.BASE_URL,"set_login":"do_login"})


def index(request):
    # 'user_form': User_Form, 'ar_user_form': AR_USER_Form,
    # if 'user_email' in request.session:
    #     return render(request, 'dashboard/dashboard_user/dashboard.html', {"message": "Logged in Successfully"})
    return render(request, 'web/home/index.html', {'home_active': "active", 'BASE_URL':settings.BASE_URL})

def whyar(request):
    return render(request, 'web/why-agile-ready/index.html', {'whyar_active': "active", 'BASE_URL':settings.BASE_URL})

def view_information(request):
    return render(request, 'web/home/view-information.html', {'home_active': "active", 'BASE_URL':settings.BASE_URL})


def company(request):

    return render(request, 'web/company/index.html', {'company_active': "active", 'BASE_URL':settings.BASE_URL})


def subscription(request):
    return render(request, 'web/subscriptions/index.html', {'subscription_active': "active", 'BASE_URL':settings.BASE_URL})


def usrating(request):
    return render(request, 'web/user-story-rating/index.html', {'usrating_active': "active", 'BASE_URL':settings.BASE_URL})




# def dashboard(request):
#     del request.session['user_email']
#     return render(request, 'basic/index.html', {'company_active': "active"})
