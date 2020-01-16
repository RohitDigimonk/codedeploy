from django.shortcuts import render
from django.conf import settings
from .models import ArUserStoryPoints
from .forms import ArStoryPointForm
from account.models import AR_organization,Ar_user,ArShowcolumns
from manage_product.models import AR_product
from manage_epic_capability.models import AR_EPIC_CAPABILITY

# Create your views here.
def index(request):
    story_point = ArUserStoryPoints.objects.all()

    org_info = AR_organization.objects.filter(id=request.session['org_id'])
    ar_story_point_form = ArStoryPointForm()

    # story_point = {}
    return render(request, 'admin/user_story_points/index.html',{'ar_story_point_form':ar_story_point_form,'story_point':story_point,'user_name':request.session['user_name'],'BASE_URL': settings.BASE_URL})

#
# def add_story_point(request):
#     org_info = AR_organization.objects.filter(id=request.session['org_id'])
#     #####################################
#     if request.method == "POST":
#         ar_backlog_form = Ar_Backlog_Form(org_info,request.POST)
#         if ar_backlog_form.is_valid():
#             title = ar_backlog_form.cleaned_data.get('title')
#             if AR_BACKLOG.objects.filter(title=title).filter(ORG_ID=request.session['org_id']).exists():
#                 messages.error(request, "Backlog already exists.")
#             else:
#                 created_by_ins = get_object_or_404(Ar_user, pk=request.session['user_id'])
#                 org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
#                 data = ar_backlog_form.save(commit=False)
#                 data.created_by=created_by_ins
#                 data.updated_by = created_by_ins
#                 data.backlog_score = 0
#                 data.Backlog_size = 0
#                 data.ORG_ID=org_ins
#                 try:
#                     data.save()
#                     messages.info(request, "Backlog added successfully !")
#                     return redirect(settings.BASE_URL + 'manage-backlog')
#                 except:
#                     messages.error(request, ar_backlog_form.errors)
#
#
#         else:
#             messages.error(request, ar_backlog_form.errors)
#     else:
#         ar_backlog_form=Ar_Backlog_Form(org_info)
#     return redirect(settings.BASE_URL + 'manage-backlog')
