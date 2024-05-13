from .models import Visitor
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Project, Visitor, ProjectVisit, Service
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
import random
from datetime import datetime, timedelta
# utils.py

from django.db.models import Count, functions



def get_visits_dataset(start_date=None, end_date=None):
    # Calculate start and end dates if not provided
    if start_date is None:
        end_date = datetime.now().date() #today
        start_date = end_date - timedelta(days=60)  # 60 days ago

    # Generate labels representing each day in the range
    days_labels = []
    current_date = start_date
    while current_date <= end_date:
        days_labels.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)  # Move to the next day
    
    # Aggregate and count visitors in the specified time range, grouped by day
    visitor_counts = (
        Visitor.objects
        .filter(timestamp__gte=start_date, timestamp__lte=end_date)
        .annotate(day=functions.TruncDay('timestamp'))
        .values('day')
        .annotate(day_count=Count('pk'))
        .order_by('day')
    )
    
    # Extract visitor counts for each day
    visitor_data = [visit['day_count'] for visit in visitor_counts]

    return days_labels, visitor_data
def get_location_dataset():
    

    # Generate labels representing each month in the range
    
    # Aggregate and count visitors in the specified time range, grouped by month
    locations_counts = (
    Visitor.objects.values('location').distinct().annotate(count=Count('id')).order_by('-count').filter(count__gt=1)
    )
    # Create dictionaries to store labels and data
    labels = []
    data = []
    print(data)
    # Populate labels and data
    for entry in locations_counts:
        labels.append(entry['location'])
        data.append(entry['count'])
    
    return labels, data


    
def get_projects_visits_dataset():

    # Generate labels representing each project and count views for each project
    project_labels = []
    project_data = []
    projects = Project.objects.all()
    for project in projects:
        n = ""
        for name in project.project_name.split():
            n += name + " "
            if len(n) >= 20:
                break
        project_labels.append(project.project_name)


        views_count = ProjectVisit.objects.filter(
            project=project,
    
        ).count()
        project_data.append(views_count)

    return project_labels , project_data




def get_project_visits_dataset_overtime(start_date=None, end_date=None):
    if start_date is None:
        end_date = datetime.now().date() #today
        start_date = end_date - timedelta(days=60)  # 60 days ago
    
    # Generate labels representing each day in the range
    days_labels = []
    current_date = start_date
    while current_date <= end_date:
        days_labels.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)  # Move to the next day

    datasets_services = {}
    for service in Service.objects.all():
        datasets_services[service.pk] = {
            "label": service.title,
            "data": [0 for _ in days_labels],
        }
    
    # Get unique projects
    projects = Project.objects.all()

    # Initialize the list to store project data
    datasets = []
    
    # Retrieve project views per day
    for project in projects:
        project_name = project.project_name
        visit_counts = []

        # Retrieve visit counts for each day
        for i, day_label in enumerate(days_labels):
            day_start = current_date - timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            visit_count = ProjectVisit.objects.filter(
                project=project,
                timestamp__gte=day_start,
                timestamp__lt=day_end
            ).count()

            visit_counts.append(visit_count)
            if project.project_category:
                datasets_services[project.project_category.pk]["data"][i] += visit_count

        # Create a dictionary for the project data and add it to the datasets list
        datasets.append({
            "label": project_name,
            "data": visit_counts,
        })

    final_services_dataset = []
    mx = 0
    mx_id = []
    for pk in datasets_services:
        final_services_dataset.append(datasets_services[pk])
        sm = sum(datasets_services[pk]["data"]) 
        if sm > mx:
            mx_id = [pk]
            mx = sm
        elif sm == mx:
            mx_id.append(pk)
    max_service = ""
    for i in mx_id:
        max_service += f' : {datasets_services[i]["label"]}'
   
    return datasets , final_services_dataset , max_service
@login_required
def dashboard_callback(request, context):
    location_labels, location_data = get_location_dataset()


    months_labels , visitor_data = get_visits_dataset()
    project_labels , project_data = get_projects_visits_dataset()

    projects_over_time_datasets , services_over_time_datesets , max_service= get_project_visits_dataset_overtime()
    print(2, services_over_time_datesets)
    context.update({
        "homePageViews": [
            {
                "title": _("Home page Website Total views over time"),
                "metric": f"{sum(visitor_data)} Views",
                
                "chart": json.dumps(
                    {
                        "labels": months_labels,
                        "datasets": [
                            {"data": visitor_data},

                        ],
                    }
                ),
                "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Website Total views over time'
                            },
                            "legend": {
                                "display": False,
                                "labels": {
                                    "color": '#9333ea   '
                                }
                            },
                        },
                })
            },
            
        ],

         "ProjectPageViews": [
            
            {
                "title": _("Total Project views "),
                
                "chart": json.dumps(
                    {
                        "labels": project_labels,
                        "datasets": [
                            {"data": project_data, 
                                }
                            
                        ],
                    }
                ),
                   "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Projects views over time'
                            },
                            "legend": {
                                "display": False,
                                "labels": {
                                    "color": '#9333ea   '
                                }
                            },
                        },
                        
                            "barThickness": 10
                })
            },
        ],
        "ProjectViewsOvertime": [
            
            {
                "title": _("Total views per Project"),
                "metric": f"{sum(project_data)} Views",
                
                "chart": json.dumps(
                    {
                        "labels": months_labels,
                        "datasets": projects_over_time_datasets,
                    }
                ),
                
                   "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Projects views over time'
                            },
                            "legend": {
                                "display": True,
                                "labels": {
                                    "color": '#9333ea   '
                                }
                            },
                        },
                        
                         
                })
            },
        ],
        "CountriesChart": [
            
            {
                "title": _("From Where? "),
                "metric": f"Most Views from {location_labels[max(enumerate(location_data), key=lambda x: x[1])[0]]}",
                
                "chart": json.dumps(
                    {
                        "labels": location_labels,
                        "datasets": [{"data": location_data}],
                    }
                ),
                
                   "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Projects views over time'
                            },
                            "legend": {
                                "display": False,
                                "labels": {
                                    "color": '#9333ea   '
                                }
                            },
                        },
                        
                         
                })
            },
        ],
        "ServiceStates": [
            
            {
                "title": _("Projects Corresponds to Services Views"),
                "metric": f"Most project Views aggregated by Service Category is  {max_service}",
                
                "chart": json.dumps(
                    {
                        "labels": months_labels,
                        "datasets": services_over_time_datesets,
                    }
                ),
                
                   "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Projects views over time'
                            },
                            "legend": {
                                "display": False,
                                "labels": {
                                    "color": '#9333ea   '
                                }
                            },
                        },
                        
                         
                })
            },
        ],
    })
    return context


    