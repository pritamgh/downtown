from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = ('organization', 'fest', 'user', 'payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/organization/', include(('organization.urls', 'organization'),
                                      namespace='organization')),
    path('api/v1/fest/', include(('fest.urls', 'fest'), namespace='fest')),
    path('api/v1/user/', include(('user.urls', 'user'), namespace='user')),
    path('api/v1/payment/', include(('payment.urls', 'payment'),
                                 namespace='payment')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
