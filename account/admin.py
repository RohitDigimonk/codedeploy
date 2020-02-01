from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ar_user,AR_organization,AR_organization_status,ArShowcolumns,csvFilesUplodaded,ArUserProfile,ArUserProfilePermission,Notification,ArUserStoryScoringPoints,ArHelpContect
# Register your models here.

class Ar_userAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['user_name']
    list_display = ('user_name','city','state','zip','country','phone','backup_email','org_id','user_type','login_status','created_dt')


class AR_organization_statusAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['status_key']
    list_display = ('status_key','created_dt','created_by')


class AR_organizationAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['organization_name']
    list_display = ('organization_name','subscription_level','organization_status','created_by','created_dt')

class ArShowcolumnsAdmin(ImportExportModelAdmin):
    search_fields = ['user_id']
    list_display = ('user','ORG','Table_name','columnName')

class csvFilesUplodadedAdmin(ImportExportModelAdmin):
    search_fields = ['ORG_ID']
    list_display = ('attachments','csvUseFor','ORG_ID','created_by')


class ArUserProfileAdmin(ImportExportModelAdmin):
    date_hierarchy = 'create_dt'
    search_fields = ['profile_key']
    list_display = ('profile_key','ORG_ID','create_by','create_dt','update_by','update_dt')

class ArUserProfilePermissionAdmin(ImportExportModelAdmin):
    date_hierarchy = 'create_dt'
    search_fields = ['profile_key']
    list_display = ('profile_key','ORG_ID','activites','editor','viewer','create_by','create_dt','update_by','update_dt')
    list_filter = ('profile_key', 'ORG_ID', 'activites')



class NotificationAdmin(ImportExportModelAdmin):
    search_fields = ['page_name','notification_key']
    list_display = ('page_name','notification_key','notification_desc')
    list_filter = ('page_name','notification_key')

class ArUserStoryScoringPointsAdmin(ImportExportModelAdmin):
    search_fields = ['Score_for','Score_key']
    list_display = ('Score_for','Score_key','Keyword','Score_one','Score_two','Score_three','Last_Update')


class ArHelpContectAdmin(ImportExportModelAdmin):
    search_fields = ['Page_name','Topic']
    list_display = ('Page_name','Page_slug','Topic','Description','Information','Linke_1','Linke_2','Linke_3','create_dt')
    list_filter = ('Page_name', 'Page_slug','Topic')


admin.site.register(ArUserProfilePermission,ArUserProfilePermissionAdmin)
admin.site.register(ArUserProfile,ArUserProfileAdmin)
admin.site.register(Ar_user,Ar_userAdmin)
admin.site.register(AR_organization,AR_organizationAdmin)
admin.site.register(AR_organization_status,AR_organization_statusAdmin)
admin.site.register(ArShowcolumns,ArShowcolumnsAdmin)
admin.site.register(csvFilesUplodaded,csvFilesUplodadedAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(ArUserStoryScoringPoints,ArUserStoryScoringPointsAdmin)
admin.site.register(ArHelpContect,ArHelpContectAdmin)
