from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ArManageGoalsForm
from .models import ArManageGoals
from account.models import AR_organization,Ar_user,Notification
from django.contrib import messages
from django.db.models import Q
from manage_product import views as product_view

from django.http import HttpResponse,JsonResponse
from user_story_view.models import AR_USER_STORY
from agileproject.serializers import ArUserStoryViewSerializer
# Create your views here.

@login_required
def index(request):
    if product_view.check_permition(request, 'Manage Goals', 0):
        goal_edit_status = product_view.check_permition(request, 'Manage Goals', 1)
        ArManageGoalsForm_get = ArManageGoalsForm()
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        get_all_goal = ArManageGoals.objects.filter(ORG_ID=org_ins)
        if request.method == 'POST':
            ArManageGoalsForm_get = ArManageGoalsForm(request.POST)
            if ArManageGoalsForm_get.is_valid():
                Goal_title = ArManageGoalsForm_get.cleaned_data.get('Goal_title')
                if ArManageGoals.objects.filter(Goal_title=Goal_title).filter(ORG_ID=org_ins).exists():
                    msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Exists")
                    msg_data = msg[0].notification_desc
                    messages.error(request, Goal_title + msg_data)
                    # messages.error(request, " '"+Goal_title+"' Goal already exists.")
                else:
                    try:
                        ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                        ManageGoals = ArManageGoalsForm_get.save(commit=False)
                        ManageGoals.ORG_ID = org_ins
                        ManageGoals.created_by = ar_user_insta
                        ManageGoals.updated_by = ar_user_insta
                        ManageGoals.save()
                        create_goal_id = "AR_GOAL_"+str(ManageGoals.id)
                        ArManageGoals.objects.filter(id=ManageGoals.id).update(Goal_id=create_goal_id)
                        msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Add")
                        msg_data = msg[0].notification_desc
                        messages.info(request, msg_data)
                        # messages.info(request, "Goal added successfully !")
                    except(TypeError, OverflowError):
                        messages.error(request, "Something was wrong !")
            else:
                messages.info(request, ArManageGoalsForm_get.errors)
            return redirect(settings.BASE_URL + "manage-goals")
        return render(request, 'admin/manage_goals/index.html',{'goal_edit_status':goal_edit_status,'get_all_goal':get_all_goal,'ArManageGoalsForm_get':ArManageGoalsForm_get,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})

@login_required
def edit(request,id):
    ArManageGoals_info = get_object_or_404(ArManageGoals, pk=id)
    ArManageGoalsForm_get = ArManageGoalsForm(instance=ArManageGoals_info)
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    if request.method == 'POST':
        ArManageGoalsForm_get = ArManageGoalsForm(request.POST,instance=ArManageGoals_info)
        if ArManageGoalsForm_get.is_valid():
            Goal_title = ArManageGoalsForm_get.cleaned_data.get('Goal_title')
            if ArManageGoals.objects.filter(Goal_title=Goal_title).filter(ORG_ID=org_ins).filter(~Q(id=id)).exists():
                msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Exists")
                msg_data = msg[0].notification_desc
                messages.error(request, Goal_title + msg_data)
                # messages.error(request, " '" + Goal_title + "' Goal already exists.")
            else:
                try:
                    ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                    ManageGoals = ArManageGoalsForm_get.save(commit=False)
                    ManageGoals.updated_by = ar_user_insta
                    ManageGoals.save()
                    msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Add")
                    msg_data = msg[0].notification_desc
                    messages.info(request, msg_data)
                    # messages.info(request, "Goal added successfully !")
                except(TypeError, OverflowError):
                    messages.error(request, "Something was wrong !")
        else:
            messages.info(request, ArManageGoalsForm_get.errors)
        return redirect(settings.BASE_URL + "manage-goals")
    return render(request,'admin/manage_goals/edit.html',{'ArManageGoalsForm_get':ArManageGoalsForm_get,'id':id})

@login_required
def remove_goal(request,id):
    if product_view.check_permition(request, 'Manage Goals', 1):
        try:
            ManageGoals = get_object_or_404(ArManageGoals, pk=id)
            ManageGoals.delete()
            msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Remove")
            msg_data = msg[0].notification_desc
            messages.info(request, msg_data)
            # messages.info(request, "Goal removed successfully !")
        except(TypeError):
            msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Remove_error")
            msg_data = msg[0].notification_desc
            messages.error(request, msg_data)
            # messages.error(request, "Maybe this goal is used in another table so we can not remove that !")
        return redirect(settings.BASE_URL + 'manage-goals')
    else:
        msg = Notification.objects.filter(page_name="Manage Goal").filter(notification_key="Permission")
        msg_data = msg[0].notification_desc
        messages.error(request, msg_data)
        # messages.warning(request, "You are not authorized person. !")
        return redirect(settings.BASE_URL + 'manage-goals')



def get_data(request):
    if request.method == "POST":
        check_map = request.POST['check']
        print(check_map)
        if check_map == "" :
            gole_val=0
        else:
            result = AR_USER_STORY.objects.filter(story_tri_part_text__icontains=check_map)
            gole_data = ArUserStoryViewSerializer(result, many=True)
            gole_val=gole_data.data
        return JsonResponse({'check_project': gole_val})