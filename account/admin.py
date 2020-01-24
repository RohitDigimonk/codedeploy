from django.contrib import admin
from .models import Ar_user,AR_organization,AR_organization_status,ArShowcolumns,csvFilesUplodaded,ArUserProfile,ArUserProfilePermission,Notification,ArUserStoryScoringPoints
# Register your models here.

class Ar_userAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['user_name']
    list_display = ('user_name','city','state','zip','country','phone','backup_email','org_id','user_type','login_status','created_dt')


class AR_organization_statusAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['status_key']
    list_display = ('status_key','created_dt','created_by')


class AR_organizationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['organization_name']
    list_display = ('organization_name','subscription_level','organization_status','created_by','created_dt')

class ArShowcolumnsAdmin(admin.ModelAdmin):
    search_fields = ['user_id']
    list_display = ('user','ORG','Table_name','columnName')

class csvFilesUplodadedAdmin(admin.ModelAdmin):
    search_fields = ['ORG_ID']
    list_display = ('attachments','csvUseFor','ORG_ID','created_by')


class ArUserProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_dt'
    search_fields = ['profile_key']
    list_display = ('profile_key','ORG_ID','create_by','create_dt','update_by','update_dt')

class ArUserProfilePermissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_dt'
    search_fields = ['profile_key']
    list_display = ('profile_key','ORG_ID','activites','editor','viewer','create_by','create_dt','update_by','update_dt')
    list_filter = ('profile_key', 'ORG_ID', 'activites')



class NotificationAdmin(admin.ModelAdmin):
    search_fields = ['page_name','notification_key']
    list_display = ('page_name','notification_key','notification_desc')

class ArUserStoryScoringPointsAdmin(admin.ModelAdmin):
    search_fields = ['Score_for','Score_key']
    list_display = ('Score_for','Score_key','Keyword','Score_one','Score_two','Score_three','Last_Update')

admin.site.register(ArUserProfilePermission,ArUserProfilePermissionAdmin)
admin.site.register(ArUserProfile,ArUserProfileAdmin)
admin.site.register(Ar_user,Ar_userAdmin)
admin.site.register(AR_organization,AR_organizationAdmin)
admin.site.register(AR_organization_status,AR_organization_statusAdmin)
admin.site.register(ArShowcolumns,ArShowcolumnsAdmin)
admin.site.register(csvFilesUplodaded,csvFilesUplodadedAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(ArUserStoryScoringPoints,ArUserStoryScoringPointsAdmin)
