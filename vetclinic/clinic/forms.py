from django import forms
from django.utils import timezone
from .models import Service, Appointment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'category']

    # 🔹 Валидация цены услуги
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError(
                "Цена услуги должна быть больше 0"
            )
        return price

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'pet',
            'vet',
            'service',
            'status',
            'appointment_time',
        ]
        widgets = {
            'appointment_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }

    # 🔹 1. Проверка даты на будущее
    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')

        if appointment_time and appointment_time < timezone.now():
            raise forms.ValidationError(
                "Дата и время приёма не могут быть в прошлом."
            )
        return appointment_time

    # 🔹 2–4. Бизнес-логика
    def clean(self):
        cleaned_data = super().clean()

        pet = cleaned_data.get('pet')
        vet = cleaned_data.get('vet')
        appointment_time = cleaned_data.get('appointment_time')
        status = cleaned_data.get('status')

        # Проверка статуса
        if status and status.name == 'Завершена':
            raise forms.ValidationError(
                "Нельзя создать приём со статусом «Завершена»."
            )

        # Проверка занятости врача
        if vet and appointment_time:
            if Appointment.objects.filter(
                vet=vet,
                appointment_time=appointment_time
            ).exists():
                raise forms.ValidationError(
                    "У этого врача уже есть приём на выбранное время."
                )

        # Проверка занятости питомца
        if pet and appointment_time:
            if Appointment.objects.filter(
                pet=pet,
                appointment_time=appointment_time
            ).exists():
                raise forms.ValidationError(
                    "У этого питомца уже есть приём на выбранное время."
                )

        return cleaned_data
