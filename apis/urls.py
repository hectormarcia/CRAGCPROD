# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

# import everything from views
from .views import SupplierViewSet, CompanyViewSet, ComplianceThresholdViewSet

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used
router.register(r'suppliers', SupplierViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'compliancethresholds', ComplianceThresholdViewSet)

# specify URL Path for rest_framework
urlpatterns = [
	path('', include(router.urls)),
	# path('api-auth/', include('rest_framework.urls'))
]
