from django.shortcuts import render, get_object_or_404, redirect
from .models import Service
from .models import Appointment
from .forms import ServiceForm
from rest_framework.viewsets import ModelViewSet
from .serializers import ServiceSerializer
from .serializers import AppointmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer

# Просмотр списка
def service_list(request):
    services = Service.objects.all()
    return render(request, 'clinic/service_list.html', {'services': services})

# Просмотр детали
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'clinic/service_detail.html', {'service': service})

# Добавление
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinic:service_list')
    else:
        form = ServiceForm()
    return render(request, 'clinic/service_form.html', {'form': form})

# Редактирование
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('clinic:service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'clinic/service_form.html', {'form': form})

# Удаление
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('clinic:service_list')
    return render(request, 'clinic/service_confirm_delete.html', {'service': service})

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.select_related('pet', 'vet', 'service', 'status').all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'vet', 'service']  # фильтруем по URL
    search_fields = ['pet__name', 'service__name']   # поиск по GET ?search=

    def get_queryset(self):
        queryset = Appointment.objects.select_related('pet', 'vet', 'service', 'status').all()

        # будущие приёмы, кроме отменённых
        future_appointments = Q(appointment_time__gte=timezone.now()) & ~Q(status__name='Отменена')

        # только приёмы конкретных ветов или конкретной услуги
        specific_vets_or_services = (Q(vet__id=1) | Q(vet__id=2)) & (Q(service__id=1) | Q(service__id=3))

        # Объединяем с OR, чтобы выбрать записи, подходящие под любой из критериев
        combined_filter = future_appointments | specific_vets_or_services

        queryset = queryset.filter(combined_filter)

        return queryset


    # получить все приёмы на сегодня
    @action(methods=['GET'], detail=False)
    def today(self, request):
        today = timezone.localdate()
        appointments = self.get_queryset().filter(
            appointment_time__date=today
        )
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    # пометить приём как завершённый
    @action(methods=['POST'], detail=True)
    def complete(self, request, pk=None):
        appointment = self.get_object()
        completed_status = appointment.status.__class__.objects.get(name='Завершена')
        appointment.status = completed_status
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)