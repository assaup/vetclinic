from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Appointment, Pet, Vet, Service, AppointmentStatus
from django.utils import timezone


class AppointmentResource(resources.ModelResource):
    pet = fields.Field(
        column_name='pet',
        attribute='pet',
        widget=ForeignKeyWidget(Pet, 'name')
    )
    vet = fields.Field(
        column_name='vet',
        attribute='vet',
        widget=ForeignKeyWidget(Vet, 'name')
    )
    service = fields.Field(
        column_name='service',
        attribute='service',
        widget=ForeignKeyWidget(Service, 'name')
    )
    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=ForeignKeyWidget(AppointmentStatus, 'name')
    )

    class Meta:
        model = Appointment
        fields = (
            'id',
            'pet',
            'vet',
            'service',
            'status',
            'appointment_time',
        )
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

    def get_export_queryset(self, request):
        return Appointment.objects.filter(
            appointment_time__gte=timezone.now()
        )
