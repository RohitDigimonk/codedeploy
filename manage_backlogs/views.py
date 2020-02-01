from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import Ar_Backlog_Form
from .models import AR_BACKLOG
from django.contrib import messages
from account.models import AR_organization,Ar_user,ArShowcolumns,Notification
from datetime import datetime
import csv
from manage_product.models import AR_product
from manage_product import views as product_view
from user_story_view import views as storyes_view
# Create your views here.

##################################View##############################
@login_required
def backlogview(request):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    backlog_data = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
    ar_backlog_form = Ar_Backlog_Form(org_info)
    return render(request, 'admin/backlog_view/index.html',{'ar_backlog_form':ar_backlog_form,'date':datetime.now(),'backlog_data':backlog_data,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

################################################################
@login_required
def index(request):
    gat_url = request.get_full_path()
    get_status_of_permission = True
    if gat_url.find('manage-backlog') != -1:
        get_status_of_permission = product_view.check_permition(request, 'Manage Backlogs', 0)
    else:
        get_status_of_permission = product_view.check_permition(request, 'Backlog View', 0)
    if get_status_of_permission:
        backlog_edit_status = product_view.check_permition(request, 'Manage Backlogs', 1)
        org_info = AR_organization.objects.filter(id=request.session['org_id'])
        user_id=request.session['user_id']
        ar_backlog_form = Ar_Backlog_Form(org_info,user_id)
        ar_backlog = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
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
            "product_parent": "Product Parent",
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
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Rearrange_Request")
        Rearrange_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Not_Remove")
        Not_Remove_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Remove Request")
        Remove_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Remove_Success")
        Remove_done_msg = msg.notification_desc
        return render(request, 'admin/manage_backlogs/index.html',{"Rearrange_Request_msg":Rearrange_Request_msg,'Remove_done_msg':Remove_done_msg,'Remove_Request_msg':Remove_Request_msg,'Not_Remove_msg':Not_Remove_msg,'backlog_edit_status':backlog_edit_status,'all_column_list':all_column_list,'get_show_column':get_show_column,'all_backlog_get':all_backlog_get,'date':datetime.now(),'ar_backlog':ar_backlog,'ar_backlog_form':ar_backlog_form,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})
    else:
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL})

@login_required
def add_backlog(request):
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    # user_name = request.session['user_name']
    user_id = request.session['user_id']
    if request.method == "POST":
        ar_backlog_form = Ar_Backlog_Form(org_info,user_id,request.POST)
        if ar_backlog_form.is_valid():
            title = ar_backlog_form.cleaned_data.get('title')
            product_parent = ar_backlog_form.cleaned_data.get('product_parent')
            org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
            if AR_BACKLOG.objects.filter(title=title).filter(ORG_ID=org_ins).exists():
                msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Exists")
                msg_data = msg.notification_desc
                messages.error(request,title +" , " + msg_data)
            else:
                # product = AR_product.objects.get(Product_name=product_parent)
                # if product.Children_backlog_list == "":
                #     child_back_list = title
                # else:
                #     child_back_list = product.Children_backlog_list + " | " + title
                # AR_product.objects.filter(Product_name=product_parent).update(Children_backlog_list=child_back_list)
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
                    ar_backlog_form.save_m2m()
                    msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Add")
                    msg_data = msg.notification_desc
                    messages.info(request, msg_data)
                    return redirect(settings.BASE_URL + 'manage-backlog')
                except:
                    messages.error(request, ar_backlog_form.errors)
        else:
            messages.error(request, ar_backlog_form.errors)
    return redirect(settings.BASE_URL + 'manage-backlog')

@login_required
def edit_backlog(request,id):
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
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
        "product_parent": "Product Parent",
        "BL_STATUS": "Backlog Status",
        "ORG_ID": "ORG Name",
        "created_by": "Created By",
        "created_dt": "Created Date",
        "updated_by": "Updated By",
        "updated_dt": "Updated Date",
    }
    ar_backlog = AR_BACKLOG.objects.filter(ORG_ID=request.session['org_id'])
    backlog_form = AR_BACKLOG.objects.get(id=id)
    backlog_id=backlog_form.id
    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    user_id = request.session['user_id']
    if request.method == "POST":
        backlog_form = Ar_Backlog_Form( data=(request.POST or None),user_id=user_id,org_info=org_info,instance = backlog_form)
        if backlog_form.is_valid():
            title = backlog_form.cleaned_data.get('title')
            product_parent = backlog_form.cleaned_data.get('product_parent')
            data = backlog_form.save(commit=False)
            created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
            data.updated_by = created_by_ins
            data.updated_dt = datetime.now()
            try:
                get_old_instance = get_object_or_404(AR_BACKLOG, pk=id)
                # product = AR_product.objects.get(Product_name=product_parent)
                # if product.Children_backlog_list == "":
                #     child_back_list = title
                # else:
                #     child_back_list = product.Children_backlog_list + " | " + title
                # AR_product.objects.filter(Product_name=product_parent).update(Children_backlog_list=child_back_list)
                data.save()
                backlog_form.save_m2m()
                storyes_view.BacklogGoodnessScore(request,0, request.POST["product_parent"])  # SET numbers for new instance
                storyes_view.BacklogGoodnessScore(request,0, get_old_instance.product_parent.id)  # SET numbers for old instance
                msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Update")
                msg_data = msg.notification_desc
                messages.info(request, msg_data)
                return redirect(settings.BASE_URL + 'manage-backlog')
            except:
                messages.error(request,  backlog_form.errors)
        else:
            messages.error(request,  backlog_form.errors)
    else:
        backlog_form = Ar_Backlog_Form(instance=backlog_form,org_info=org_info,user_id=user_id)
    return render(request, 'admin/manage_backlogs/edit.html',{'all_column_list':all_column_list,'get_show_column':get_show_column,'all_backlog_get':all_backlog_get,'date':datetime.now(),'backlog_edit':"value",'ar_backlog':ar_backlog,'backlog_id':backlog_id,'ar_backlog_edit_form':backlog_form,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

@login_required
def delete_backlog(request,id):
    if product_view.check_permition(request, 'Backlog View', 1):
        try:

            get_instance = get_object_or_404(AR_BACKLOG,pk=id)
            product_id = get_instance.product_parent.id
            get_instance.delete()
            storyes_view.BacklogGoodnessScore(request, 0, product_id)
            msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Remove")
            msg_data = msg.notification_desc
            messages.info(request, msg_data)
        except(TypeError):
            msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Remove_error")
            msg_data = msg.notification_desc
            messages.error(request, msg_data)
    else:
        msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Permission")
        msg_data = msg.notification_desc
        messages.error(request, msg_data)
    return redirect(settings.BASE_URL + 'manage-backlog')

@login_required
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


@login_required
def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_BACKLOG').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_BACKLOG',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    msg = get_object_or_404(Notification, page_name="Manage Backlog", notification_key="Rearrange")
    msg_data = msg.notification_desc
    messages.info(request, msg_data)
    return redirect(settings.BASE_URL + 'backlog-view')