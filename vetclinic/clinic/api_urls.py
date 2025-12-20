from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet
from .views import AppointmentViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls
