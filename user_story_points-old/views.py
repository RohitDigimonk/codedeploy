from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from .models import ArUserStoryPoints
from manage_product.models import AR_product
from manage_epic_capability.models import AR_EPIC_CAPABILITY

# Create your views here.
def index(request):
    story_point = ArUserStoryPoints.objects.all()
    return render(request, 'admin/user_story_points/index.html',{'date':datetime.now(),'story_point':story_point,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
