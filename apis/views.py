from django.shortcuts import render

# Create your views here.
# import viewsets
from rest_framework import viewsets

# import local data
from .serializers import SupplierSerializer, CompanySerializer, ComplianceThresholdSerializer
from supplier.models import Supplier, Company, Compliance_threshhold

# create a viewset

class SupplierViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = Supplier.objects.all()
	# specify serializer to be used
	serializer_class = SupplierSerializer

class CompanyViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = Company.objects.all()
	# specify serializer to be used
	serializer_class = CompanySerializer
 
class ComplianceThresholdViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = Compliance_threshhold.objects.all()
	# specify serializer to be used
	serializer_class = ComplianceThresholdSerializer
