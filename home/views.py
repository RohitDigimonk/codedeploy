from django.shortcuts import render,HttpResponse
from django.conf import settings
from user_story_view import set_user_story_acceptance_criteria_and_conver_algo as ACCA
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
    text = "One hot day, a thirsty crow flew all over the fields looking for water. For a long time, he could not find any. He felt very weak, almost lost all hope. Suddenly, he saw a water jug below the tree. He flew straight down to see if there was any water inside. Yes, he could see some water inside the jug! The crow tried to push his head into the jug. Sadly, he found that the neck of the jug was too narrow. Then he tried to push the jug to tilt for the water to flow out, but the jug was too heavy. The crow thought hard for a while. Then, looking around it, he saw some pebbles. He suddenly had a good idea. He started picking up the pebbles one by one, dropping each into the jug. As more and more pebbles filled the jug, the water level kept rising. Soon it was high enough for the crow to drink. His plan had worked!"
    data = ACCA.break_sentences(text)  #    for sentences count
    # data = ACCA.word_count(text)
    words = len(text.split())  # for word count
    data = ACCA.sentence_count(text)   #  No. of sentences

    # data = sum(len(word) for word in words) / len(words)

    # data = ACCA.avg_sentence_length(text)
    # data = ACCA.syllables_count(text)
    # data = ACCA.avg_syllables_per_word(text)
    # data = ACCA.difficult_words(text)
    # data = ACCA.poly_syllable_count(text)
    # data = ACCA.flesch_reading_ease(text)
    return HttpResponse(data)
    # return render(request, 'web/why-agile-ready/index.html', {'whyar_active': "active", 'BASE_URL':settings.BASE_URL})

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
