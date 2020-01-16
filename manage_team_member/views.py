from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from account.models import Ar_user,AR_organization,ArUserProfile
from .forms import ManageTeamMemberForm
from manage_product.models import AR_team
from datetime import datetime

# Create your views here.
def index(request):
    # story_point = ArUserStoryPoints.objects.get(ORG_ID=request.session['org_id'])
    user1 = Ar_user.objects.filter(org_id=request.session['org_id'])
    user = AR_team.objects.filter(ORG_id=request.session['org_id'])
    print(user)
    # for user2 in user1:
    #     for a in user2.Team_member_list.all():
    #         print(a)
    #     print(user2.Team_member_list.all())
    # print(user1)



    # user = Ar_user.objects.filter(org_id=request.session['org_id'])

    return render(request, 'admin/manage_teams_members/index.html',{'date':datetime.now(),'user':user1,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})



def edit_team_member(request,id):
    user = Ar_user.objects.get(id=id)
    profile = ArUserProfile.objects.filter(ORG_ID=request.session['org_id'])
    member_form = Ar_user.objects.get(id=id)
    member_id=member_form.id
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    if request.method == "POST":
        user_name = request.POST["user_name"]
        city = request.POST["city"]
        state = request.POST["state"]
        zip = request.POST["zip"]
        country = request.POST["country"]
        phone = request.POST["phone"]
        status=request.POST["status"]
        if zip == "":
            zip = 0
        if Ar_user.objects.filter(id=id).exists():
            Ar_user.objects.filter(id=id).update(user_name=user_name, city=city,state=state,zip=zip,country=country, phone=phone,status=status)
            messages.info(request, "Profile updated successfully !")
        member_form = ManageTeamMemberForm(data=(request.POST or None), org_info=org_info, instance=member_form)
        if member_form.is_valid():
            try:
                team = member_form.save(commit=False)
                ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                team.update_by = ar_user_insta
                team.update_dt = datetime.now()
                member_form.save_m2m()
                return redirect(settings.BASE_URL + 'manage-team-member')
            except:
                messages.error(request,  member_form.errors)
        else:
            messages.error(request,  member_form.errors)
    else:
        member_form = ManageTeamMemberForm(instance=member_form,org_info=org_info)
    #######################################
    return render(request, 'admin/manage_teams_members/edit.html',{'profile':profile,'user':user,'date':datetime.now(),'member_edit':"value",'member_id':member_id,'member_edit_form':member_form,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})



def delete_team_member(request,id):
    try:
        Ar_user.objects.get(pk=id).delete()
        messages.info(request, "Team member removed !")
    except(TypeError):
        messages.error(request, "Maybe this member is used in another table so we can not remove that !")
    return redirect(settings.BASE_URL + 'manage-team-member')