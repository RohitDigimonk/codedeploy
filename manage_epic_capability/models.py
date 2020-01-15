from django.db import models
import django
from account.models import AR_organization,Ar_user
from manage_product.models import AR_product


# Create your models here.
class AR_EPIC_CAPABILITY(models.Model):
    Cepic_key   = models.CharField(max_length=50)
    Cepic_desc    = models.TextField()
    PROJECT_ID  = models.ManyToManyField(AR_product, default="",blank=True)
    ORG_ID   = models.ForeignKey(AR_organization,default="",null=True , on_delete='models.SET_NULL')
    created_by  = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='create_by_epic')
    create_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_by = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='update_by_epic')
    update_dt = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.Cepic_key)
