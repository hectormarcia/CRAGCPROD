from django.db import models

# Create your models here.

class Company(models.Model):
    code = models.CharField(max_length=80)
    posting_block_1 = models.CharField(max_length=80)
    purchase_block_2 = models.CharField(max_length=80)
    payment_block_3 = models.CharField(max_length=80)
    payment_block_type = models.CharField(max_length=80)

class Supplier(models.Model):
    coupa_supplier_id = models.IntegerField(null=True)
    coupa_sim_id = models.IntegerField(null=True)
    system_id_1 = models.IntegerField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    
class Compliance_threshhold(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='compliance_thresholds')
    legal_entity = models.CharField(max_length=80,null=True)
    total_year = models.CharField(max_length=4,null=True)
    spend_non_po_invoices = models.FloatField(null=True)
    spend_purchase_orders = models.FloatField(null=True)
    spend_total = models.FloatField(null=True)
    spend_threshold = models.FloatField(null=True)
    spend_currency = models.CharField(max_length=4,null=True)
    