import datetime
from django.core.management.base import BaseCommand, CommandError
from front.models import Games


class Command(BaseCommand):
    help = "Удалить игры которые начались и подвисли/или намеренно не закончены"

    def handle(self, *args, **options):
        Games.objects.filter(start_time_lte=(datetime.datetime.now() - datetime.timedelta(hours=1)), done=False)