from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from account.models import Ar_user
from .models import ArFeedback, ArSendFeedbackEmail
from datetime import datetime
from django.contrib import messages
from manage_backlogs.models import AR_BACKLOG
from manage_backlogs.forms import Ar_Backlog_Form
from account.models import AR_organization,Notification
from manage_epic_capability.models import AR_EPIC_CAPABILITY
from datetime import datetime
from django.template.loader import render_to_string
import email.message
import smtplib
import django
# Create your views here.
def sent_feedback_email(request):
    get_data = ArSendFeedbackEmail.objects.filter(status=False)
    if get_data:
        data_content = {"user_name":"Admin","logo_image":settings.BASE_URL+"static/img/basic/logo.png","get_data":get_data}
        email_content = render_to_string('email_template/email_sent_for_feedback_template.html', data_content)
        user_email = "feedback@agileready.net"
        msg = email.message.Message()
        msg['Subject'] = 'beagileready Feedback'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user_email
        password = settings.EMAIL_HOST_PASSWORD
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        get_data.update(status=True,sent_date=django.utils.timezone.now())
    return HttpResponse("True")

def function_feedback_sent(feedback_page, entry_user,created_by_ins):
    default = 'Test'
    entry_feedback_sent = ArSendFeedbackEmail(page_name=feedback_page, feedback_id=entry_user, user_id=created_by_ins)
    entry_feedback_sent.save()

    return True


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

        # ___________________________________ feedback store for send mail ___________________________________

        data_res = function_feedback_sent(feedback_page, entry_user,created_by_ins)

        # ____________________________________________________________________________________________________
        msg = Notification.objects.filter(page_name="Feedback").filter(notification_key="Send")
        msg_data = msg[0].notification_desc
        messages.info(request, msg_data)
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
            return redirect(settings.BASE_URL + 'products-view')
        elif feedback_page == "Backlog View":
            return redirect(settings.BASE_URL + 'backlog-view')
        elif feedback_page == "Iteration View":
            return redirect(settings.BASE_URL + 'iteration-view')
        elif feedback_page == "Manage Iteration":
            return redirect(settings.BASE_URL + 'manage-iteration')
        elif feedback_page == "Manage Roles":
            return redirect(settings.BASE_URL + 'manage-role')
        elif feedback_page == "Manage Goal":
            return redirect(settings.BASE_URL + 'manage-goals')
        elif feedback_page == "Manage Benefits":
            return redirect(settings.BASE_URL + 'manage-benefits')
        elif feedback_page == "Manage User Story Point":
            return redirect(settings.BASE_URL + 'user-story-points')
        elif feedback_page == "Account Settings":
            return redirect(settings.BASE_URL + 'account-settings')

    return render(request, 'admin/backlog_view/index.html',{'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
