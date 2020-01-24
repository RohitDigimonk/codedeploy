from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from account.models import Ar_user
from .models import ArFeedback
from datetime import datetime
from django.contrib import messages
from manage_backlogs.models import AR_BACKLOG
from manage_backlogs.forms import Ar_Backlog_Form
from account.models import AR_organization
from manage_epic_capability.models import AR_EPIC_CAPABILITY
from datetime import datetime


# Create your views here.
@login_required
def index(request):
    print("enter")
    if request.method == "POST":
        feed_nature = request.POST.get('feed_nature')
        feedback_page = request.POST.get('feedback_page')
        feedinformation = request.POST['feedinformation']
        feedback_file = request.FILES.get('feedback_file', False)
        created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
        today = datetime.now()
        val = today.strftime("%d_%m_%Y_%H_%M_%S_%f")
        if feedback_file is not False:
            filename = feedback_file.name
            splitedfilename = filename.split(".")
            length_of_filename = len(splitedfilename)
            file_extention = splitedfilename[length_of_filename - 1]
            upload_file_name = str(val) + "." + file_extention
            fs = FileSystemStorage()
            fs.save(upload_file_name, feedback_file)
        else:
            upload_file_name = ""
        entry_user = ArFeedback(page_name=feedback_page, feedback_nature=feed_nature, feedback_information=feedinformation,
                                attachments=upload_file_name,created_by=created_by_ins)
        entry_user.save()
        messages.info(request, "Feedback send successfully !")
        if feedback_page =="Manage Products":
            return redirect(settings.BASE_URL+'manage-products')
        elif feedback_page =="Manage Feature":
            return redirect(settings.BASE_URL + 'manage-feature')
        elif feedback_page =="Manage Epic Capabilities":
            return redirect(settings.BASE_URL + 'manage-epic-capabilities')
        elif feedback_page =="Manage Team":
            return redirect(settings.BASE_URL + 'manage-team')
        elif feedback_page =="Manage Backlog":
            return redirect(settings.BASE_URL + 'manage-backlog')
        elif feedback_page =="Manage Team Member":
            return redirect(settings.BASE_URL + 'manage-team-member')
        elif feedback_page =="Manage User Story Point":
            return redirect(settings.BASE_URL + 'user-story-points')
        elif feedback_page =="Invite User":
            return redirect(settings.BASE_URL + 'invite-user')
        elif feedback_page =="User Profile":
            return redirect(settings.BASE_URL + 'user-profile')
        elif feedback_page =="Dashboard":
            return redirect(settings.BASE_URL + 'dashboard')
        elif feedback_page =="User Story View":
            return redirect(settings.BASE_URL + 'user-story-view')
        elif feedback_page =="Product View":
            return redirect(settings.BASE_URL + 'product-view')
        elif feedback_page == "Backlog View":
            return redirect(settings.BASE_URL + 'backlog-view')
        elif feedback_page == "Account Settings":
            return redirect(settings.BASE_URL + 'account-settings')

    return render(request, 'admin/backlog_view/index.html',{'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
