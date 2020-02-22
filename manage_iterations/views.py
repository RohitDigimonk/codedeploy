from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import IterationForm
from account.models import AR_organization, Ar_user, ArShowcolumns, Notification
from manage_backlogs.models import AR_BACKLOG
from .models import ArIterations
from manage_product.models import AR_product,AR_team
from user_story_view.models import AR_USER_STORY
from django.contrib import messages
from django.utils.dateparse import parse_date
from datetime import datetime
import string
import random
from manage_product import views as product_view


# Create your views here.

@csrf_exempt
def get_storyes_scores_and_size(request):
    get_ids = request.POST["storyes_ids"].split(",")
    get_score = 0
    get_size = 0
    get_count_of_storyes = len(get_ids)
    for id in get_ids:
        if AR_USER_STORY.objects.filter(id=id).exists():
            get_user_storyes = get_object_or_404(AR_USER_STORY, pk=id)
            get_score += get_user_storyes.readiness_quality_score
            if get_user_storyes.story_points != None:
                get_size += get_user_storyes.story_points.Point_score
    return JsonResponse({"get_score": get_score / get_count_of_storyes, "get_size": get_size})


@csrf_exempt
@login_required
def get_backlogs(request):
    org_id = request.session['org_id']
    org_ins = AR_organization.objects.get(id=org_id)
    select_backlog_default = AR_BACKLOG.objects.filter(title='None').filter(ORG_ID=org_ins)
    product_id = request.POST["product_id"]
    instance_product = get_object_or_404(AR_product, pk=product_id)
    if AR_BACKLOG.objects.filter(product_parent=instance_product).exists():
        get_backlog = AR_BACKLOG.objects.filter(product_parent=instance_product)
    else:
        get_backlog = {}
    return render(request, 'admin/iterations/get_backlog.html', {'date': datetime.now(), "backlog_data": get_backlog,"select_backlog_default":select_backlog_default})


@csrf_exempt
@login_required
def get_user_story(request):
    get_backlog_id = request.POST["get_backlog_id"]
    selected_user_storyes = request.POST["selected_user_storyes"].split("|")
    instance_of_backlog = get_object_or_404(AR_BACKLOG, pk=get_backlog_id)
    if AR_USER_STORY.objects.filter(backlog_parent=instance_of_backlog).exists():
        get_userstory = AR_USER_STORY.objects.filter(backlog_parent=instance_of_backlog)
    else:
        get_userstory = {}
    return render(request, 'admin/iterations/get_user_storyes.html',
                  {'date': datetime.now(), "user_story_data": get_userstory,
                   'selected_user_storyes': selected_user_storyes})


@login_required
def index(request):
    gat_url = request.get_full_path()
    get_status_of_permission = True
    if gat_url.find('manage-iteration') != -1:
        get_status_of_permission = product_view.check_permition(request, 'Manage Iterations', 0)
    else:
        get_status_of_permission = product_view.check_permition(request, 'Iteration View', 0)
    if get_status_of_permission:
        org_info_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        if ArIterations.objects.filter(ORG_ID=org_info_ins).exists():
            get_all_iterations = ArIterations.objects.filter(ORG_ID=org_info_ins).order_by("-id")
        else:
            get_all_iterations = {}
        if ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id']).exists():
            show_column = ArShowcolumns.objects.filter(Table_name='ArIterations').filter(
                user_id=request.session['user_id'])
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
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Rearrange_Request")
        Rearrange_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Not_Remove")
        Not_Remove_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Remove Request")
        Remove_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Remove_Success")
        Remove_done_msg = msg.notification_desc
        return render(request, 'admin/iterations/index.html',
                      {'date': datetime.now(), "Rearrange_Request_msg": Rearrange_Request_msg,
                       'Remove_done_msg': Remove_done_msg, 'Remove_Request_msg': Remove_Request_msg,
                       'Not_Remove_msg': Not_Remove_msg, 'all_column_list': all_column_list,
                       'get_show_column': get_show_column, 'get_all_iterations': get_all_iterations,
                       'user_name': request.session['user_name'], 'BASE_URL': settings.BASE_URL})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html',
                      {'BASE_URL': settings.BASE_URL, 'error_message': error_data})


