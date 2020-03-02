from django.shortcuts import render,HttpResponse
from django.conf import settings
from user_story_view import set_user_story_acceptance_criteria_and_conver_algo as ACCA
# from account.forms import User_Form,AR_USER_Form
from django.core.mail import send_mail
import smtplib
import email.message
import stripe
from helpuser.models import Cms_manage
# Create your views here.


def handler404(request,exception):
    return render(request, 'web/error_page/page_404.html', {'BASE_URL':settings.BASE_URL})

def handler500(request):
    return render(request, 'web/error_page/page_500.html',  {'BASE_URL':settings.BASE_URL})



def test_data(request):
    return render(request, 'web/payment/stripe.html',  {'BASE_URL':settings.BASE_URL})

def login_page(request):
    return render(request, 'web/home/index.html', {'home_active': "active", 'BASE_URL': settings.BASE_URL,"set_login":"do_login"})


def contact_us(request):
    return render(request, 'web/home/contact_us.html', {'BASE_URL': settings.BASE_URL,"Contact_active":"active"})

def about_us(request):
    return render(request, 'web/home/about_us.html', {'BASE_URL': settings.BASE_URL,"about_active":"active"})

def eula(request):
    return render(request, 'web/home/eula.html', {'BASE_URL': settings.BASE_URL,"EULA_active":"active"})

def privacy(request):
    return render(request, 'web/home/privacy.html', {'BASE_URL': settings.BASE_URL,"Privacy_active":"active"})

def security(request):
    return render(request, 'web/home/security.html', {'BASE_URL': settings.BASE_URL,"Security_active":"active"})


def index(request):
    # 'user_form': User_Form, 'ar_user_form': AR_USER_Form,
    # if 'user_email' in request.session:
    #     return render(request, 'dashboard/dashboard_user/dashboard.html', {"message": "Logged in Successfully"})
    return render(request, 'web/home/index.html', {'home_active': "active", 'BASE_URL':settings.BASE_URL})

def whyar(request):
   
    return render(request, 'web/why-agile-ready/index.html', {'whyar_active': "active", 'BASE_URL':settings.BASE_URL})

def view_information(request,keyword):
    contecn = ""
    title = ""
    if Cms_manage.objects.filter(keyword=keyword).exists():
        get_data = Cms_manage.objects.get(keyword=keyword)
        contecn = get_data.help_description
        title = get_data.title

    return render(request, 'web/home/view-information.html', {'home_active': "active", 'BASE_URL':settings.BASE_URL,"contect":contecn,"title":title})


def company(request):

    return render(request, 'web/company/index.html', {'company_active': "active", 'BASE_URL':settings.BASE_URL})


def subscription(request):
    return render(request, 'web/subscriptions/index.html', {'subscription_active': "active", 'BASE_URL':settings.BASE_URL})


def usrating(request):
    return render(request, 'web/user-story-rating/index.html', {'usrating_active': "active", 'BASE_URL':settings.BASE_URL})




# def dashboard(request):
#     del request.session['user_email']
#     return render(request, 'basic/index.html', {'company_active': "active"})
