from django.shortcuts import get_object_or_404
from manage_backlogs.models import AR_BACKLOG
from account.models import AR_organization
from user_story_points.models import ArUserStoryPoints
from django import template
register = template.Library()

@register.simple_tag
def back_scr(pk, id):
    org_ins = get_object_or_404(AR_organization, organization_name=str(pk))
    backlog_data = AR_BACKLOG.objects.filter(ORG_ID=org_ins).filter(pk=id)
    for data in backlog_data:
        QS = 0
        num = 0
        UTP = 0
        point_num = 0
        if data.story_by_backlog.all().count() != 0:
            for val in data.story_by_backlog.all():
                print(val.readiness_quality_score)
                num = num +1
                QS = QS + val.readiness_quality_score
                # if val.story_points_id is not None:
                #     point_num = point_num + 1
                #     UTP_val = get_object_or_404(ArUserStoryPoints, pk=val.story_points_id)
                #     UTP = UTP + UTP_val.Point_score
            TOT = QS + UTP
            num = num + point_num
            if num != 0 :
                tot = TOT/num
                return (int(tot))
        else:
            tot = 0
            return (round(tot,2))




@register.simple_tag
def size(pk, id):
    org_ins = get_object_or_404(AR_organization, organization_name=str(pk))
    backlog_data = AR_BACKLOG.objects.filter(ORG_ID=org_ins).filter(pk=id)
    for data in backlog_data:
        UTP = 0
        if data.story_by_backlog.all().count() != 0:
            for val in data.story_by_backlog.all():
                if val.story_points_id is not None:
                    UTP_val = get_object_or_404(ArUserStoryPoints, pk=val.story_points_id)
                    if UTP_val.Point_score is not None:
                        UTP = UTP + UTP_val.Point_score
        return (UTP)
