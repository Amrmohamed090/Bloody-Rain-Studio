
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from app.models import Image  # Replace 'yourapp' with the actual name of your Django app
from django.conf import settings

class Command(BaseCommand):
    help = 'Upload .png and .jpg images from the media folder to the database'
    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='The directory where the images are stored')

    def handle(self, *args, **options):
        if options['directory'][0] == '/':
            options['directory'] = options['directory'][1:]
        media_directory = os.path.join(settings.BASE_DIR, "media_source", options['directory'])  # Adjust this path based on your MEDIA_ROOT setup

        # Iterate through files in the media directory
        for filename in os.listdir(media_directory):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                full_path = os.path.join(media_directory, filename)

                # Check if an image with this filename already exists in the database
                if Image.objects.filter(name=filename).exists():
                    self.stdout.write(self.style.WARNING(f"Image '{filename}' already exists in the database. Skipping."))
                    continue

                # Create Image instance and save to database
                with open(full_path, 'rb') as f:
                    image_instance = Image(name=filename)
                    image_instance.image.save(filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f"Image '{filename}' uploaded successfully."))

        self.stdout.write(self.style.SUCCESS('Image upload process complete.'))