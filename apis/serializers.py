from rest_framework import serializers

# import model from models.py
from supplier.models import Supplier, Company, Compliance_threshhold

# class ComplianceThresholdSerializer(serializers.HyperlinkedModelSerializer):
class ComplianceThresholdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # specify model and fields
    class Meta:
        model = Compliance_threshhold
        fields = ('id', 'legal_entity', 'total_year', 'spend_non_po_invoices','spend_purchase_orders','spend_total','spend_threshold','spend_currency')
        read_only_fields = ('id',)

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # specify model and fields
    class Meta:
        model = Company
        fields = ('id','code', 'posting_block_1', 'purchase_block_2','payment_block_3','payment_block_type')
        read_only_fields = ('id',)

# Create a model serializer
class SupplierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    compliance_thresholds = ComplianceThresholdSerializer(many=True,required=False, allow_null=True)
    company = CompanySerializer(required=False, allow_null=True)

    # specify model and fields
    class Meta:
        model = Supplier
        fields = ('id','coupa_supplier_id', 'coupa_sim_id', 'system_id_1','company', 'compliance_thresholds')
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Custom validation logic for the whole serializer.
        """
        
        if 'coupa_supplier_id' not in data:
            raise serializers.ValidationError({'Error': 'coupa_supplier_id is mandatory'})

        return data

    def upsert(self, validated_data):
        """ 
        Do a custom create / update due to payload complexity and 'hidden' key fields 
        """
        supplier_coupa_supplier_id = validated_data['coupa_supplier_id'] # this is the actual PK
        supplier_coupa_sim_id = None
        if 'coupa_sim_id' in validated_data:
            supplier_coupa_sim_id = validated_data['coupa_sim_id']

        # find supplier on coupa_supplier_id
        sups = Supplier.objects.filter(coupa_supplier_id=supplier_coupa_supplier_id)
        if len(sups) > 0: #we have it!
            instance = sups[0]
        else:
            # create the supplier
            instance = Supplier(coupa_supplier_id=supplier_coupa_supplier_id,coupa_sim_id=supplier_coupa_sim_id)
            instance.save()

        cths = None
        try:
            cths = validated_data.pop('compliance_thresholds')
        except:
            pass

        cpy = None
        try:
            cpy = validated_data.pop('company')
            if 'posting_block_1' in cpy:
                company_posting_block_1 = cpy['posting_block_1']
            if 'purchase_block_2' in cpy:
                company_purchase_block_2 = cpy['purchase_block_2']
            if 'payment_block_3' in cpy:
                company_payment_block_3 = cpy['payment_block_3']
            if 'payment_block_type' in cpy:
                company_payment_block_type = cpy['payment_block_type']
            if 'code' in cpy:
                company_code = cpy['code']
            i_company = None
            if instance.company:
                i_company = instance.company
            else:
                i_company = Company()
            i_company.posting_block_1 = company_posting_block_1
            i_company.purchase_block_2 = company_purchase_block_2
            i_company.payment_block_3 = company_payment_block_3
            i_company.payment_block_type = company_payment_block_type
            i_company.code = company_code
            i_company.save()
            
            instance.company = i_company
            instance.save()
            
            # savedcpy = Company.objects.create(**cpy)
            # validated_data['company_id'] = savedcpy.id
        except:
            pass        

        # if 'id' in validated_data:
        #     validated_data.pop('id')
        # instance = Supplier.objects.create(**validated_data)
        
        if cths:
            for cth in cths:
                if 'legal_entity' in cth:
                    ct_legal_entity = cth['legal_entity']
                if 'total_year' in cth:
                    ct_total_year = cth['total_year']
                if 'spend_non_po_invoices' in cth:
                    ct_spend_non_po_invoices = cth['spend_non_po_invoices']
                if 'spend_purchase_orders' in cth:
                    ct_spend_purchase_orders = cth['spend_purchase_orders']
                if 'spend_total' in cth:
                    ct_spend_total = cth['spend_total']
                if 'spend_threshold' in cth:
                    ct_spend_threshold = cth['spend_threshold']
                if 'spend_currency' in cth:
                    ct_spend_currency = cth['spend_currency']
                # cth['supplier_id'] = instance.id
                # Compliance_threshhold.objects.create(**cth)
                cts = Compliance_threshhold.objects.filter(supplier=instance, legal_entity=ct_legal_entity, total_year=ct_total_year)
                if len(cts) > 0:
                    # we have one!
                    comp_th = cts[0]
                else:
                    comp_th = Compliance_threshhold()
                    comp_th.supplier = instance
                comp_th.legal_entity = ct_legal_entity
                comp_th.total_year = ct_total_year
                comp_th.spend_non_po_invoices = ct_spend_non_po_invoices
                comp_th.spend_purchase_orders = ct_spend_purchase_orders
                comp_th.spend_total = ct_spend_total
                comp_th.spend_threshold = ct_spend_threshold
                comp_th.spend_currency = ct_spend_currency
                comp_th.save()

        return instance


    def create(self, validated_data):
        return self.upsert(validated_data)
    
        cths = None
        try:
            cths = validated_data.pop('compliance_thresholds')
        except:
            pass
        
        cpy = None
        try:
            cpy = validated_data.pop('company')
            if 'id' in cpy:
                cpy.pop('id')
            savedcpy = Company.objects.create(**cpy)
            validated_data['company_id'] = savedcpy.id
        except:
            pass
        
        if 'id' in validated_data:
            validated_data.pop('id')
        instance = Supplier.objects.create(**validated_data)

        if cths:
            for cth in cths:
                if 'id' in cth:
                    cth.pop('id')
                cth['supplier_id'] = instance.id
                Compliance_threshhold.objects.create(**cth)
        return instance

    def update(self, instance, validated_data):
        return self.upsert(validated_data)
    
        cths = None
        try: 
            cths = validated_data.pop('compliance_thresholds')
        except:
            pass

        cpy = None
        try:
            cpy = validated_data.pop('company')
            companyid = cpy['id']
            cpy.pop('id')
            Company.objects.filter(pk=companyid).update(**cpy)
            # validated_data['company_id'] = savedcpy
        except Exception as e:
            pass
        
        if id in validated_data:
            validated_data.pop('id')
        Supplier.objects.update(**validated_data)
        if cths:
            for cth in cths:
                ctid = cth['id']
                cth.pop('id')
                Compliance_threshhold.objects.filter(pk=ctid).update(**cth)
        return instance


 