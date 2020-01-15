from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ArHelpFile
# Register your models here.

class ArHelpFileAdmin(SummernoteModelAdmin):
# class ArHelpFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_dt'
    search_fields = ['help_topic_title']
    # summernote_fields = ('help_topic_title')
    list_display = ('help_topic_title','help_description','help_text','help_link_1','help_link_2','help_link_3','created_by','created_dt',
                    'updated_by','updated_dt')

admin.site.register(ArHelpFile,ArHelpFileAdmin)