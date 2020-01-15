from django.db import models
import django
from account.models import Ar_user,AR_organization



# Create your models here.
###########################
class ArUserStoryPoints(models.Model):
    point_desc   = models.CharField(max_length=80,blank=False)
    size  = models.BigIntegerField(default=0)
    create_by = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='create_by_stroypoints')
    create_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_by = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='update_by_storypoints')
    update_dt = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.point_desc)
###########################