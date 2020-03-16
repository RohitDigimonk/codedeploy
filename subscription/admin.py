from django.contrib import admin
from .models import Subscription,Payment,MembershipHistory,MembershipRequest
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from agileproject import settings
from django.contrib.auth.models import User,auth
import email.message
import smtplib
class SubscriptionAdmin(ImportExportModelAdmin):
    search_fields = ['Title']
    list_display = ('Title','Price','Undefine_price','Active','All_member','Role_access_and_security','Invite_user','Team','Product','Backlog_per_Product','Rating_cycle','User_story','Time_duration_count','Time_duration_type')

class MembershipRequestAdmin(ImportExportModelAdmin):
    search_fields = ['Request_status']
    list_display = ('Request_from','Organization','Request_for','Request_status','Description','create_dt')


class MembershipHistoryAdmin(ImportExportModelAdmin):
    search_fields = ['Payment_Done']
    list_display = ('Package_name','payment_link','Organization','Root_user','Payment_Done','Price','Active','Active_date','Role_access_and_security','Invite_user','Team','Product','Backlog_per_Product','Rating_cycle','User_story','Time_duration_count','Time_duration_type','create_by','create_dt')
    actions = {'send_payment_link',}



    def payment_link(self,membership):
        return "payment_link"


    def send_payment_link(self,request,queryset):
        default = "Test"
        count_get = queryset
        for item in count_get:
            email_content = str(item.Package_name) +" test data"
            msg = email.message.Message()
            msg['Subject'] = 'Account Create successfully'
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = 'deepaksinghpatel052@gmail.com'
            password = settings.EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            self.message_user(request,"{} payment link sent".format(item))
    send_payment_link.short_description = 'Send payment link'
class PaymentAdmin(ImportExportModelAdmin):
    search_fields = ['Transaction_id']
    list_display = ('payment_port','Organization','Root_user','Payment_method','Payment_Done','Currency_type','Transaction_id')


admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(MembershipHistory,MembershipHistoryAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(MembershipRequest,MembershipRequestAdmin)