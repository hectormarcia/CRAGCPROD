from django.shortcuts import render
from django.conf import settings
# from ftplib import FTP
import pysftp
import csv
from panel.models import CRAstatus, CraFtpLog
from .models import Compliance_threshhold
import datetime

def filetosql(csvfile):
    print('FTP PROCESS ROWS')
    csvfile.seek(3) # read past the BOM
    reader = csv.DictReader(csvfile)    
    count = 0
    for row in reader:
        count += 1
        if 'Evaluation Fact DI' in row:
            thekey = row['Evaluation Fact DI']
        if 'Evaluation Fact ID' in row:
            thekey = row['Evaluation Fact ID']
        cras = CRAstatus.objects.filter(evaluationfactdi=thekey)
        if len(cras) > 0:
            cra = cras[0]
        else:
            cra = CRAstatus(evaluationfactdi=thekey)
        if 'Corporate Name' in row:
            cra.corporatename = row['Corporate Name']
        if 'Proxy ID' in row:
            cra.proxyid = row['Proxy ID']
        if 'Entity ID' in row:
            cra.entityid = row['Entity ID']
        if 'Program Name' in row:
            cra.programname = row['Program Name']
        if 'Program Status' in row:
            cra.programstatus = row['Program Status']
        if 'Evaluation Fact ID' in row:
            cra.evaluationfactdi = row['Evaluation Fact ID']
        if 'Evaluation Fact DI' in row:
            cra.evaluationfactdi = row['Evaluation Fact DI']
        if 'Create Date' in row:
            cra.createdate = row['Create Date']
        if 'Modify Date' in row:
            cra.updatedate = row['Modify Date']
        cra.save()
        print(row)
    
    return count

def processftpfile(sftp, filename):
    # cnopts = pysftp.CnOpts()
    # cnopts.hostkeys = None
    # sftp = pysftp.Connection(SFTP_HOST, username=SFTP_USERNAME, port=SFTP_PORT, password=SFTP_PASSWORD, cnopts=cnopts)
    sftp.cwd(settings.SFTP_DIRECTORY)
    frompath = settings.SFTP_DIRECTORY + '/' + filename
    nowtime = datetime.datetime.now()
    nowtimestring = nowtime.strftime('%Y%m%d_%H%M%S')
    tofile = filename.replace('.csv', ' (' + nowtimestring + ')') + '.csv'
    topath = settings.SFTP_DIRECTORY + '/' + tofile
    sftp.rename(frompath, topath)
    with sftp.open(topath, 'r', 32768) as f:
        count = filetosql(f)
    log = CraFtpLog(filename=filename, records=count)
    log.save()

# Create your views here.
def syncFTP(request):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    # print("FTP SETTINGS:")
    # print("\tHOST: {}\n\tUSERNAME: {}\n\tPORT: {}\n\tPASSWORD: {}\n".format(settings.SFTP_HOST, settings.SFTP_USERNAME, settings.SFTP_PORT,settings.SFTP_PASSWORD ))
    # print("\tHOST: {}\n\tUSERNAME: {}\n\tPORT: {}\n\tPASSWORD: {}\n".format(settings.SFTP_HOST, settings.SFTP_USERNAME, settings.SFTP_PORT,settings.SFTP_PASSWORD ))
    
    ftpport = int(settings.SFTP_PORT)
    sftp = pysftp.Connection(settings.SFTP_HOST, username=settings.SFTP_USERNAME, port=ftpport, password=settings.SFTP_PASSWORD, cnopts=cnopts)
    
    if request.method == "POST":
        data = request.POST
        filename = data.get('filename')
        processftpfile(sftp, filename)

    sftp.cwd(settings.SFTP_DIRECTORY)
    files = sftp.listdir()
    # for file in files:
    #     print(file)
        
    context = {
        "files": files
    }
    return render (request,'ftplist.html', context)

def supplierlist(request):
    comths = Compliance_threshhold.objects.all().prefetch_related('supplier')
    
    context = {
        "comths": comths
    }
    
    return render (request,'supplierlist.html', context)