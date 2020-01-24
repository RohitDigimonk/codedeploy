from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import Ar_User_Story_Form
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from account.models import Ar_user,AR_organization,ArShowcolumns,csvFilesUplodaded,Notification,ArUserStoryScoringPoints
from account.forms import csvFilesUplodadedForm
from .models import AR_USER_STORY
from django.contrib import messages
from datetime import datetime
from manage_role.models import ArRole
from manage_benefits.models import ArManageBenefits
from manage_goals.models import ArManageGoals
from manage_backlogs.models import AR_BACKLOG

import csv, io
from manage_product import views as product_view
# from manage_iterations.models import AR_ITERATIONS


@csrf_exempt
def get_file_data(request):
    id = force_text(urlsafe_base64_decode(request.POST["csv_id"]))
    file_name = ""
    if csvFilesUplodaded.objects.filter(id=id).exists():
        get_file = csvFilesUplodaded.objects.get(id=id)
        if get_file.ORG_ID.id != request.session['org_id']:
            messages.error(request, 'This CSV file is not related to your organization.')
        file_name = get_file.attachments
        data_set = file_name.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        get_data = csv.reader(io_string, delimiter=',', quotechar="|")
        get_data2 = ""
        file_name =  get_data
    else:
        messages.error(request, 'File id is invald')
    return render(request, 'admin/user_story_view/file_data.html',{'date':datetime.now(),'id':id,"file_name":file_name})

def add_csv_files(request):
    set_statue = ""
    csv_id = ""
    if request.method == "POST":
        csv_file = request.FILES['attachments']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            set_statue = urlsafe_base64_encode(force_bytes("error"))
        else:
            csvFilesUplodadedForm_get = csvFilesUplodadedForm(request.POST, request.FILES)
            if csvFilesUplodadedForm_get.is_valid():
                data = csvFilesUplodadedForm_get.save(commit=False)
                created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
                org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                data.csvUseFor = "Ar User Story"
                data.created_by = created_by_ins
                data.updated_by = created_by_ins
                data.ORG_ID = org_ins
                try:
                    data.save()
                    messages.info(request, "User Story CSV Uploded successfully !")
                    set_statue = urlsafe_base64_encode(force_bytes("done"))
                    csv_id = urlsafe_base64_encode(force_bytes(data.id))
                    return redirect(settings.BASE_URL + 'user-story-view')
                    # return redirect(settings.BASE_URL + 'user-story-view/' + set_statue + "/" + set_statue+"/"+csv_id)
                except IntegrityError:
                    messages.error(request, "Some thing was wrong !")
                    set_statue = urlsafe_base64_encode(force_bytes("error"))
            else:
                messages.error(request, csvFilesUplodadedForm_get.errors)
    # return redirect(settings.BASE_URL + 'user-story-view/'+set_statue+"/"+set_statue)
    return redirect(settings.BASE_URL + 'user-story-view')

# Create your views here.
def index(request,set_statue="",set_statue_2="",csv_id=""):
    if product_view.check_permition(request, 'User Story View', 0):
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        get_user_story = {};
        get_show_column = {};
        if AR_USER_STORY.objects.filter(ORG_id=org_ins).exists():
            get_user_story = AR_USER_STORY.objects.filter(ORG_id=org_ins)

        else:
            get_user_story = {}
        if ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id']).exists():
            show_column = ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id'])
            get_show_column = show_column[0].columnName.split(",")
        else:
            get_show_column = {}
        all_column_list = {
            "backlog_parent": "Backlog Parent",
            "owner":"Owner",
            "title":"Title",
            "story_tri_part_text":"Story Tri Part Text",
            "acceptance_criteria":"Acceptance Criteria",
            "ac_readability_score":"Ac Readability Score",
            "conversation":"Conversation",
            "convo_readability_score":"Convo Readability Score",
            "attachments":"Attachments",
            "autoscoring_on":"Autoscoring On",
            "archive_indicator":"Archive Indicator",
            "readiness_quality_score":"Readiness Quality Score",
            "story_points":"Story Points",
            "user_story_status":"User Story Status",
            "ORG_id":"ORG Name",
            "UST_ID":"User Story Type",
            "ar_user":"Ar User",
            "created_by":"Created By",
            "created_dt":"Created Date",
            "updated_by":"Updated_By",
            "updated_dt":"Updated Date"
        }
        csvFilesUplodadedForm_get = csvFilesUplodadedForm()
        return render(request, 'admin/user_story_view/index.html',{'date':datetime.now(),'csv_id':csv_id,'set_statue':set_statue,'set_statue_2':set_statue_2,'csvFilesUplodadedForm':csvFilesUplodadedForm_get,'all_column_list':all_column_list,'user_name':request.session['user_name'],'BASE_URL':settings.BASE_URL,'get_user_story':get_user_story,"get_show_column":get_show_column})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})
