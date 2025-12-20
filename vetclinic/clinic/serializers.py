from rest_framework import serializers
from django.utils import timezone
from .models import Appointment, Pet, Vet, Service, AppointmentStatus

class ServiceSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена услуги должна быть больше 0")
        return value

    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    vet_name = serializers.CharField(source='vet.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_appointment_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата и время приёма не могут быть в прошлом.")
        return value
        
    def validate(self, attrs):
        vet = attrs.get('vet')
        appointment_time = attrs.get('appointment_time')
        status = attrs.get('status')

        if status and status.name == 'Завершена':
            raise serializers.ValidationError("Нельзя создать приём со статусом 'Завершена'")

        # Проверка занятости врача
        if Appointment.objects.filter(vet=vet, appointment_time=appointment_time).exists():
            raise serializers.ValidationError("У этого врача уже есть приём на выбранное время")

        # Проверка занятости питомца
        if Appointment.objects.filter(pet=pet, appointment_time=appointment_time).exists():
            raise serializers.ValidationError("У этого питомца уже есть приём на выбранное время")

            
        return attrs
    
