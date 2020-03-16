from django.db import models
from account.models import Ar_user,AR_organization
from manage_product.models import AR_team,AR_product
from manage_backlogs.models import AR_BACKLOG
from user_story_view.models import AR_USER_STORY
import django
# Create your models here.



class ArIterations(models.Model):
    IterationName  = models.CharField(max_length=50,blank=True)
    owner  = models.CharField(max_length=50,blank=True)
    IterationId    = models.TextField(max_length=50)
    StartDate      = models.DateTimeField()
    EndDate        = models.DateTimeField()
    Description    = models.TextField()
    Product        = models.ForeignKey(AR_product, on_delete=models.SET_NULL,related_name='productArIterations',null=True)
    Backlog        = models.ForeignKey(AR_BACKLOG, on_delete=models.SET_NULL,related_name='backlogArIterations',null=True)
    UserStory = models.ManyToManyField(AR_USER_STORY, default="", blank=True,related_name='userstoryArIterations')
    Team           = models.ForeignKey(AR_team, on_delete=models.SET_NULL,related_name='teamArIterations',null=True)
    IterationScore = models.IntegerField(blank=True)
    IterationSize = models.IntegerField(blank=True)
    ORG_ID         = models.ForeignKey(AR_organization, on_delete=models.SET_NULL,related_name='teamArIterations',null=True)
    create_by = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='create_by_iterations')
    create_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_by = models.ForeignKey(Ar_user, on_delete='models.SET_NULL',related_name='update_by_iterations')
    update_dt = models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.IterationName)