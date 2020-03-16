import io,csv
from django.shortcuts import get_object_or_404
from user_story_points.models import ArUserStoryPoints
from datetime import datetime
from account.models import Ar_user,Notification
from data_import_export.models import import_files_data
from django.contrib.auth.models import User
import string
import random
from agileproject import settings


def read_ArUserStoryPoints_csv(file_ins,org_ins,file_name_value,file_name_txt,user_id):
    file2 = open(file_name_txt, "w+")
    csv_file = file_ins.files
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    get_data = csv.reader(io_string, delimiter=',', quotechar="|")
    created_by_ins = get_object_or_404(Ar_user, pk=user_id)
    updateded_by_ins = get_object_or_404(Ar_user, pk=user_id)
    file_name = get_data
    i=2

    total_data = 0
    import_data = 0
    empty_data = 0
    exists_data = 0
    other_error = 0


    i=2
    try:

        for item in file_name:
            if item[0] == "":
                empty_data += 1
                file2.write(
                    "Error : " + str(file_name_value) + " : row no. : " + str(i) + " : Point_Key is empty. : " + str(datetime.now()) + "\r\n")
            else:
                if ArUserStoryPoints.objects.filter(Point_Key=item[0]).filter(ORG_ID=org_ins).exists():
                    exists_data += 1
                    msg = get_object_or_404(Notification, page_name="Manage User Story Points",notification_key="Exists")
                    msg_data = msg.notification_desc
                    file2.write("Error : " + str(file_name_value) + " : row no. : " + str(i) + " : " + msg_data + " : " + str(datetime.now()) + "\r\n")
                else:
                    if item[3] != "":
                        try:
                            created_by_ins_id = int(item[3])
                            if Ar_user.objects.filter(id=created_by_ins_id).filter(org_id=org_ins).exists():
                                created_by_ins = get_object_or_404(Ar_user, pk=created_by_ins_id)
                        except:
                            if Ar_user.objects.filter(user_name=item[3]).filter(org_id=org_ins).exists():
                                created_by_ins = get_object_or_404(Ar_user, user_name=item[3], org_id=org_ins)
                    if item[5] != "":
                        try:
                            updateded_by_ins_id = int(item[5])
                            if Ar_user.objects.filter(id=updateded_by_ins_id).filter(org_id=org_ins).exists():
                                updateded_by_ins = get_object_or_404(Ar_user, pk=updateded_by_ins_id)
                        except:
                            if Ar_user.objects.filter(user_name=item[5]).filter(org_id=org_ins).exists():
                                updateded_by_ins = get_object_or_404(Ar_user, user_name=item[5], org_id=org_ins)
                    # ger instasnce of create_by and update_by user END
                    # GET DATE START
                    created_dt = datetime.now()
                    updated_dt = datetime.now()
                    # created_dt = item[4]
                    # if created_dt == "":
                    #     created_dt = datetime.now()
                    #
                    # updated_dt = item[6]
                    # if updated_dt == "":
                    #     updated_dt = datetime.now()
                    add_ArUserStoryPoints = ArUserStoryPoints(Point_Key=item[0],Point_Description=item[1],Point_score=item[2],ORG_ID=org_ins,create_by=created_by_ins,create_dt=created_dt,update_by=updateded_by_ins,update_dt=updated_dt)
                    try:
                        add_ArUserStoryPoints.save()
                        file2.write("Success : " + str(file_name_value) + " : row no. : " + str(i) + " : '" + item[1] + "' user story point add successfully : " + str(datetime.now()) + "\r\n")
                        import_data += 1
                    except:
                        other_error += 1
                        file2.write("Error : " + str(file_name_value) + " : row no. : " + str(i) + " : Something was wrong in this file : " + str(datetime.now()) + "\r\n")
            i += 1
            total_data += 1
    except:
        other_error += 1
        file2.write("Error : " + str(file_name_value) + " : row no. : " + str(i) + " : Something was wrong in this file : " + str(datetime.now()) + "\r\n")
    file2.close()
    file_name_txt_in_array = file_name_txt.split("media")

    empty_mess = ""
    exists_message = ""
    if empty_data > 0:
        empty_mess = str(empty_data) + " backlog title is empty.,,"
    if exists_data > 0:
        exists_message = str(exists_data) + " backlog already exists."
    file_data_mess = str(total_data) + " total Role .,," + str(import_data) + " Role  import.,," + empty_mess + exists_message + str(other_error) + " other error"
    import_files_data.objects.filter(id=file_ins.id).update(error_log=file_name_txt_in_array[1],file_data=file_data_mess)
    return True