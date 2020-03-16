from account.models import AR_organization,Ar_user
from manage_backlogs.models import AR_BACKLOG
from manage_epic_capability.models import AR_EPIC_CAPABILITY
from manage_features.models import AR_FEATURE
from user_story_points.models import ArUserStoryPoints
from user_story_view.models import AR_USER_STORY
from manage_iterations.models import ArIterations
from manage_role.models import ArRole
from manage_goals.models import ArManageGoals
from manage_benefits.models import ArManageBenefits
import xlsxwriter
from datetime import date
from manage_backlogs.templatetags import add_value
import pathlib
import csv
import os



def get_ar_backlog_data(org_ins,worksheet):
    if AR_BACKLOG.objects.filter(ORG_ID=org_ins).exists():
        data = AR_BACKLOG.objects.filter(ORG_ID=org_ins)
        worksheet.write('A1', "title")
        worksheet.write('B1', "owner")
        worksheet.write('C1', "backlog_score")
        worksheet.write('D1', "Backlog_size")
        worksheet.write('E1', "team_list")
        worksheet.write('F1', "product_parent")
        worksheet.write('G1', "BL_STATUS")
        worksheet.write('H1', "created_by")
        worksheet.write('I1', "created_dt")
        worksheet.write('J1', "updated_by")
        worksheet.write('K1', "updated_dt")
        worksheet.write('L1', "organization_name")
        i = 2
        for rows in data:
            print(i)
            worksheet.write('A' + str(i), str(rows.title))
            worksheet.write('B' + str(i), str(rows.owner))
            worksheet.write('C' + str(i), str(add_value.back_scr(org_ins.organization_name,rows.id)))
            worksheet.write('D' + str(i), str(add_value.size(org_ins.organization_name,rows.id)))
            worksheet.write('E' + str(i), str(list_to_string_team_member(rows.team_list.all())))
            worksheet.write('F' + str(i), str(rows.product_parent))
            worksheet.write('G' + str(i), str(rows.BL_STATUS))
            worksheet.write('H' + str(i), str(rows.created_by))
            worksheet.write('I' + str(i), str(rows.created_dt))
            worksheet.write('J' + str(i), str(rows.updated_by))
            worksheet.write('K' + str(i), str(rows.updated_dt))
            worksheet.write('L' + str(i), str(org_ins.organization_name))
            i += 1
    return True




def get_ar_backlog_data_CSV(org_ins, file_name):
    if AR_BACKLOG.objects.filter(ORG_ID=org_ins).exists():
        data = AR_BACKLOG.objects.filter(ORG_ID=org_ins)
        with open(file_name, mode='w') as data_file:
            file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(["title","owner","backlog_score","Backlog_size","team_list","product_parent","BL_STATUS","created_by","created_dt","updated_by","updated_dt","organization_name"])
            for rows in data:
                file_writer.writerow([str(rows.title),str(rows.owner),str(add_value.back_scr(org_ins.organization_name,rows.id)),str(add_value.size(org_ins.organization_name,rows.id)),str(list_to_string_team_member(rows.team_list.all())),str(rows.product_parent),str(rows.BL_STATUS),str(rows.created_by),str(rows.created_dt),str(rows.updated_by),str(rows.updated_dt),str(org_ins)])
    return True


def list_to_string_team_member(objcts):
    data = ""
    i=0
    for items in objcts:
        if i == 0:
            data = items.Team_name
        else:
            data +="|"+str(items.Team_name)
        i += 1
    return data