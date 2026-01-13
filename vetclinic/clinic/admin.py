from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportMixin
from .resources import AppointmentResource
from django.utils import timezone
from .models import (
    Client,
    Pet,
    Vet,
    Service,
    Appointment,
    VetService,
    AppointmentStatus,
    VetSpecialization,
    ServiceCategory,
)


# Inline для питомцев в Client
class PetInline(admin.TabularInline):
    model = Pet
    extra = 1
    raw_id_fields = ('owner',)
    readonly_fields = ('created_at',)


# Service
@admin.register(Service)
class ServiceAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    list_display_links = ('name',)


# Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'pets_count')
    search_fields = ('name', 'phone', 'email')
    inlines = [PetInline]
    date_hierarchy = 'created_at'

    @admin.display(description='Количество питомцев')
    def pets_count(self, obj):
        return obj.pets.count()


# Pet
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'species', 'breed', 'birth_date', 'created_at')
    list_filter = ('species', 'birth_date')
    search_fields = ('name', 'owner__name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('owner',)


# Vet
@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'created_at')
    list_filter = ('specialization',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    filter_horizontal = ()
    raw_id_fields = ()
    readonly_fields = ('created_at',)


# Appointment
@admin.register(Appointment)
class AppointmentAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = AppointmentResource
    list_display = (
        'pet',
        'vet',
        'service',
        'status',
        'appointment_time',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'vet', 'service', 'appointment_time')
    search_fields = ('pet__name', 'vet__name', 'service__name')
    date_hierarchy = 'appointment_time'
    raw_id_fields = ('pet', 'vet', 'service', 'status')
    readonly_fields = ('created_at', 'updated_at')

    def get_export_queryset(self, request):
        return self.model.objects.filter(appointment_time__gte=timezone.now())


# VetService
@admin.register(VetService)
class VetServiceAdmin(admin.ModelAdmin):
    list_display = ('vet', 'service', 'created_at')
    list_filter = ('vet', 'service')
    search_fields = ('vet__name', 'service__name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('vet', 'service')
    readonly_fields = ('created_at',)


# Справочники
@admin.register(AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(VetSpecialization)
class VetSpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
