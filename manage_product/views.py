from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from agileproject import settings
from .forms import ProductForm
from django.contrib import messages
from account.models import Ar_user,AR_organization,ArShowcolumns
from django.contrib.auth.decorators import login_required
from .models import AR_product
from datetime import datetime
# Create your views here.

@login_required
def productview(request):
    product_data = AR_product.objects.filter(ORG_ID=request.session['org_id'])
    return render(request, 'admin/product_view/index.html',{'date':datetime.now(),'product_data':product_data,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

@login_required
def index(request,set_statue="",set_statue_2="",csv_id=""):
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    all_project_get = {}
##############################################
    if AR_product.objects.filter(ORG_ID=org_ins).exists():
        all_project_get = AR_product.objects.filter(ORG_ID=org_ins).order_by("-id")
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
        "Procduct_name":"Procduct Name",
        "Procduct_description":"Procduct Description",
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
##########################################################


    return render(request, 'admin/manage_product/index.html', {'all_project_get':all_project_get,'all_column_list':all_column_list,"get_show_column":get_show_column,'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL':settings.BASE_URL,"all_project_get":all_project_get})

@login_required
def add_product(request):
    # product_form = ProductForm(request.POST or None,request.session['org_id'])
    if request.method == 'POST':
        product_form = ProductForm(request.user,request.session['org_id'], request.POST)
        status = product_form.is_valid()
        if product_form.is_valid():
            Procduct_name = product_form.cleaned_data.get('Procduct_name')
            if AR_product.objects.filter(Procduct_name=Procduct_name).filter(ORG_ID=request.session['org_id']).exists():
                messages.error(request, "Product already exists.")
            else:
                org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
                ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
                product = product_form.save(commit=False)
                product.ORG_ID = org_ins
                product.create_by = ar_user_insta
                product.update_by = ar_user_insta
                product.save()
                product_form.save_m2m()
                messages.info(request, "Product added successfully !")
                return redirect(settings.BASE_URL + "manage-products")
        else:
            messages.info(request, product_form.errors)
        return redirect(settings.BASE_URL + "manage-products/add-product")
    else:
        product_form = ProductForm(request.user,request.session['org_id'])
    return render(request, 'admin/manage_product/add_project.html', {'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL,'product_form':product_form})

@login_required
def remove_product(request,id):
    try:
        project = get_object_or_404(AR_product, pk=id)
        project.delete()
        messages.info(request, "Product removed successfully !")
    except(TypeError, OverflowError): 
        messages.error(request, "Maybe this project is used in another table so we can not remove that !")
    return redirect(settings.BASE_URL+'manage-products')

@login_required
def edit_product(request,id):
    product_info = get_object_or_404(AR_product, pk=id)
    if request.method == 'POST':
        product_form = ProductForm(request.user, request.session['org_id'], request.POST,instance = product_info)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            ar_user_insta = get_object_or_404(Ar_user, pk=request.session['user_id'])
            product.update_by = ar_user_insta
            product.save()
            product_form.save_m2m()
            messages.info(request, "Product updated successfully !")
            return redirect(settings.BASE_URL + "manage-products")
        else:
            messages.error(request, product_form.error)
        return redirect(settings.BASE_URL + "manage-products")
    else:
        product_form = ProductForm(request.user, request.session['org_id'],instance=product_info)
    return render(request, 'admin/manage_product/edit_project.html',{'date':datetime.now(),'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL, 'product_form': product_form})


#####################################
def update_table_structure(request,columnnames):
    if  ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id']).exists():
        save_column = ArShowcolumns.objects.filter(Table_name='AR_PRODUCT').filter(user_id=request.session['user_id']).update(columnName=columnnames)
    else:
        save_column = ArShowcolumns(Table_name='AR_PRODUCT',user_id=request.session['user_id'],columnName=columnnames,ORG_id=request.session['org_id'])
        save_column.save()
    messages.info(request, "Table structure updated successfully.")
    return redirect(settings.BASE_URL + 'products-view')