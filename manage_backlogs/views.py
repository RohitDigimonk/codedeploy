from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import Ar_Backlog_Form
from .models import AR_BACKLOG
from django.contrib import messages
from account.models import AR_organization,Ar_user,ArShowcolumns
from datetime import datetime
import csv

# Create your views here.

##################################View##############################
def backlogview(request):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])

    backlog_data = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
    ar_backlog_form = Ar_Backlog_Form(org_info)
    return render(request, 'admin/backlog_view/index.html',{'ar_backlog_form':ar_backlog_form,'date':datetime.now(),'backlog_data':backlog_data,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

################################################################
def index(request):
    ##################################################################333333333333

    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    ar_backlog_form = Ar_Backlog_Form(org_info)
    ar_backlog = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
    ######################################
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    ##############################################
    if AR_BACKLOG.objects.filter(ORG_ID=org_ins).exists():
        all_backlog_get = AR_BACKLOG.objects.filter(ORG_ID=org_ins).order_by("-id")
    else:
        all_backlog_get = {}

    if ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).exists():
        show_column = ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id'])
        get_show_column = show_column[0].columnName.split(",")
    else:
        get_show_column = {}

    all_column_list = {
        "team_list": "Team List",
        "product_parent": "product Parent",
        "title": "Title",
        "children_us_list": "Children Us List",
        "owner": "Owner",
        "backlog_score": "Backlog Score",
        "Backlog_size": "Backlog Size",
        "BL_STATUS": "Backlog Status",
        "ORG_ID": "ORG Name",
        "created_by": "Created By",
        "created_dt": "Created Date",
        "updated_by": "Updated By",
        "updated_dt": "Updated Date",
    }
    ##########################################################
    ##################################################################333333333333
    return render(request, 'admin/manage_backlogs/index.html',{'all_column_list':all_column_list,'get_show_column':get_show_column,'all_backlog_get':all_backlog_get,'date':datetime.now(),'ar_backlog':ar_backlog,'ar_backlog_form':ar_backlog_form,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})


def add_backlog(request):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    #####################################
    if request.method == "POST":
        ar_backlog_form = Ar_Backlog_Form(org_info,request.POST)
        if ar_backlog_form.is_valid():
            title = ar_backlog_form.cleaned_data.get('title')
            if AR_BACKLOG.objects.filter(title=title).filter(ORG_ID=request.session['org_id']).exists():
                messages.error(request, "Backlog already exists.")
            else:
                created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
                org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
                data = ar_backlog_form.save(commit=False)
                data.created_by=created_by_ins
                data.updated_by = created_by_ins
                data.backlog_score = 0
                data.Backlog_size = 0
                data.ORG_ID=org_ins
                try:
                    data.save()
                    messages.info(request, "Backlog added successfully !")
                    return redirect(settings.BASE_URL + 'manage-backlog')
                except:
                    messages.error(request, ar_backlog_form.errors)


        else:
            messages.error(request, ar_backlog_form.errors)
    else:
        ar_backlog_form=Ar_Backlog_Form(org_info)
    return redirect(settings.BASE_URL + 'manage-backlog')


def edit_backlog(request,id):
    ##################################################################333333333333
    ######################################
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    ##############################################
    if AR_BACKLOG.objects.filter(ORG_ID=org_ins).exists():
        all_backlog_get = AR_BACKLOG.objects.filter(ORG_ID=org_ins).order_by("-id")
    else:
        all_backlog_get = {}

    if ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).exists():
        show_column = ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id'])
        get_show_column = show_column[0].columnName.split(",")
    else:
        get_show_column = {}

    all_column_list = {
        "title": "Title",
        "children_us_list": "Children Us List",
        "owner": "Owner",
        "backlog_score": "Backlog Score",
        "Backlog_size": "Backlog Size",
        "team_list": "Team List",
        "product_parent": "product Parent",
        "BL_STATUS": "Backlog Status",
        "ORG_ID": "ORG Name",
        "created_by": "Created By",
        "created_dt": "Created Date",
        "updated_by": "Updated By",
        "updated_dt": "Updated Date",
    }
    ##########################################################

    ##################################################################333333333333
    ar_backlog = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
    #######################################
    backlog_form = AR_BACKLOG.objects.get(id=id)
    backlog_id=backlog_form.id
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    if request.method == "POST":
        backlog_form = Ar_Backlog_Form( data=(request.POST or None),org_info=org_info,instance = backlog_form)
        if backlog_form.is_valid():
            try:
                backlog_form.save()
                messages.info(request, "Backlog update successfully !")
                return redirect(settings.BASE_URL + 'manage-backlog')
            except:
                messages.error(request,  backlog_form.errors)
        else:
            messages.error(request,  backlog_form.errors)
    else:
        backlog_form = Ar_Backlog_Form(instance=backlog_form,org_info=org_info)
    #######################################
    return render(request, 'admin/manage_backlogs/index.html',{'all_column_list':all_column_list,'get_show_column':get_show_column,'all_backlog_get':all_backlog_get,'date':datetime.now(),'backlog_edit':"value",'ar_backlog':ar_backlog,'backlog_id':backlog_id,'ar_backlog_edit_form':backlog_form,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})


def delete_backlog(request,id):
    AR_BACKLOG.objects.get(id=id).delete()
    messages.info(request, "Backlog removed !")
    return redirect(settings.BASE_URL + 'manage-backlog')


def export_backlog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Backlog.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['ID','Title', 'Children us List', 'User Story List', 'Owner',
                                                 'Auto Score Flag',
                                                 'Backlog Score', 'Backlog Size', 'Backlog Scoring History', 'Team List', 'Product Parent',
                                                 'Iteration', 'Backlog Status',
                                                 'ORG ID', 'Created By','Created Date','Updated By','Updated Date'])
    users = AR_BACKLOG.objects.all().values_list('id','title', 'children_us_list', 'user_story_list', 'owner',
                                                 'auto_score_flag',
                                                 'backlog_score', 'Backlog_size', 'bl_scoring_history', 'team_list', 'product_parent',
                                                 'iteration', 'BL_STATUS',
                                                 'ORG_ID', 'created_by','created_dt','updated_by','updated_dt')
    for user in users:
        writer.writerow(user)
    return response


#####################################
def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_BACKLOG',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    messages.info(request, "Table structure updated successfully.")
    return redirect(settings.BASE_URL + 'backlog-view')