from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import re_path as url

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # for browsable api
    url(r'api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url for obtaining the token
    url('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url for refreshing the token
    url('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # admin urls
    url(r'admin/', admin.site.urls),
    # api urls with user and customer and log endpoints
    url(r'api/', include('customer.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
