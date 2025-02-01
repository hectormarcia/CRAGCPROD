from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from coupaconnect.utility import coupa_oauth, getcoresupplierdetails, getcrasupplierguidbyname, getcrasupplierfields
from supplier.models import Supplier, Compliance_threshhold
from panel.models import crastatus
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
            supdets = getcoresupplierdetails(access_token, object_id)
            supplier_name = supdets['name']
            try:
                supplier_guid = supdets['supplier-risk-detail']['custom-fields']['cra-entityid']
            except:
                supplier_guid = None
                supplier_guid = 'd67d80ad-d198-4c4c-8075-b07e5829793c'
            
            # guid = getcrasupplierguidbyname(access_token, supplier_name)
            if supplier_guid:
                fields = getcrasupplierfields(access_token, supplier_guid)
            else:
                error_desc = "This supplier is not linked to CRA yet"
        
        cras = crastatus.objects.filter(entityid=supplier_guid).values('programname','programstatus', 'created_at', 'updated_at')
    
        sup = Supplier.objects.get(pk=object_id)
        comths = Compliance_threshhold.objects.filter(Supplier=sup)
        
        
    context = {
        "object_id": object_id,
        "object_type": object_type,
        "user_id": user_id,
        "coupahost": coupahost,
        "suppliername": supplier_name,
        "cra_guid": guid,
        "error_desc": error_desc,
        "programmes": list(cras),
        "comths": list(comths)
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
