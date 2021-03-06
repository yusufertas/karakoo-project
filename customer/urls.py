from django.urls import include
from rest_framework import routers

from customer.views import UserViewSet, CustomerViewSet, LogViewSet, CustomerContactViewSet
from django.urls import re_path as url


router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='user')
router.register('customer', CustomerViewSet, basename='customer')
router.register('log', LogViewSet, basename='log')
router.register('customer_contact', CustomerContactViewSet, basename='customer_contact')
urlpatterns = [
    url(r'', include(router.urls)),
]
