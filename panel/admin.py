from django.contrib import admin
from .models import ProgramSequence, CraFtpLog, CRAstatus

class ProgramSequenceAdmin(admin.ModelAdmin):
    list_display = ('programname', 'sequence')     

class CraFtpLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'filename', 'records')  

class CRAstatusAdmin(admin.ModelAdmin):
    list_display = ('proxyid', 'entityid', 'programname', 'programstatus') 

admin.site.register(ProgramSequence, ProgramSequenceAdmin)
admin.site.register(CraFtpLog, CraFtpLogAdmin)
admin.site.register(CRAstatus, CRAstatusAdmin)
