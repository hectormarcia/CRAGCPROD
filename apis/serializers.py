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

    def create(self, validated_data):
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


 