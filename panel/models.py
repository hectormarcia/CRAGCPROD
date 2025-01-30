from django.db import models

# Create your models here.

class crastatus(models.Model):
    corporatename = models.CharField(max_length=250, null=False)
    proxyid = models.IntegerField(null=True)
    entityid = models.CharField(max_length=128, null=False)
    programname = models.CharField(max_length=128, null=True)
    programstatus = models.CharField(max_length=128, null=True)
    evaluationfactdi = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    