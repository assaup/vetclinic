from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ServiceViewSet, AppointmentViewSet, ClientViewSet, PetViewSet, VetViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'pets', PetViewSet)
router.register(r'vets', VetViewSet)

urlpatterns = [path('', include(router.urls))]
