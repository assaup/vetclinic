from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='clinic/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout' ),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/add/', views.service_create, name='service_add'),
    path('services/<int:pk>/edit/', views.service_update, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_create, name='appointment_add'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]
    