from django.db import models
from simple_history.models import HistoricalRecords

# 1. Справочники
class AppointmentStatus(models.Model):
    name = models.CharField("Статус записи", max_length=50)

    class Meta:
        verbose_name = "Статус записи"
        verbose_name_plural = "Статусы записей"

    def __str__(self):
        return self.name


class VetSpecialization(models.Model):
    name = models.CharField("Специализация", max_length=100)

    class Meta:
        verbose_name = "Специализация ветеринара"
        verbose_name_plural = "Специализации ветеринаров"

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField("Категория услуги", max_length=100)

    class Meta:
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.name


# 2. Основные модели
class Service(models.Model):
    name = models.CharField("Название услуги", max_length=150)
    description = models.TextField("Описание услуги")
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    category = models.ForeignKey(ServiceCategory, verbose_name="Категория", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField("Имя клиента", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Pet(models.Model):
    owner = models.ForeignKey(Client, verbose_name="Владелец", on_delete=models.CASCADE, related_name='pets')
    name = models.CharField("Имя питомца", max_length=100)
    species = models.CharField("Вид", max_length=50)
    breed = models.CharField("Порода", max_length=100, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"

    def __str__(self):
        return f"{self.name} ({self.species})"


class Vet(models.Model):
    name = models.CharField("Имя ветеринара", max_length=100)
    specialization = models.ForeignKey(VetSpecialization, verbose_name="Специализация", on_delete=models.PROTECT)
    photo = models.ImageField("Фото", upload_to='vets/', null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Ветеринар"
        verbose_name_plural = "Ветеринары"

    def __str__(self):
        return f"{self.name} ({self.specialization})"


class Appointment(models.Model):
    pet = models.ForeignKey(Pet, verbose_name="Питомец", on_delete=models.CASCADE)
    vet = models.ForeignKey(Vet, verbose_name="Ветеринар", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name="Услуга", on_delete=models.CASCADE)
    status = models.ForeignKey(AppointmentStatus, verbose_name="Статус", on_delete=models.PROTECT)
    appointment_time = models.DateTimeField("Дата и время приёма")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"

    def __str__(self):
        return f"{self.pet} - {self.service}"


class VetService(models.Model):
    vet = models.ForeignKey(Vet, verbose_name="Ветеринар", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name="Услуга", on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Связь ветеринар-услуга"
        verbose_name_plural = "Связи ветеринар-услуга"
        unique_together = ('vet', 'service')

    def __str__(self):
        return f"{self.vet} - {self.service}"
