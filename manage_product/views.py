from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from agileproject import settings
from .forms import ProductForm
from django.contrib import messages
from manage_backlogs.models import AR_BACKLOG
from account.models import Ar_user,AR_organization,ArShowcolumns,ArUserProfilePermission,Notification
from django.contrib.auth.decorators import login_required
from .models import AR_product
from datetime import datetime
from django.template.defaulttags import register
from django.db.models import Q
# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def check_permition(request,page_name_get,page_action_get):
    '''
    This function is use for check the user permission
    and it's tke some peramiters 4 peramiters
    1 'request' this is a statis and required
    2 'page_name' for which page you check that (String)
    3 'peramiters' type it's use the 0 OR 1 value 0 for view page and 1 for edit page (int)
     and this function is return true or false value for if user have the peramiters for that task then it's give true other it's give false
    '''
    status_set = True
    page_name = page_name_get   #'Product View'
    page_action = page_action_get    # 0 USE FOR VIEW ACTION AND 1 FOR EDIT SECTION
    # page_name_action = '1'
    if request.session['user_type'] == 'User':
        status_set = False
        get_user_info = get_object_or_404(Ar_user, pk=request.session['user_id'])
        set_profile_daat = get_user_info.profile_permission.all()
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        for items in set_profile_daat:
            print(items)
            if ArUserProfilePermission.objects.filter(activites=page_name,profile_key=items,ORG_ID=org_ins).exists():
                get_permition_data = ArUserProfilePermission.objects.get(activites=page_name,profile_key=items,ORG_ID=org_ins)
                if get_permition_data.editor:
                    status_set = True
                else:
                    status_set = False
                    if page_action == 0:
                        if get_permition_data.viewer:
                            status_set = True
                        else:
                            status_set = False
            else:
                status_set = False
            if status_set:
                break
    return status_set

@login_required
def productview(request):
    product_data = AR_product.objects.filter(ORG_ID=request.session['org_id'])
    return render(request, 'admin/product_view/index.html',{'date':datetime.now(),'product_data':product_data,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

@login_required
def index(request,set_statue="",set_statue_2="",csv_id=""):
    gat_url = request.get_full_path()
    get_status_of_permission = True
    if gat_url.find('manage-products') != -1:
        get_status_of_permission = check_permition(request, 'Manage Products', 0)
    else:
        get_status_of_permission = check_permition(request, 'Product View', 0)
    if get_status_of_permission:
        org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
        if AR_product.objects.filter(ORG_ID=org_ins).exists():
            all_project_get = AR_product.objects.filter(ORG_ID=org_ins).order_by("-id").filter(~Q(Product_name = 'None'))
        else:
            all_project_get = {}
        if ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id']).exists():
            show_column = ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id'])
            get_show_column = show_column[0].columnName.split(",")
        else:
            get_show_column = {}
        all_column_list = {
            "Team_parent": "Team Parent",
            "Children_backlog_list": "Children Backlog List",
            "Product_name":"Product Name",
            "Product_description":"Product Description",
            "Business_unit":"Business Unit",
            "Product_size":"Product Size",
            "Product_score":"Product Score",
            "US_quality_threshold":"Us Quality Threshold",
            "ORG_ID":"ORG Name",
            "create_by":"Created By",
            "create_dt":"Created Date",
            "update_by":"Updated By",
            "update_dt":"Updated Date",
                }
        msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Rearrange_Request")
        Rearrange_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Not_Remove")
        Not_Remove_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Remove Request")
        Remove_Request_msg = msg.notification_desc
        msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Remove_Success")
        Remove_done_msg = msg.notification_desc
        ar_backlog = AR_BACKLOG.objects.all()
        return render(request, 'admin/manage_product/index.html', {'ar_backlog':ar_backlog,'Rearrange_Request_msg':Rearrange_Request_msg,'Remove_done_msg':Remove_done_msg,'Remove_Request_msg':Remove_Request_msg,'Not_Remove_msg':Not_Remove_msg,'all_project_get':all_project_get,'all_column_list':all_column_list,"get_show_column":get_show_column,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL':settings.BASE_URL,"all_project_get":all_project_get})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL,'error_message':error_data})
@login_required
def add_product(request):
    if check_permition(request, 'Manage Products', 1):
        if request.method == 'POST':
            product_form = ProductForm(request.user,request.session['org_id'], request.POST)
            status = product_form.is_valid()
            if product_form.is_valid():
                Product_name = product_form.cleaned_data.get('Product_name')
                org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                if AR_product.objects.filter(Product_name=Product_name).filter(ORG_ID=org_ins).exists():
                    msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Exists")
                    msg_data = msg.notification_desc
                    messages.error(request, msg_data)
                else:
                    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                    ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                    product = product_form.save(commit=False)
                    product.ORG_ID = org_ins
                    product.create_by = ar_user_insta
                    product.update_by = ar_user_insta
                    product.save()
                    product_form.save_m2m()
                    msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Add")
                    msg_data = msg.notification_desc
                    messages.info(request, msg_data)
                    return redirect(settings.BASE_URL + "manage-products")
            else:
                messages.error(request, product_form.errors)
            return redirect(settings.BASE_URL + "manage-products/add-product")
        else:
            product_form = ProductForm(request.user,request.session['org_id'])
        return render(request, 'admin/manage_product/add_project.html', {'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL,'product_form':product_form})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL,'error_message':error_data})
@login_required
def remove_product(request,id):
    if check_permition(request, 'Manage Products', 1):
        try:
            project = get_object_or_404(AR_product, pk=id)
            project.delete()
            msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Remove")
            msg_data = msg.notification_desc
            messages.info(request, msg_data)
        except(TypeError, OverflowError):
            msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Remove_error")
            msg_data = msg.notification_desc
            messages.error(request, msg_data)
    else:
        msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Permission")
        msg_data = msg.notification_desc
        messages.error(request, msg_data)
    return redirect(settings.BASE_URL+'manage-products')

@login_required
def edit_product(request,id):
    if check_permition(request, 'Manage Products', 1):
        product_info = get_object_or_404(AR_product, pk=id)
        if request.method == 'POST':
            product_form = ProductForm(request.user, request.session['org_id'], request.POST,instance = product_info)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                product.update_by = ar_user_insta
                product.save()
                product_form.save_m2m()
                msg = get_object_or_404(Notification, page_name="Manage Products", notification_key="Update")
                msg_data = msg.notification_desc
                messages.info(request, msg_data)
                return redirect(settings.BASE_URL + "manage-products")
            else:
                messages.error(request, product_form.error)
            return redirect(settings.BASE_URL + "manage-products")
        else:
            product_form = ProductForm(request.user, request.session['org_id'],instance=product_info)
        return render(request, 'admin/manage_product/edit_project.html',{'team_id': id,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL, 'product_form': product_form})
    else:
        msg = get_object_or_404(Notification, page_name="Authorized", notification_key="Error")
        error_data = msg.notification_desc
        return render(request, 'admin/dashboard/no_permssion.html', {'BASE_URL': settings.BASE_URL,'error_message':error_data})


def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_PRODUCT',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    msg = get_object_or_404(Notification, page_name="View Products", notification_key="Rearrange")
    msg_data = msg.notification_desc
    messages.info(request, msg_data)
    return redirect(settings.BASE_URL + 'products-view')