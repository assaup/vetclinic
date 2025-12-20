from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/add/', views.service_create, name='service_add'),
    path('services/<int:pk>/edit/', views.service_update, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
]
    