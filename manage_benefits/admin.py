from django.contrib import admin
from .models import ArManageBenefits
# Register your models here.

class ArManageBenefitsAdmin(admin.ModelAdmin):
    list_display = ('Benefits_id', 'Benefits_title','Benefits_description','Use_in','ORG_ID','created_by','created_dt','updated_by','updated_dt')
    list_filter = ('Benefits_title', 'ORG_ID', 'created_by')

admin.site.register(ArManageBenefits,ArManageBenefitsAdmin)