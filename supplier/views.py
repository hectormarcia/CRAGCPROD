from django.shortcuts import render
from django.conf import settings
# from ftplib import FTP
import pysftp
import csv
from panel.models import crastatus

def filetosql(csvfile):
    print('FTP PROCESS ROWS')
    csvfile.seek(3) # read past the BOM
    reader = csv.DictReader(csvfile)    
    for row in reader:
        thekey = row['Evaluation Fact DI']
        cras = crastatus.objects.filter(evaluationfactdi=thekey)
        if len(cras) > 0:
            cra = cras[0]
        else:
            cra = crastatus(evaluationfactdi=thekey)
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
        if 'Proxy ID' in row:
            cra.proxyid = row['Proxy ID']
        if 'Create Date' in row:
            cra.createdate = row['Create Date']
        if 'Modify Date' in row:
            cra.updatedate = row['Modify Date']
        cra.save()
        print(row)

def processftpfile(sftp, filename):
    # cnopts = pysftp.CnOpts()
    # cnopts.hostkeys = None
    # sftp = pysftp.Connection(SFTP_HOST, username=SFTP_USERNAME, port=SFTP_PORT, password=SFTP_PASSWORD, cnopts=cnopts)
    sftp.cwd(settings.SFTP_DIRECTORY)
    path = settings.SFTP_DIRECTORY + '/' + filename
    with sftp.open(path, 'r', 32768) as f:
        filetosql(f)

# Create your views here.
def syncFTP(request):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    print("FTP SETTINGS:")
    print("\tHOST: {}\n\tUSERNAME: {}\n\tPORT: {}\n\tPASSWORD: {}\n".format(settings.SFTP_HOST, settings.SFTP_USERNAME, settings.SFTP_PORT,settings.SFTP_PASSWORD ))
    
    sftp = pysftp.Connection(settings.SFTP_HOST, username=settings.SFTP_USERNAME, port=settings.SFTP_PORT, password=settings.SFTP_PASSWORD, cnopts=cnopts)
    
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
