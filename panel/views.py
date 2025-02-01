from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from coupaconnect.utility import coupa_oauth, getcoresupplierdetails, getproxysupplierdetails, getcrasupplierfields
from supplier.models import Supplier, Compliance_threshhold
from panel.models import CRAstatus, CraFtpLog
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

    if object_type != "supplier":
        error_desc = "The context is wrong, please talk to your administrator"
    else:
        json_auth = coupa_oauth()
        if json_auth:
            access_token = json_auth['access_token']
            proxyid = getproxysupplierdetails(access_token, 74676)
            if proxyid == 0:
                error_desc = "This supplier is not linked to CRA yet"
            else:
                supplier_guid = None
                cras = CRAstatus.objects.filter(proxyid=proxyid)
                if len(cras) > 0:
                    cra = cras[0]
                    supplier_guid = cra.entityid
            
            if supplier_guid:
                fields = getcrasupplierfields(access_token, supplier_guid)
            else:
                error_desc = "This supplier is not linked to CRA yet"
        
        cras = CRAstatus.objects.filter(entityid=supplier_guid).values('programname','programstatus', 'updatedate')
    
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
        "programmes": list(cras),
        "comths": list(comths),
        "lastupdate": maxval
    }
    
    if len(fields) > 0:
        for field in fields:
            if  field['value']:
                context[field['name']] = field['value']
            # if field['name'] == 'kyc_tpdd_applicable':
            #     context['kyc_tpdd_applicable'] = field['kyc_tpdd_applicable'] 
            # if 'risk_assess_index' in field:
            #     context['risk_assess_index'] = field['risk_assess_index'] 
            # if 'risk_assess_index_date' in field:
            #     context['risk_assess_index_date'] = field['risk_assess_index_date']
            # if 'block_reason' in field:
            #     context['block_reason'] = field['block_reason']
            # if 'block_date' in field:
            #     context['block_date'] = field['block_date']
            # if 'kcy_expiry_date' in field:
            #     context['kcy_expiry_date'] = field['kcy_expiry_date']
            # if 'tpdd_expiry_date' in field:
            #     context['tpdd_expiry_date'] = field['tpdd_expiry_date']
            # if 'kyc_risk_level' in field:
            #     context['kyc_risk_level'] = field['kyc_risk_level']
            # if 'tpdd_type' in field:
            #     context['tpdd_type'] = field['tpdd_type']
            # if 'tpdd_contract_end_date' in field:
            #     context['tpdd_contract_end_date'] = field['tpdd_contract_end_date']
    
    return render (request,'supplierdetail.html', context)

def crastatuslist(request):
    cras = CRAstatus.objects.all()
    context = {
        'cras': list(cras)
    }
    return render (request,'crastatus.html', context)
