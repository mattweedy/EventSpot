from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Creates the periodic scraper tasks'

    def handle(self, *args, **options):
        # create schedule: run every day
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        # create task
        PeriodicTask.objects.create(
            interval=schedule,
            name='Scrape event ids task',
            task='backend.core.tasks.scrape_event_ids_task',
        )

        # create task
        PeriodicTask.objects.create(
            interval=schedule,
            name='Get event data task',
            task='backend.core.tasks.get_event_data_task',
        )