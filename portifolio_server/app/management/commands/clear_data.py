from django.core.management.base import BaseCommand
from app.models import Newsletter, NewsletterSubscriber  # Import your models

class Command(BaseCommand):
    help = 'Clear data from specified models'

    def handle(self, *args, **kwargs):
        # Clear data from specific models
        Newsletter.objects.all().delete()
        NewsletterSubscriber.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Data cleared successfully'))