from django.contrib import admin
from .models import ArUserStoryPoints
# Register your models here.

class ArUserStoryPointsAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_dt'
    list_display = ('Point_Key','Point_Description','Point_score','create_by','create_dt','update_by','update_dt')

admin.site.register(ArUserStoryPoints,ArUserStoryPointsAdmin)