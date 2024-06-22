import random
import pytz
from django.utils import timezone
from django.core.management.base import BaseCommand
from app.models import Project


class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):

        for obj in Project.objects.all():
            obj.sort_order = obj.pk
            obj.save()
        

        self.stdout.write(self.style.SUCCESS('populated sort_order with primary key'))

        