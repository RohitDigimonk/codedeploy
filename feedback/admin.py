from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import ArFeedback, ArSendFeedbackEmail
# Register your models here.

class ArFeedbackAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['feedback_nature','page_name']
    list_display = ('page_name','feedback_nature','feedback_information','attachments','created_by','created_dt')
admin.site.register(ArFeedback,ArFeedbackAdmin)


class ArSendFeedbackEmailAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['page_name']
    list_display = ('page_name','feedback_id','user_id','status','sent_date','created_dt')
admin.site.register(ArSendFeedbackEmail,ArSendFeedbackEmailAdmin)
