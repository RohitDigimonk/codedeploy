from django.contrib import admin
from .models import export_data_info,import_files_data,dommy_data
# Register your models here.

class export_data_infoAdmin(admin.ModelAdmin):
    search_fields = ['Score_for','Score_key']
    list_display = ('folder_name','files_name','created_dt')


class import_dataAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    search_fields = ['files']
    list_display = ('file_name','files','file_data','error_log','upload_status','ORG_ID','created_by','created_date','priority')
    list_filter = ('file_name', 'ORG_ID', 'priority')


class dommy_dataAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    search_fields = ['files']
    list_display = ('files','file_name','file_data','upload_status','error_log','created_date','priority')
    list_filter = ('file_name','priority')

admin.site.register(export_data_info,export_data_infoAdmin)
admin.site.register(import_files_data,import_dataAdmin)
admin.site.register(dommy_data,dommy_dataAdmin)