def add_user_story_view(request):
    if product_view.check_permition(request, 'User Story View', 1):
        Ar_Manage_Benefits = ArManageBenefits.objects.filter(ORG_ID=request.session['org_id'])
        Ar_Manage_Goals = ArManageGoals.objects.filter(ORG_ID=request.session['org_id'])
        Ar_Role = ArRole.objects.filter(ORG_ID=request.session['org_id'])
        if request.method == "POST":
            str_part = request.POST["str_part"]
            ar_user_story_form = Ar_User_Story_Form(request.session['org_id'], request.POST, request.FILES)
            if ar_user_story_form.is_valid():
                title = ar_user_story_form.cleaned_data.get('title')
                backlog_parent = ar_user_story_form.cleaned_data.get('backlog_parent')
                story_tri_part_text = ar_user_story_form.cleaned_data.get('story_tri_part_text')
                if story_tri_part_text == "":
                    story_tri_part_text=str_part

                if AR_USER_STORY.objects.filter(title=title).filter(ORG_id=request.session['org_id']).exists():
                    messages.error(request, "User story already exists.")
                else:
                    ############################################################
                    backlog = AR_BACKLOG.objects.get(title=backlog_parent)
                    if backlog.children_us_list == "":
                        child_us_list = title
                    else:
                        child_us_list = backlog.children_us_list + " | " + title
                    AR_BACKLOG.objects.filter(title=backlog_parent).update(
                        children_us_list=child_us_list)
                    ############################################################
                    data = ar_user_story_form.save(commit=False)
                    created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
                    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                    data.story_tri_part_text = story_tri_part_text
                    data.ORG_id = org_ins
                    data.created_by = created_by_ins
                    data.updated_by = created_by_ins
                    try:
                        data.save()
                        msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Add")
                        msg_data = msg[0].notification_desc
                        messages.info(request, msg_data)
                        # messages.info(request, "User Story added successfully !")
                        return redirect(settings.BASE_URL + 'user-story-view')
                    except IntegrityError:
                        messages.error(request, "Some thing was wrong !")
                return redirect(settings.BASE_URL+"user-story-view")
            else:
                messages.error(request,  ar_user_story_form.errors)
        else:
            val=request.session['org_id']

            ar_user_story_form = Ar_User_Story_Form(request.session['org_id'])
        return render(request, 'admin/user_story_view/add-user-story.html',{'Ar_Manage_Benefits':Ar_Manage_Benefits,'Ar_Manage_Goals':Ar_Manage_Goals,'Ar_Role':Ar_Role,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL,"ar_user_story_form":ar_user_story_form})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})
def edit_user_story_view(request,id):
    if product_view.check_permition(request, 'User Story View', 1):
        ar_user_story_form = AR_USER_STORY.objects.get(id=id)
        user_id=ar_user_story_form.id
        # current_user = request.user
        # current_user_id = current_user.id
        # org_info_user = AR_organization.objects.get(created_by=current_user_id)
        # org_id = org_info_user.id
        org_info = AR_organization.objects.filter(id=request.session['org_id'])
        if request.method == "POST":
            ar_user_story_form = Ar_User_Story_Form(request.session['org_id'], data=(request.POST or None),files=(request.FILES or None),instance = ar_user_story_form)
            if ar_user_story_form.is_valid():
                data = ar_user_story_form.save(commit=False)
                created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
                data.updated_by = created_by_ins
                data.updated_dt = datetime.now()
                try:
                    data.save()
                    msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Update")
                    msg_data = msg[0].notification_desc
                    messages.info(request, msg_data)
                    # messages.info(request, "User Story edit successfully !")
                    return redirect(settings.BASE_URL + 'user-story-view')
                except IntegrityError:
                    messages.error(request, "Some thing was wrong !")
                return redirect(settings.BASE_URL + 'user-story-view')
            else:
                messages.error(request,  ar_user_story_form.errors)
        else:
            ar_user_story_form = Ar_User_Story_Form(request.session['org_id'],instance=ar_user_story_form)
        return render(request, 'admin/user_story_view/edit-user-story.html',{'date':datetime.now(),'user_name':request.session['user_name'],'user_id':user_id,'ar_user_story_form':ar_user_story_form,'BASE_URL': settings.BASE_URL})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})
def delete_user_story_view(request,id):
    if product_view.check_permition(request, 'User Story View', 1):
        try:
            AR_USER_STORY.objects.get(id=id).delete()
            msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Remove")
            msg_data = msg[0].notification_desc
            messages.info(request, msg_data)
            # messages.info(request, "User story removed successsfully !")
            return redirect(settings.BASE_URL + 'user-story-view')
        except(TypeError, OverflowError):
            msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Remove_error")
            msg_data = msg[0].notification_desc
            messages.error(request, msg_data)
            # messages.error(request, "Maybe this user story is used in another table so we can not remove that !")
    else:
        msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Permission")
        msg_data = msg[0].notification_desc
        messages.error(request, msg_data)
        # messages.error(request, "You are not authorized person.")
    return redirect(settings.BASE_URL + 'user-story-view')


