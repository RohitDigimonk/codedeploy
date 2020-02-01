from django.db import models
import django
from django.contrib.auth.models import User
from account.models import Ar_user,AR_organization

# Create your models here.
###########################
class ArUserStoryPoints(models.Model):
    Point_Key   = models.CharField(max_length=50,default='Point_Key')
    Point_Description  = models.TextField(default='Set Description')
    Point_score = models.BigIntegerField(default=10)
    ORG_ID   = models.ForeignKey(AR_organization,default="",null=True , on_delete='models.SET_NULL')
    create_by = models.ForeignKey(Ar_user,  on_delete='models.SET_NULL', related_name='UserCreateBy',default="")
    create_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_by = models.ForeignKey(Ar_user,  on_delete='models.SET_NULL', related_name='UserUpdateBy',default="")
    update_dt = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.Point_Key)
