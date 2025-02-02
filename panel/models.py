from django.db import models

# Create your models here.

class CraFtpLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=250, null=False)
    records =  models.IntegerField(null=True)

class ProgramSequence(models.Model):
    programname = models.CharField(max_length=128)
    sequence = models.IntegerField()

# python3 manage.py shell
# from panel.models import ProgramSequence
# ProgramSequence(sequence=100, programname="Onboarding").save()
# ProgramSequence(sequence=200, programname="Internal Scoping Questionnaire").save()
# ProgramSequence(sequence=300, programname="Internal Diligent TPDD Questionnaire").save()
# ProgramSequence(sequence=400, programname="KYC Copper").save()
# ProgramSequence(sequence=400, programname="KYC - Global").save()
# ProgramSequence(sequence=500, programname="External Goods and Services Questionnaire").save()
# ProgramSequence(sequence=600, programname="SCDD Final Consolidated Review").save()
# ProgramSequence(sequence=700, programname="Supplier Re-assessment Confirmation Program").save()



class CRAstatus(models.Model):
    corporatename = models.CharField(max_length=250, null=False)
    proxyid = models.IntegerField(null=True)
    entityid = models.CharField(max_length=128, null=False)
    programname = models.CharField(max_length=128, null=True)
    programstatus = models.CharField(max_length=128, null=True)
    evaluationfactdi = models.IntegerField(null=True)
    createdate = models.CharField(max_length=80, null=True)
    updatedate = models.CharField(max_length=80, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # programsequence = models.ForeignKey(ProgramSequence, on_delete=models.SET_NULL, null=True, db_column='programname')
    