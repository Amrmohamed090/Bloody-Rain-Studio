import random
import pytz
from django.utils import timezone
from django.core.management.base import BaseCommand
from app.models import Visitor, ProjectVisit, Project, Service
def get_random_object(model_class):
    """
    Retrieves all objects from the specified model class, randomly orders them, 
    and selects the first one.

    Args:
        model_class: The Django model class from which to select an object.

    Returns:
        A randomly selected object from the model, or None if no objects exist.
    """

    objects = list(model_class.objects.all().order_by('?'))  # Randomly order objects
    if not objects:
        return None  # Handle case where no objects exist

    return random.choice(objects)



class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('total_views', type=int, help='Indicates the number of dummy views to be created')
        parser.add_argument('total_projects', type=int, help='Indicates the number of dummy project to be created')


    def handle(self, *args, **kwargs):
        total_views = kwargs['total_views']
        total_projects = kwargs['total_projects']

        self.stdout.write(self.style.SUCCESS(f'Creating {total_views} dummy projects...'))

        # have some dummy countries
        countries =  ["Egypt", "Sudan", "Jordan", "USA", "Germany"]
        for _ in range(total_projects):
            self.create_projects()
        # Dummy data generation loop

        self.stdout.write(self.style.SUCCESS(f'Creating {total_views} dummy visitors...'))

        for _ in range(total_views):
            # Generate dummy Visitor data
            visitor_timestamp = self.generate_timestamp()
            visitor = Visitor.objects.create(
                ip_address=f'192.168.{random.randint(0, 255)}.{random.randint(0, 255)}',
                location=random.choice(countries),
                timestamp=visitor_timestamp
            )

            # Randomly select a project

            # Generate dummy ProjectVisit data with associated project
            project_visit_timestamp = self.generate_timestamp_variation(visitor_timestamp)
            project  = get_random_object(Project)

            project_visit = ProjectVisit.objects.create(
                visitor=visitor,
                project=project,
                timestamp=project_visit_timestamp
            )

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))

        
    def generate_timestamp(self):
        # Generate a random timestamp between 2023 and 2025
        start_date = timezone.datetime(2024, 3, 1, tzinfo=pytz.utc)
        end_date = timezone.datetime(2024, 12, 31, 23, 59, 59, tzinfo=pytz.utc)
        random_timestamp = timezone.make_aware(timezone.datetime.fromtimestamp(random.uniform(start_date.timestamp(), end_date.timestamp())), timezone=pytz.utc)
        return random_timestamp

    def generate_timestamp_variation(self, original_timestamp):
        # Add random variation to the original timestamp
        variation_seconds = random.randint(-3600 * 60, 3600* 60)  # Variation between -1 hour to +1 hour
        new_timestamp = original_timestamp + timezone.timedelta(seconds=variation_seconds)
        return new_timestamp

    def create_projects(self):
        # Create some dummy projects and return them
        # You can customize this function based on your Project model
        projects = []
        total_n = len(Project.objects.all())
        for i in range(5):  # Creating 5 dummy projects
            project = Project.objects.create(
                project_name=f'Dummy Project {i+total_n+1}',
                project_description=f'Description for Dummy Project {i+total_n+1}',
            
                
            )
            project.project_category = get_random_object(Service)
            project.save()
            projects.append(project)
        return projects
