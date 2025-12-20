from import_export import resources
from .models import Appointment
from django.utils import timezone

class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment
        fields = ('id', 'pet', 'vet', 'service', 'status', 'appointment_time')
        export_order = ('id', 'pet', 'vet', 'service', 'status', 'appointment_time')

    def dehydrate_pet(self, appointment):
        return appointment.pet.name

    def dehydrate_vet(self, appointment):
        return appointment.vet.name

    def dehydrate_service(self, appointment):
        return appointment.service.name

    def dehydrate_status(self, appointment):
        return appointment.status.name

    def dehydrate_appointment_time(self, appointment):
        return appointment.appointment_time.strftime("%d-%m-%Y %H:%M")
        
    def export(self, queryset=None, **kwargs):
        kwargs['export_headers'] = True
        dataset = super().export(queryset=queryset, **kwargs)
        dataset.encoding = 'utf-8-sig'  # важно для Excel
        return dataset