@login_required
def update_table_structure(request, columnnames):
    if ArShowcolumns.objects.filter(Table_name='ArIterations').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='ArIterations').filter(
            user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='ArIterations', user_id=request.session['user_id'],
                                    columnName=columnnames, ORG_id=request.session['org_id'])
        save_column.save()
    msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Rearrange")
    msg_data = msg.notification_desc
    messages.info(request, msg_data)
    return redirect(settings.BASE_URL + 'iteration-view')



@login_required
def edit_iteration(request, id):
    if product_view.check_permition(request, 'Manage Iterations', 1):
        user_id = request.session['user_id']
        org_info = AR_organization.objects.filter(id=request.session['org_id'])
        IterationInfo = get_object_or_404(ArIterations, pk=id)
        if request.method == 'POST':
            IterationForm_get = IterationForm(org_info,user_id,  request.POST, instance=IterationInfo)
            if IterationForm_get.is_valid():
                IterationForm_get_commit = IterationForm_get.save(commit=False)
                # #######################################33
                UserStory = IterationForm_get.cleaned_data.get('UserStory')
                # return HttpResponse (UserStory)
                story_num = 0
                if UserStory.count() != 0:
                    for i in UserStory:
                        story_data = AR_USER_STORY.objects.filter(title=i)
                        story_num = story_num + story_data[0].readiness_quality_score

                    story_num_value = story_num / UserStory.count()
                    story_num_value = round(story_num_value, 2)

                else:
                    story_num_value = 0
                    story_num_value = round(story_num_value, 2)
                # #######################################33


                StartDate = request.POST.get('StartDate')
                StartDateSet = datetime.strptime(StartDate, "%m/%d/%Y")
                EndDate = request.POST.get('EndDate')
                EndDateSet = datetime.strptime(EndDate, "%m/%d/%Y")
                IterationForm_get_commit.StartDate = StartDateSet
                IterationForm_get_commit.EndDate = EndDateSet
                IterationForm_get_commit.IterationScore = story_num_value
                try:
                    IterationForm_get_commit.save()
                    IterationForm_get.save_m2m()
                    msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Update")
                    msg_data = msg.notification_desc
                    messages.info(request, msg_data)

                except:
                    messages.error(request, IterationForm_get.ValidationError)
            else:
                messages.error(request, IterationForm_get.errors)
            return redirect(settings.BASE_URL + "iteration-view")
        else:
            IterationForm_get = IterationForm(org_info,request.session['user_id'], instance=IterationInfo)
            start_data = IterationInfo.StartDate.strftime("%m/%d/%Y")
            end_data = IterationInfo.EndDate.strftime("%m/%d/%Y")
            return render(request, 'admin/iterations/edit_iteration.html',
                          {'IterationInfo': IterationInfo, 'date': datetime.now(), 'start_data': start_data,
                           'end_data': end_data, 'IterationForm': IterationForm_get,
                           'user_name': request.session['user_name'], 'BASE_URL': settings.BASE_URL})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html',
                      {'BASE_URL': settings.BASE_URL, 'error_message': error_data})


@login_required
def remove_iteration(request, id):
    if product_view.check_permition(request, 'Manage Iterations', 1):
        try:
            ArIterations.objects.get(pk=id).delete()
            msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Remove")
            msg_data = msg.notification_desc
            messages.info(request, msg_data)
        except(TypeError):
            msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Remove_error")
            msg_data = msg.notification_desc
            messages.error(request, msg_data)
    else:
        msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Permission")
        msg_data = msg.notification_desc
        messages.error(request, msg_data)
    return redirect(settings.BASE_URL + 'iteration-view')