def select_user_story_view(request,ids):
    if product_view.check_permition(request, 'User Story View', 1):
        get_ids = ids.split(",")
        for id in get_ids:
            if AR_USER_STORY.objects.filter(id=id).exists():
                get_data_object =  AR_USER_STORY.objects.get(pk=id)
                get_data_object.pk = None
                get_data_object.save()
                messages.info(request, "Copy created successfully !")
            else:
                messages.error(request, " '"+str(id)+"' this story does not exist !")
    else:
        msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Permission")
        msg_data = msg[0].notification_desc
        messages.error(request, msg_data)
        # messages.error(request, "You are not authorized person.")
    return redirect(settings.BASE_URL + 'user-story-view')



def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_USER_STORY',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    msg = Notification.objects.filter(page_name="User Story View").filter(notification_key="Rearrange")
    msg_data = msg[0].notification_desc
    messages.info(request, msg_data)
    # messages.info(request, "Table column order rearrange successfully.")
    return redirect(settings.BASE_URL + 'user-story-view')


def get_data(request):
    if request.method == "POST":
        check_map = request.POST['check']
        check_map=check_map.lower()
        benefit_tag = ArUserStoryScoringPoints.objects.get(Score_key='Benefit_Tag')
        benefit_key = benefit_tag.Keyword
        benefit_key=benefit_key.lower()
        benefit_data = list(benefit_key.split(","))
        benefit_val = 0
        for benefit_str in benefit_data:
            if benefit_str in check_map:
                benefit_val = benefit_val + 1

        goal_tag = ArUserStoryScoringPoints.objects.get(Score_key='Goal_Tag')
        goal_key = goal_tag.Keyword
        goal_key = goal_key.lower()
        goal_data = list(goal_key.split(","))
        goal_val = 0
        for goal_str in goal_data:
            if goal_str in check_map:
                goal_val = goal_val + 1

        role_tag = ArUserStoryScoringPoints.objects.get(Score_key='Role_Tag')
        role_key = role_tag.Keyword
        role_key = role_key.lower()
        role_data = list(role_key.split(","))
        role_val = 0
        for role_str in role_data:
            if role_str in check_map:
                role_val = role_val + 1

        benefit_text = ArUserStoryScoringPoints.objects.get(Score_key='Benefit_text')
        benefit_text_key = benefit_text.Keyword
        benefit_text_key = benefit_text_key.lower()
        benefit_text_data = list(benefit_text_key.split(","))
        benefit_text_val = 0
        for benefit_text_str in benefit_text_data:
            if benefit_text_str in check_map:
                benefit_text_val = benefit_text_val + 1

        goal_text = ArUserStoryScoringPoints.objects.get(Score_key='Goal_text')
        goal_text_key = goal_text.Keyword
        goal_text_key = goal_text_key.lower()
        goal_text_data = list(goal_text_key.split(","))
        goal_text_val = 0
        for goal_text_str in goal_text_data:
            if goal_text_str in check_map:
                goal_text_val = goal_text_val + 1

        role_text = ArUserStoryScoringPoints.objects.get(Score_key='Role_text')
        role_text_key = role_text.Keyword
        role_text_key = role_text_key.lower()
        role_text_data = list(role_text_key.split(","))
        role_text_val = 0
        for role_text_str in role_text_data:
            if role_text_str in check_map:
                role_text_val = role_text_val + 1

        conjunction_set = ArUserStoryScoringPoints.objects.get(Score_key='Conjunction Set')
        conjunction_set_key = conjunction_set.Keyword
        benefit_key = benefit_key.lower()
        conjunction_set_data = list(conjunction_set_key.split(","))
        conjunction_set_val = 0
        for conjunction_set_str in conjunction_set_data:
            if conjunction_set_str in check_map:
                conjunction_set_val = conjunction_set_val + 1

        if conjunction_set_val == 0 :
            conjunction_set_scr = 10
        elif conjunction_set_val == 1 or conjunction_set_val == 2:
            conjunction_set_scr = 5
        else:
            conjunction_set_scr = 1

        if benefit_text_val == 0:
            benefit_text_scr = 1
        else:
            benefit_text_scr = 5

        if goal_text_val == 0:
            goal_text_scr = 2
        else:
            goal_text_scr = 10

        if role_text_val == 0:
            role_text_scr = 2
        else:
            role_text_scr = 10

        if benefit_val == 0:
            benefit_scr = 0
        else:
            benefit_scr = 10

        if goal_val == 0:
            goal_scr = 0
        else:
            goal_scr = 15

        if role_val == 0:
            role_scr = 0
        else:
            role_scr = 15

        Story_Tri_Part_Text = 25

        total_scr = conjunction_set_scr + benefit_text_scr + goal_text_scr + role_text_scr + benefit_scr + goal_scr + role_scr + Story_Tri_Part_Text

        return JsonResponse({'check_project': total_scr})