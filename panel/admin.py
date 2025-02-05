from django.contrib import admin
from models import ProgramSequence, CraFtpLog, CRAstatus


@admin.register(ProgramSequence)
class ProgramSequenceAdmin(admin.ModelAdmin):
    list_display = ('programname', 'sequence')     

@admin.register(CraFtpLog)
class CraFtpLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'filename', 'records')  

@admin.register(CRAstatus)
class CRAstatusAdmin(admin.ModelAdmin):
    list_display = ('proxyid', 'entityid', 'programname', 'programstatus') 
