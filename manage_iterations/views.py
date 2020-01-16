from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import IterationForm
from account.models import AR_organization,Ar_user,ArShowcolumns
from manage_backlogs.models import AR_BACKLOG
from .models import ArIterations
from manage_product.models import AR_product
from user_story_view.models import AR_USER_STORY
from django.contrib import messages
from django.utils.dateparse import parse_date
import datetime
import string
import random
# Create your views here.


@csrf_exempt
def get_backlogs(request):
    product_id = request.POST["product_id"]
    instance_product = get_object_or_404(AR_product, pk=product_id)
    get_backlog = {}
    if AR_BACKLOG.objects.filter(product_parent=instance_product).exists():
        get_backlog = AR_BACKLOG.objects.filter(product_parent=instance_product)
    else:
        get_backlog = {}
    return  render(request, 'admin/iterations/get_backlog.html',{"backlog_data":get_backlog})

@csrf_exempt
def get_user_story(request):
    get_backlog_id = request.POST["get_backlog_id"]
    instance_of_backlog = get_object_or_404(AR_BACKLOG, pk=get_backlog_id)
    get_userstory = {}
    if AR_USER_STORY.objects.filter(backlog_parent=instance_of_backlog).exists():
        get_userstory = AR_USER_STORY.objects.filter(backlog_parent=instance_of_backlog)
    else:
        get_userstory = {}
    return render(request, 'admin/iterations/get_user_storyes.html', {"user_story_data": get_userstory})

def index(request):
    org_info_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    get_all_iterations = {}
    if ArIterations.objects.filter(ORG_ID=org_info_ins).exists():
        get_all_iterations = ArIterations.objects.filter(ORG_ID=org_info_ins)
    else:
        get_all_iterations = {}
    if ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id']).exists():
        show_column = ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id'])
        get_show_column = show_column[0].columnName.split(",")
    else:
        get_show_column = {}
    all_column_list = {
        "IterationId": "Iteration Id",
        "IterationName": "Iteration Name",
        "Product": "Product",
        "Backlog": "Backlog",
        "owner": "Owner",
        "StartDate": "Start Date",
        "EndDate": "End Date",
        "Description": "Description",
        "UserStory": "User Story",
        "Team": "Team",
        "IterationScore": "Iteration Score",
        "IterationSize": "Iteration Size",
        "ORG_ID": "ORG ID",
        "create_by": "Created By",
        "create_dt": "Created Date",
        "update_by": "Updated_By",
        "update_dt": "Updated Date"
    }
    return render(request, 'admin/iterations/index.html',{'all_column_list':all_column_list,'get_show_column':get_show_column,'get_all_iterations':get_all_iterations,'user_name': request.session['user_name'], 'BASE_URL': settings.BASE_URL})



def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='ArIterations',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    messages.info(request, "Table structure updated successfully.")
    return redirect(settings.BASE_URL + 'iteration-view')

def edit_iteration(request,id):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    IterationInfo = get_object_or_404(ArIterations, pk=id)

    if request.method == 'POST':
        IterationForm_get = IterationForm(org_info, request.POST, instance=IterationInfo)
        if IterationForm_get.is_valid():
            IterationForm_get_commit = IterationForm_get.save(commit=False)
            StartDate = request.POST.get('StartDate')
            StartDateSet = datetime.datetime.strptime(StartDate, "%m/%d/%Y %I:%M %p")
            EndDate = request.POST.get('EndDate')
            EndDateSet = datetime.datetime.strptime(StartDate, "%m/%d/%Y %I:%M %p")
            IterationForm_get_commit.StartDate = StartDateSet
            IterationForm_get_commit.EndDate = EndDateSet
            try:
                IterationForm_get_commit.save()
                IterationForm_get.save_m2m()
                messages.info(request, "Iteration Update successfully !")
                return redirect(settings.BASE_URL + "iteration-view")
            except:

                messages.error(request, IterationForm_get.errors)
        else:
            messages.error(request, IterationForm_get.error)
    else:
        IterationForm_get = IterationForm(org_info, instance=IterationInfo)
        start_data = IterationInfo.StartDate.strftime('%m/%d/%Y %h:%i %a')
        end_data = IterationInfo.EndDate.strftime('%m/%d/%Y %h:%i %a')
    return render(request, 'admin/iterations/edit_iteration.html',{'start_data':start_data,'end_data':end_data,'IterationForm': IterationForm_get, 'user_name': request.session['user_name'],'BASE_URL': settings.BASE_URL})



def remove_iteration(request,id):
    try:
        ArIterations.objects.get(pk=id).delete()
        messages.info(request, "Iterations removed !")
    except(TypeError):
        messages.error(request, "Maybe this iterations is used in another table so we can not remove that !")
    return redirect(settings.BASE_URL + 'iteration-view')


def add_iteration(request):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    if request.method == 'POST':
        IterationForm_get = IterationForm(org_info, request.POST)
        if IterationForm_get.is_valid():
            IterationName = IterationForm_get.cleaned_data.get('IterationName')
            if ArIterations.objects.filter(IterationName=IterationName).filter(ORG_ID=request.session['org_id']).exists():
                messages.error(request, "Iteration Name already exists.")
            else:

                IterationId = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                while ArIterations.objects.filter(IterationId=IterationId).exists():
                    IterationId = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

                IterationForm_data = IterationForm_get.save(commit=False)
                ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                # StartDate = request.POST.get('StartDate')
                StartDate = request.POST.get('StartDate')
                StartDateSet = datetime.datetime.strptime(StartDate, "%m/%d/%Y %I:%M %p")
                EndDate = request.POST.get('EndDate')
                EndDateSet = datetime.datetime.strptime(StartDate, "%m/%d/%Y %I:%M %p")

                org_info_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])

                IterationForm_data.IterationId = IterationId
                IterationForm_data.StartDate = StartDateSet
                IterationForm_data.EndDate = EndDateSet
                IterationForm_data.ORG_ID = org_info_ins
                IterationForm_data.create_by = ar_user_insta
                IterationForm_data.update_by = ar_user_insta
                try:
                    IterationForm_data.save()
                    IterationForm_get.save_m2m()
                    messages.info(request, "Iteration added successfully !")
                    return redirect(settings.BASE_URL + "iteration-view")
                except:
                    messages.error(request, IterationForm_get.errors)
        else:
            messages.error(request, IterationForm_get.errors)
    else:

        IterationForm_get = IterationForm(org_info)
    return render(request, 'admin/iterations/add_iteration.html',{'IterationForm':IterationForm_get,'user_name': request.session['user_name'], 'BASE_URL': settings.BASE_URL})