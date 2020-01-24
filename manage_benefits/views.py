from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.conf import settings
from .forms import ArManageBenefitsForm
from .models import ArManageBenefits
from account.models import AR_organization,Ar_user,Notification
from django.contrib import messages
from django.db.models import Q
from manage_product import views as product_view


from django.http import HttpResponse,JsonResponse
from user_story_view.models import AR_USER_STORY
from agileproject.serializers import ArUserStoryViewSerializer
# Create your views here.

def index(request):
    if product_view.check_permition(request, 'Manage Benefits', 0):
        benefits_edit_status = product_view.check_permition(request, 'Manage Benefits', 1)
        ArManageBenefitsForm_get = ArManageBenefitsForm()
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        get_all_Benefits = ArManageBenefits.objects.filter(ORG_ID=org_ins)
        if request.method == 'POST':
            ArManageBenefitsForm_get = ArManageBenefitsForm(request.POST)
            if ArManageBenefitsForm_get.is_valid():
                Benefit_title = ArManageBenefitsForm_get.cleaned_data.get('Benefits_title')
                if ArManageBenefits.objects.filter(Benefits_title=Benefit_title).filter(ORG_ID=org_ins).exists():
                    msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Exists")
                    msg_data = msg[0].notification_desc
                    messages.error(request, Benefit_title + msg_data)
                    # messages.error(request, " '"+Benefit_title+"' Benefits already exists.")
                else:
                    try:
                        ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                        ManageBenefits = ArManageBenefitsForm_get.save(commit=False)
                        ManageBenefits.ORG_ID = org_ins
                        ManageBenefits.created_by = ar_user_insta
                        ManageBenefits.updated_by = ar_user_insta
                        ManageBenefits.save()
                        create_benefite_id = "AR_BENEFITE_"+str(ManageBenefits.id)
                        ArManageBenefits.objects.filter(id=ManageBenefits.id).update(Benefits_id=create_benefite_id)
                        msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Add")
                        msg_data = msg[0].notification_desc
                        messages.info(request, msg_data)
                        # messages.info(request, "Benefits added successfully !")
                    except(TypeError, OverflowError):
                        messages.error(request, "Something was wrong !")
            else:
                messages.info(request, ArManageBenefitsForm_get.errors)
            return redirect(settings.BASE_URL + "manage-benefits")
        return render(request, 'admin/manage_benefits/index.html',{'benefits_edit_status':benefits_edit_status,'get_all_Benefits':get_all_Benefits,'ArManageBenefitsForm_get':ArManageBenefitsForm_get,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})
def edit(request,id):
    ArManageBenefits_info = get_object_or_404(ArManageBenefits, pk=id)
    ArManageBenefitsForm_get = ArManageBenefitsForm(instance=ArManageBenefits_info)
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    if request.method == 'POST':
        ArManageBenefitsForm_get = ArManageBenefitsForm(request.POST,instance=ArManageBenefits_info)
        if ArManageBenefitsForm_get.is_valid():
            Benefits_title = ArManageBenefitsForm_get.cleaned_data.get('Benefits_title')
            if ArManageBenefits.objects.filter(Benefits_title=Benefits_title).filter(ORG_ID=org_ins).filter(~Q(id=id)).exists():
                messages.error(request, " '" + Benefits_title + "' Benefit already exists.")
            else:
                try:
                    ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                    ManageBenefits = ArManageBenefitsForm_get.save(commit=False)
                    ManageBenefits.updated_by = ar_user_insta
                    ManageBenefits.save()
                    msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Update")
                    msg_data = msg[0].notification_desc
                    messages.info(request, msg_data)
                    # messages.info(request, "Benefits updated successfully !")
                except(TypeError, OverflowError):
                    messages.error(request, "Something was wrong !")
        else:
            messages.info(request, ArManageBenefitsForm_get.errors)
        return redirect(settings.BASE_URL + "manage-benefits")
    return render(request,'admin/manage_benefits/edit.html',{'ArManageBenefitsForm_get':ArManageBenefitsForm_get,'id':id,'BASE_URL': settings.BASE_URL})


def remove_benefit(request,id):
    if product_view.check_permition(request, 'Manage Benefits', 1):
        try:
            ManageBenefits = get_object_or_404(ArManageBenefits, pk=id)
            ManageBenefits.delete()
            msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Remove")
            msg_data = msg[0].notification_desc
            messages.info(request, msg_data)
            # messages.info(request, "Benefits removed successfully !")
        except(TypeError, OverflowError):
            msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Remove_error")
            msg_data = msg[0].notification_desc
            messages.error(request, msg_data)
            # messages.error(request, "Maybe this benefits is used in another table so we can not remove that !")
    else:
        msg = Notification.objects.filter(page_name="Manage Benefit").filter(notification_key="Permission")
        msg_data = msg[0].notification_desc
        messages.error(request, msg_data)
        # messages.error(request, "You are not authorized person !")
    return redirect(settings.BASE_URL + 'manage-benefits')



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