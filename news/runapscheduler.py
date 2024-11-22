from django.core.management.base import BaseCommand
from jobs import scheduler


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **kwargs):
        scheduler.start()
