from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import Booking  # Импорт по правильному имени приложения

class Command(BaseCommand):
    help = 'Удаляет прошедшие бронирования'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired = Booking.objects.filter(end_time__lt=now)
        count = expired.count()
        expired.delete()
        self.stdout.write(f'{count} просроченных бронирований удалено.')
