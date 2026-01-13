from rest_framework import serializers
from django.utils import timezone
from .models import Appointment, Pet, Vet, Service, Client


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
        pet = attrs.get('pet')
        vet = attrs.get('vet')
        service = attrs.get('service')
        status = attrs.get('status')
        appointment_time = attrs.get('appointment_time')

        # Проверка обязательных полей
        if not all([pet, vet, service, status, appointment_time]):
            raise serializers.ValidationError(
                "Все поля записи на приём должны быть заполнены."
            )

        # Запрет создания приёма со статусом «Завершена»
        if status.name == 'Завершена':
            raise serializers.ValidationError(
                "Нельзя создать приём со статусом «Завершена»."
            )

        # Проверка занятости ветеринара
        if Appointment.objects.filter(
            vet=vet,
            appointment_time=appointment_time
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "У выбранного ветеринара уже есть приём на это время."
            )

        # Проверка занятости питомца
        if Appointment.objects.filter(
            pet=pet,
            appointment_time=appointment_time
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "У данного питомца уже есть приём на это время."
            )

        return attrs


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class PetSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='owner', write_only=True
    )

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'birth_date', 'owner', 'owner_id']


class VetSerializer(serializers.ModelSerializer):
    specialization_name = serializers.CharField(source='specialization.name', read_only=True)

    class Meta:
        model = Vet
        fields = ['id', 'name', 'specialization', 'specialization_name', 'photo', 'created_at']
