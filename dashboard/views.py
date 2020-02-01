from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User,auth
from agileproject import settings
from account.models import AR_organization
from manage_product.models import AR_product,AR_team
from manage_backlogs.models import AR_BACKLOG
from user_story_view.models import AR_USER_STORY
from manage_iterations.models import ArIterations
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.




@login_required
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'org_id' in request.session:
        del request.session['org_id']
    if 'user_name' in request.session:
        del request.session['user_name']
    auth.logout(request)
    return redirect(settings.BASE_URL)


@login_required
def index(request):
    org_ins = get_object_or_404(AR_organization, pk=request.session['org_id'])
    team = AR_team.objects.filter(ORG_id=org_ins).count()
    team_data = AR_team.objects.filter(ORG_id=org_ins)
    product = AR_product.objects.filter(ORG_ID=org_ins).count()
    product_data = AR_product.objects.filter(ORG_ID=org_ins)
    backlog = AR_BACKLOG.objects.filter(ORG_ID=org_ins).count()
    backlog_data = AR_BACKLOG.objects.filter(ORG_ID=org_ins)
    user_storyes = AR_USER_STORY.objects.filter(ORG_id=org_ins).count()
    user_storyes_data = AR_USER_STORY.objects.filter(ORG_id=org_ins)
    itearations = ArIterations.objects.filter(ORG_ID=org_ins).count()
    itearations_data = ArIterations.objects.filter(ORG_ID=org_ins)
    return render(request,"admin/dashboard/index.html",{'itearations_data':itearations_data,'user_storyes_data':user_storyes_data,'backlog_data':backlog_data,
                                                        'product_data':product_data,'team_data':team_data,'date':datetime.now(),'itearations':itearations,
                                                        'user_storyes':user_storyes,'team':team,'product':product,'backlog':backlog,'user_name':request.session['user_name'],
                                                        "BASE_URL":settings.BASE_URL})

