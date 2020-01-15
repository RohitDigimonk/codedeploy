from django.shortcuts import render, HttpResponse,get_object_or_404,redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import Ar_User_Story_Form
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from account.models import Ar_user,AR_organization,ArShowcolumns,csvFilesUplodaded
from account.forms import csvFilesUplodadedForm
from .models import AR_USER_STORY
from django.contrib import messages
from datetime import datetime
import csv, io

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

def add_user_story_view(request):
    if request.method == "POST":
        ar_user_story_form = Ar_User_Story_Form(request.session['org_id'], request.POST, request.FILES)
        if ar_user_story_form.is_valid():
            title = ar_user_story_form.cleaned_data.get('title')
            if AR_USER_STORY.objects.filter(title=title).filter(ORG_id=request.session['org_id']).exists():
                messages.error(request, "User story already exists.")
            else:
                data = ar_user_story_form.save(commit=False)
                created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
                org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                data.ORG_id = org_ins
                data.created_by = created_by_ins
                data.updated_by = created_by_ins
                try:
                    data.save()
                    messages.info(request, "User Story added successfully !")
                    return redirect(settings.BASE_URL + 'user-story-view')
                except IntegrityError:
                    messages.error(request, "Some thing was wrong !")
            return redirect(settings.BASE_URL+"user-story-view")
        else:
            messages.error(request,  ar_user_story_form.errors)
    else:
        val=request.session['org_id']
        ar_user_story_form = Ar_User_Story_Form(request.session['org_id'])
    return render(request, 'admin/user_story_view/add-user-story.html',{'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL,"ar_user_story_form":ar_user_story_form})

def edit_user_story_view(request,id):
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
            try:
                data.save()
                messages.info(request, "User Story edit successfully !")
                return redirect(settings.BASE_URL + 'user-story-view')
            except IntegrityError:
                messages.error(request, "Some thing was wrong !")
            return redirect(settings.BASE_URL + 'user-story-view')
        else:
            messages.error(request,  ar_user_story_form.errors)
    else:
        ar_user_story_form = Ar_User_Story_Form(request.session['org_id'],instance=ar_user_story_form)
    return render(request, 'admin/user_story_view/edit-user-story.html',{'date':datetime.now(),'user_name':request.session['user_name'],'user_id':user_id,'ar_user_story_form':ar_user_story_form,'BASE_URL': settings.BASE_URL})

def delete_user_story_view(request,id):
    try:
        AR_USER_STORY.objects.get(id=id).delete()
        messages.info(request, "User story removed successsfully !")
        return redirect(settings.BASE_URL + 'user-story-view')
    except(TypeError, OverflowError):
        messages.error(request, "Maybe this user story is used in another table so we can not remove that !")
    return redirect(settings.BASE_URL + 'user-story-view')


def select_user_story_view(request,ids):
    get_ids = ids.split(",")
    for id in get_ids:
        if AR_USER_STORY.objects.filter(id=id).exists():
            get_data_object =  AR_USER_STORY.objects.get(pk=id)
            get_data_object.pk = None
            get_data_object.save()
            messages.info(request, "Copy created successfully !")
        else:
            messages.error(request, " '"+str(id)+"' this story does not exist !")
    return redirect(settings.BASE_URL + 'user-story-view')



def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_USER_STORY').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_USER_STORY',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    messages.info(request, "Table structure updated successfully. !")
    return redirect(settings.BASE_URL + 'user-story-view')