@login_required
def add_iteration(request):
    if product_view.check_permition(request, 'Manage Iterations', 1):
        user_id = request.session['user_id']
        org_info = AR_organization.objects.filter(id=request.session['org_id'])
        if request.method == 'POST':
            IterationForm_get = IterationForm(org_info,user_id, request.POST)
            if IterationForm_get.is_valid():
                IterationName = IterationForm_get.cleaned_data.get('IterationName')
                UserStory = IterationForm_get.cleaned_data.get('UserStory')
                story_num = 0
                if UserStory.count() != 0:
                    for i in UserStory:
                        story_data = AR_USER_STORY.objects.filter(title=i)
                        story_num = story_num + story_data[0].readiness_quality_score

                    story_num_value = story_num / UserStory.count()
                    story_num_value = round(story_num_value, 2)

                else:
                    story_num_value = 0
                    story_num_value = round(story_num_value, 2)

                if ArIterations.objects.filter(IterationName=IterationName).filter(
                        ORG_ID=request.session['org_id']).exists():
                    print('hhhh')
                    msg = get_object_or_404(Notification, page_name="Manage Iteration", notification_key="Exists")
                    msg_data = msg.notification_desc
                    messages.error(request, IterationName + " , " + msg_data)
                else:
                    print('dddd')
                    IterationForm_data = IterationForm_get.save(commit=False)
                    ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                    StartDate = request.POST.get('StartDate')
                    # StartDateSet = datetime.strptime(StartDate, "%m/%d/%Y %I:%M %p")
                    StartDateSet = datetime.strptime(StartDate, "%m/%d/%Y")
                    EndDate = request.POST.get('EndDate')
                    EndDateSet = datetime.strptime(EndDate, "%m/%d/%Y")
                    org_info_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                    IterationForm_data.StartDate = StartDateSet
                    IterationForm_data.EndDate = EndDateSet
                    IterationForm_data.ORG_ID = org_info_ins
                    IterationForm_data.IterationScore = story_num_value

                    IterationForm_data.create_by = ar_user_insta
                    IterationForm_data.update_by = ar_user_insta

                    # IterationForm_data.save()
                    # print("lon")
                    # IterationForm_get.save_m2m()
                    # create_itera_id = "AR_ITER_" + str(IterationForm_data.id)
                    # ArIterations.objects.filter(id=IterationForm_data.id).update(IterationId=create_itera_id)
                    # msg = get_object_or_404(Notification, page_name="Manage Iteration",
                    #                         notification_key="Add")
                    # msg_data = msg.notification_desc
                    # messages.info(request, msg_data)
                    # return redirect(settings.BASE_URL + "iteration-view")
                    # IterationForm_data.save()
                    # print("kkkk")
                    # IterationForm_get.save_m2m()
                    try:

                        IterationForm_data.save()
                        IterationForm_get.save_m2m()
                        create_itera_id = "AR_ITER_" + str(IterationForm_data.id)
                        ArIterations.objects.filter(id=IterationForm_data.id).update(IterationId=create_itera_id)
                        msg = get_object_or_404(Notification, page_name="Manage Iteration",notification_key="Add")
                        msg_data = msg.notification_desc
                        messages.info(request, msg_data)
                        return redirect(settings.BASE_URL + "iteration-view")
                    except:
                        messages.error(request, IterationForm_get.errors)
            else:
                messages.error(request, IterationForm_get.errors)
        else:
            IterationForm_get = IterationForm(org_info,user_id)
        return render(request, 'admin/iterations/add_iteration.html',
                      {'date': datetime.now(), 'IterationForm': IterationForm_get,
                       'user_name': request.session['user_name'], 'BASE_URL': settings.BASE_URL})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html',
                      {'BASE_URL': settings.BASE_URL, 'error_message': error_data})




@csrf_exempt
@login_required
def get_team(request):
    org_id = request.session['org_id']
    org_ins = AR_organization.objects.get(id=org_id)
    select_team_default = AR_team.objects.filter(Team_name='None').filter(ORG_id=org_ins)
    # org_id = 4
    get_backlog_id = request.POST["get_backlog_id"]
    selected_team = request.POST["selected_selected_team"]
    # get_backlog_id = 70
    # selected_team = ""


    backlog_ins = get_object_or_404(AR_BACKLOG, pk=get_backlog_id)
    print("====depak===")
    print(backlog_ins.title)
    print(backlog_ins.team_list.all())
    return render(request, 'admin/iterations/get_team.html', {'get_team':backlog_ins.team_list.all(),"select_team_default":select_team_default,"selected_team":selected_team})

