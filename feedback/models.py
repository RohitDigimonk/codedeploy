from django.db import models
import django
from django.contrib.auth.models import User
from account.models import Ar_user,AR_organization



# Create your models here.
###########################
class ArFeedback(models.Model):
    page_name   = models.CharField(max_length=50,blank=True)
    feedback_nature  = models.TextField(blank=True)
    feedback_information = models.TextField()
    attachments = models.FileField(upload_to='feedback/')
    created_by = models.ForeignKey(Ar_user, on_delete=models.SET_NULL,related_name='created_by_feedback',null=True )
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.page_name)
    class Meta:
        verbose_name_plural = "Ar feedback"
###########################