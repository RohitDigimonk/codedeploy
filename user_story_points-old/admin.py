from django.contrib import admin
from .models import ArUserStoryPoints
# Register your models here.

class ArUserStoryPointsAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_dt'
    search_fields = ['point_desc']
    list_display = ('point_desc','size','create_by','create_dt','update_by','update_dt')

admin.site.register(ArUserStoryPoints,ArUserStoryPointsAdmin)