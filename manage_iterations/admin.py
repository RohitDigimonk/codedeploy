from django.contrib import admin
from .models import ArIterations
# Register your models here.
class ArIterationsAdmin(admin.ModelAdmin):
    search_fields = ['IterationName']
    list_display = ('IterationName','owner','IterationId','StartDate','EndDate','Product','Backlog','Team','IterationScore','IterationSize')


admin.site.register(ArIterations,ArIterationsAdmin)