from django.shortcuts import render
# from ftplib import FTP
import pysftp

# Create your views here.
def syncFTP(request):
    SFTP_HOST = 'fileshare-eu-test.coupahost.com'
    SFTP_USERNAME = 'glencore-dev'
    SFTP_PASSWORD = 'X2ymchRWS6fh'
    SFTP_PORT = 22
    SFTP_DIRECTORY = '/Outgoing/CRAPanelApp'
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    sftp = pysftp.Connection(SFTP_HOST, username=SFTP_USERNAME, port=SFTP_PORT, password=SFTP_PASSWORD, cnopts=cnopts)
    sftp.cwd(SFTP_DIRECTORY)
    files = sftp.listdir()
    for file in files:
        print(file)
    
    # ftp = FTP(host='fileshare-eu-test.coupahost.com', user='glencore-dev', passwd='X2ymchRWS6fh', timeout=500)
    # ftp.login() 
    # ftp.cwd('/Outgoing/CRAPanelApp')       
    # list = ftp.retrlines('LIST')
    # for item in list:
    #     print(list)
    
    context = {
        "files": files
    }
    return render (request,'ftplist.html', context)
