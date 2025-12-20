from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django pages
    path('', include('clinic.urls')),

    # API
    path('api/', include('clinic.api_urls')),
]
