from django.core.management.base import BaseCommand
from django.utils import timezone
from clinic.models import Appointment, Vet


class Command(BaseCommand):
    help = "Выводит количество будущих приёмов для каждого ветеринара"

    def handle(self, *args, **options):
        now = timezone.now()
        vets = Vet.objects.all()
        if not vets:
            self.stdout.write("Нет ветеринаров в базе")
            return

        for vet in vets:
            count = Appointment.objects.filter(vet=vet, appointment_time__gte=now).count()
            self.stdout.write(f"Ветеринар: {vet.name}, будущие приёмы: {count}")

        self.stdout.write(self.style.SUCCESS("Подсчёт будущих приёмов завершён"))
