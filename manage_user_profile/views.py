from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from account.models import AR_organization,Ar_user,ArUserProfile,ArUserProfilePermission
from .forms import ArUserProfileForm
from agileproject.serializers import ArUserProfilePermissionSerializer

# Create your views here.
def index(request):
    org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
    ar_user_profile_form = ArUserProfileForm()
    ar_user_data = ArUserProfile.objects.filter(ORG_ID=org_ins)
    if request.method == "POST":
        list = request.POST.get("list")
        if list is not None:
            list_ins = get_object_or_404(ArUserProfile, profile_key=list)
            created_by_ins = get_object_or_404(User, pk=request.session['user_id'])
            org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
            activity = request.POST.getlist('activity[]')
            if ArUserProfilePermission.objects.filter(profile_key=list_ins).exists():
                messages.info(request, "Profile permission update successfully !")
            else:
                messages.info(request, "Profile permission added successfully !")
            for activityvalue in activity:
                value = activityvalue.lower()
                valueacti = value.replace(" ", "")
                editor = request.POST.get(valueacti+"edit")
                if editor == "on" :
                    editoracti= True
                else:
                    editoracti=False
                viewer = request.POST.get(valueacti + "view")
                if viewer == "on":
                    vieweracti = True
                else:
                    vieweracti = False
                if ArUserProfilePermission.objects.filter(profile_key=list_ins).filter(activites=activityvalue).exists():
                    ArUserProfilePermission.objects.filter(profile_key=list_ins).filter(activites=activityvalue).update(update_by=created_by_ins,
                                                           activites=activityvalue, editor=editoracti,
                                                           viewer=vieweracti)
                else:
                    activitydata = ArUserProfilePermission(profile_key=list_ins, ORG_ID=org_ins, create_by=created_by_ins, update_by=created_by_ins,
                                                        activites=activityvalue,editor=editoracti,viewer=vieweracti)
                    activitydata.save()
                    return redirect(settings.BASE_URL + 'user-profile')
        else:
            messages.info(request, "Please select a Profile Key !")
    return render(request, 'admin/manage_user_profile/index.html',{'ar_user_data':ar_user_data,'ar_user_profile_form':ar_user_profile_form,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})


def add_profile(request):
    org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
    ar_user_profile_form = ArUserProfileForm()
    ar_user_data = ArUserProfile.objects.filter(ORG_ID=org_ins)
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    if request.method == "POST":
        ar_user_profile_form = ArUserProfileForm(request.POST)
        if ar_user_profile_form.is_valid():
            # profile_key  = ar_user_profile_form.cleaned_data.get('profile_key')
            # if ArUserProfile.objects.filter(profile_key=profile_key).filter(ORG_ID=request.session['org_id']).exists():
            #     messages.error(request, "Profile already exists.")
            # else:
            data = Ar_user.objects.filter(id=request.session['user_id'])
            username = data[0].user_id
            # data = User.objects.filter(id=username)

            created_by_ins = get_object_or_404(User, pk=username)
            org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
            data = ar_user_profile_form.save(commit=False)
            data.create_by=created_by_ins
            data.update_by = created_by_ins
            data.ORG_ID=org_ins
            try:
                data.save()
                messages.info(request, "Profile key added successfully !")
                return redirect(settings.BASE_URL + 'user-profile')

            except:
                messages.error(request, ar_user_profile_form.errors)
        else:
            messages.error(request, ar_user_profile_form.errors)
    return render(request, 'admin/manage_user_profile/profile.html',{'ar_user_data':ar_user_data,'ar_user_profile_form':ar_user_profile_form,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})



def edit_user_profile(request,id):
    org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
    ar_user_data = ArUserProfile.objects.filter(ORG_ID=org_ins)
    ar_user_profile = ArUserProfile.objects.filter(ORG_ID=request.session['org_id'])
    ar_user_profile_form = ArUserProfile.objects.get(id=id)
    user_profile_id=ar_user_profile_form.id
    if request.method == "POST":
        ar_user_profile_form = ArUserProfileForm( data=(request.POST or None),instance = ar_user_profile_form)
        if ar_user_profile_form.is_valid():
            try:
                ar_user_profile_form.save()
                messages.info(request, "Profile key updated successfully !")
                return redirect(settings.BASE_URL + 'user-profile')
            except:
                messages.error(request, ar_user_profile_form.errors)
        else:
            messages.error(request, ar_user_profile_form.errors)
    else:
        ar_user_profile_form = ArUserProfileForm(instance=ar_user_profile_form)
    return render(request, 'admin/manage_user_profile/profile.html',{'ar_user_data':ar_user_data,'ar_user_profile_form':ar_user_profile_form,'ar_user_profile':ar_user_profile,'date':datetime.now(),'user_profile_id':user_profile_id,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})


def delete_user_profile(request,id):
    try:
        ArUserProfile.objects.get(pk=id).delete()
        messages.info(request, "Profile key removed !")
        return redirect(settings.BASE_URL + 'user-profile')
    except(TypeError):
        messages.error(request, "Maybe this Profile key is used in another table so we can not remove that !")


    return redirect(settings.BASE_URL + 'user-profile/add-profile')


def get_data(request):
    if request.method == "POST":
        check_map = request.POST['check']
        print('check_map[0]')
        print(check_map)
        data = ArUserProfile.objects.get(profile_key=check_map)
        val = data.id
        data = ArUserProfilePermission.objects.filter(profile_key=val)
        print(data)
        profiledata = ArUserProfilePermissionSerializer(data, many=True)
        return JsonResponse({'check_project': profiledata.data})
    return JsonResponse({'check_project':"sorry"})
