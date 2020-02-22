from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from agileproject import settings
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from account.models import Ar_user,ArUserProfile,AR_organization,Notification
from django.contrib import messages
import hashlib
import django
from datetime import datetime
from django.db.models import Subquery
# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated:
        user = Ar_user.objects.filter(id=request.session['user_id'])
        profile = ArUserProfile.objects.filter(ORG_ID=request.session['org_id'])
        get_count_of_invit_user = Ar_user.objects.filter(created_by=request.session['user_id']).count()
        get_active_user = User.objects.filter(is_active=True)
        get_count_of_active_user = Ar_user.objects.filter(created_by=request.session['user_id']).filter(
            user_id__in=Subquery(get_active_user.values("id"))).count()
        if request.method == "POST":
            user_name = request.POST["user_name"]
            city = request.POST["city"]
            state = request.POST["state"]
            zip = request.POST["zip"]
            country = request.POST["country"]
            phone = request.POST["phone"]
            if zip == "":
                zip=0
            if Ar_user.objects.filter(id=request.session['user_id']).exists():
                Ar_user.objects.filter(id=request.session['user_id']).update(user_name=user_name, city=city,state=state,zip=zip,country=country,
                                                            phone=phone)
                msg = Notification.objects.filter(page_name="Account Settings").filter(notification_key="Done")
                msg_data = msg[0].notification_desc
                messages.info(request, msg_data)
                # messages.info(request, "Profile updated successfully !")
                del request.session['user_name']
                request.session['user_name'] = user_name
                return redirect(settings.BASE_URL + 'account-settings')
            else:
                msg = Notification.objects.filter(page_name="Account Settings").filter(notification_key="Not Done")
                msg_data = msg[0].notification_desc
                messages.error(request, msg_data)
                # messages.info(request, "Profile not updated !")
        return render(request,"admin/account_settings/index.html",{'date':datetime.now(),'get_count_of_active_user':get_count_of_active_user,'get_count_of_invit_user':get_count_of_invit_user,'profile':profile,'user':user,"BASE_URL":settings.BASE_URL,'user_name':request.session['user_name']})
    else:
        return redirect(settings.BASE_URL)


@login_required
def get_data(request):
    if request.method == "POST":
        check_map = request.POST['check']
        data = Ar_user.objects.filter(id=request.session['user_id'])

        username = data[0].user_id
        data = User.objects.filter(id=username)
        username = data[0].username
        user = auth.authenticate(username=username,password=check_map)
        if user is not None:
            check_map=0
        else:
            check_map=1
        return JsonResponse({'check_project': check_map})
    return JsonResponse({'check_project':"sorry"})


@login_required
def pass_change(request):
    if request.method == "POST":
        newpwd = request.POST['newpwd']
        # print(newpwd)
        data = Ar_user.objects.filter(id=request.session['user_id'])

        username = data[0].user_id
        data = User.objects.get(id=username)
        username = data.username
        # user = auth.authenticate(username=username,password=check_map)
        #
        #
        # data = User.objects.get(id=request.session['user_id'])
        # username = data.username
        # print(username)
        # print(newpwd)
        data.set_password(newpwd)
        data.save()
        del request.session['user_id']
        del request.session['org_id']
        del request.session['user_name']
        auth.logout(request)
        user = auth.authenticate(username=username, password=newpwd)
        if user is not None:
            get_user_info = Ar_user.objects.get(user=user)
            request.session['user_id'] = get_user_info.id
            request.session['org_id'] = get_user_info.org_id.id
            request.session['user_name'] = get_user_info.user_name
            auth.login(request, user)
        check_map=1
        return JsonResponse({'check_project': check_map})
    return JsonResponse({'check_project':"sorry"})

