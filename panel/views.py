from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from coupaconnect.utility import coupa_oauth, getcoresupplierdetails, getproxysupplierdetails, getcrasupplierfields
from supplier.models import Supplier, Compliance_threshhold
from panel.models import CRAstatus, CraFtpLog, ProgramSequence
from django.db.models import Max
# Create your views here.

@xframe_options_exempt
def coupasupplierdetail(request):
    object_id = request.GET.get('object_id', 0)
    object_type = request.GET.get('object_type', 0)
    user_id = request.GET.get('user_id', 0)
    coupahost = request.GET.get('coupahost', 0)
    error_desc = "None"
    supplier_name = ""
    guid = ""
    fields = []
    # cras = []
    sortedlstcras = []
    
    if object_type != "supplier":
        error_desc = "The context is wrong, please talk to your administrator"
    else:
        json_auth = coupa_oauth()
        if json_auth:
            access_token = json_auth['access_token']
            proxyid = getproxysupplierdetails(access_token, object_id)
            supplier_guid = None
            if proxyid == 0:
                error_desc = "This supplier is not linked to CRA yet"
            else:

                cras = CRAstatus.objects.filter(proxyid=proxyid)
                if len(cras) > 0:
                    cra = cras[0]
                    supplier_guid = cra.entityid
            
            if supplier_guid:
                fields = getcrasupplierfields(access_token, supplier_guid)
            else:
                error_desc = "This supplier is not linked to CRA yet"
        
        cras = CRAstatus.objects.filter(entityid=supplier_guid).values('programname','programstatus', 'updatedate') #.order_by('programname')
        lstcras = cras.values()
        sequence = ProgramSequence.objects.all().values()
        
        for cra in lstcras:
            res = next((sub for sub in sequence if sub['programname'] == cra['programname']), None)
            if res:
                cra['sequence'] = res['sequence']
            else:
                cra['sequence'] = 5000

        sortedlstcras = sorted(lstcras, key=lambda x: x['sequence'])

        
        # sup = Supplier.objects.get(pk=object_id)
        sups = Supplier.objects.filter(coupa_supplier_id=object_id)
        if len(sups) > 0:
            sup = sups[0]
            comths = Compliance_threshhold.objects.filter(supplier=sup)
        else:
            comths = []
        
    maxval = None
    try:
        maxval = CraFtpLog.objects.aggregate(Max('created_at'))['created_at__max'] 
    except:
        pass
        
    context = {
        "object_id": object_id,
        "object_type": object_type,
        "user_id": user_id,
        "coupahost": coupahost,
        "suppliername": supplier_name,
        "cra_guid": guid,
        "error_desc": error_desc,
        "programmes": sortedlstcras,
        "comths": list(comths),
        "lastupdate": maxval
    }
    
    if len(fields) > 0:
        for field in fields:
            if  field['value']:
                context[field['name']] = field['value']

    if 'kyc_tpdd_applicable' in context:
        if context['kyc_tpdd_applicable'] == 'tpdd':
            context['ComplianceProcessCategory'] = 'TPDD'
        elif context['kyc_tpdd_applicable'] == 'kyc':
            context['ComplianceProcessCategory'] = 'KYC Full'
        elif context['kyc_tpdd_applicable'] == 'simplified_kyc':
            context['ComplianceProcessCategory'] = 'KYC Simplified'
        elif context['kyc_tpdd_applicable'] == 'kyc_tpdd':
            context['ComplianceProcessCategory'] = 'KYC Exempt'
        else:
            context['ComplianceProcessCategory'] = context['kyc_tpdd_applicable']
    else:
        context['ComplianceProcessCategory'] = 'Not found'
        
    return render (request,'supplierdetail.html', context)

def crastatuslist(request):
    
    cras = CRAstatus.objects.all()
    lstcras = cras.values()
    sequence = ProgramSequence.objects.all().values()
    
    for cra in lstcras:
        res = next((sub for sub in sequence if sub['programname'] == cra['programname']), None)
        if res:
            cra['sequence'] = res['sequence']
        else:
            cra['sequence'] = 5000

    sorted_list = sorted(lstcras, key=lambda x: x['sequence'])

    context = {
        'cras': list(sorted_list)
    }
    return render (request,'crastatus.html', context)
