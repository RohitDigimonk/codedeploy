from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),

    path('sent-feedback-email', views.sent_feedback_email, name='sent_feedback_email'),

]