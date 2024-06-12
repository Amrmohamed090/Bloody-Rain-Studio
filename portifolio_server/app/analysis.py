
from django.db.models import Count
from .models import Project, Visitor, ProjectVisit, Service
from django.shortcuts import render
from collections import defaultdict
import random
from datetime import datetime, timedelta
import numpy as np
from django.db.models import Count, functions

class DataAnalysis:
    def __init__(self,start_date=None, end_date=None):
        self.projects = Project.objects.all()
        self.services = Service.objects.all()
        self.days_labels = []
        
        
        self.end_date = datetime.now().date() #today
        if start_date is None:    
            self.start_date = self.end_date - timedelta(days=60)  # 60 days ago
        else:
            self.start_date = start_date

        
        current_date = self.start_date
        while current_date <= self.end_date:
            self.days_labels.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)  # Move to the next day




    def get_visits_dataset(self, start_date=None, end_date=None):
        # This function returns the home page visits per day for the time range
        start_d = start_date if start_date else self.start_date
        end_d = end_date if end_date else self.end_date
        
        # Create a dictionary with default value 0 for each day
        visitor_data = defaultdict(int)
        
        # Aggregate and count visitors in the specified time range, grouped by day
        visitor_counts = Visitor.objects \
            .filter(timestamp__gte=start_d, timestamp__lte=end_d +timedelta(days=1)) \
            .annotate(day=functions.TruncDay('timestamp')) \
            .values('day') \
            .annotate(day_count=Count('pk')) \
            .order_by('day')
        # Populate the visitor_data dictionary with visit counts for each day
        for visit in visitor_counts:
            day_str = visit['day'].strftime("%Y-%m-%d")  # Convert to string in the same format as self.days_labels
            visitor_data[day_str] = visit['day_count']   # Use the string as key
            
        # Create a list of visit counts corresponding to each day label
        visitor_data_list = [visitor_data[day] for day in self.days_labels]
        return self.days_labels, visitor_data_list
    


    def get_location_dataset(self):
        
        # Aggregate Visitors based on thier location
        locations_counts = (
        Visitor.objects.values('location').distinct().annotate(count=Count('id')).order_by('-count').filter(count__gt=1)
        )
        # Create dictionaries to store labels and data
        labels = []
        data = []
        # Populate labels and data
        for entry in locations_counts:
            labels.append(entry['location'])
            data.append(entry['count'])
        
        return labels, data


        
    def get_projects_visits_dataset(self):

        # Generate labels representing each project and count views for each project
        project_labels = []
        project_data = []
       
        for project in self.projects:
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

    def get_project_visits_dataset_overtime_2(self,start_date=None, end_date=None):
        end_date = datetime.now().date() +timedelta(days=1)
        if start_date is None:
            start_date = end_date - timedelta(days=60)  # 60 days ago
        #get all project visits in the specific range first
        project_visits_within_range = ProjectVisit.objects.filter(timestamp__range=(start_date, end_date)).order_by('timestamp')
        # Create a dictionary to hold ProjectVisits grouped by day
        project_visits_by_day = defaultdict(list)

        # Iterate over the queryset and group ProjectVisits by day
        for visit in project_visits_within_range:
            visit_day = visit.timestamp.date().strftime("%Y-%m-%d")
            project_visits_by_day[visit_day].append(visit)
        

        #initialize each project independently in a dictionary with key: project.pk
        project_data_set = {}
        for project in self.projects:
            project_data_set[project.pk] = {
                "label": project.project_name,
                "data": defaultdict(int),
               }
        
        #the same for services
        datasets_services = {}
        for service in self.services:
            datasets_services[service.pk] = {
                "label": service.title,
                "data": defaultdict(int),
            }
      
        for i , day in enumerate(project_visits_by_day):
            for visit in project_visits_by_day[day]:
                if visit.project:
                    project_data_set[visit.project.pk]["data"][day] +=1
                if visit.project.project_category:
                    datasets_services[visit.project.project_category.pk]["data"][day] +=1
        
        for project_visit_pk in project_data_set:
            proj_list = [project_data_set[project_visit_pk]["data"][day] for day in self.days_labels]
            project_data_set[project_visit_pk]["data"] = proj_list
            
        final_project_list_dataset = []
        for key in project_data_set:
            #convert array to list
            final_project_list_dataset.append(project_data_set[key])
        
        final_services_list_dataset = []
        for key in datasets_services:
            final_services_list_dataset.append(datasets_services[key])


        
        print(final_project_list_dataset)
        print(final_services_list_dataset)

        ## most viewed services
        mx = 0
        nm = ""     
        for dataset in final_services_list_dataset:
            temp = sum([dataset["data"][day] for day in dataset["data"]])
            if temp > mx:
                mx = temp
                nm = dataset["label"]
            elif temp == mx and temp !=0:
                nm += ", " +  dataset["label"]
        

        return final_project_list_dataset , final_services_list_dataset , nm





    def get_project_visits_dataset_overtime_3(self,start_date=None, end_date=None):
        end_date = datetime.now().date() +timedelta(days=1)
        if start_date is None:
            start_date = end_date - timedelta(days=60)  # 60 days ago
        #get all project visits in the specific range first
        project_visits_within_range = ProjectVisit.objects.filter(timestamp__range=(start_date, end_date)).order_by('timestamp')
        # Create a dictionary to hold ProjectVisits grouped by day
        project_visits_by_day = defaultdict(list)

        # Iterate over the queryset and group ProjectVisits by day
        for visit in project_visits_within_range:
            visit_day = visit.timestamp.date().strftime("%Y-%m-%d")
            project_visits_by_day[visit_day].append(visit)
        

        #initialize each project independently in a dictionary with key: project.pk
        project_data_set = {} 
        for project in self.projects:
            project_data_set[project.pk] = {
                "label": project.project_name,
                "data": np.zeros(len(self.days_labels)),
               }
        
        #the same for services
        datasets_services = {}
        for service in self.services:
            datasets_services[service.pk] = {
                "label": service.title,
                "data": np.zeros(len(self.days_labels)),
            }
      
        for i , day in enumerate(project_visits_by_day):
            for visit in project_visits_by_day[day]:
                if visit.project:
                    project_data_set[visit.project.pk]["data"][i] +=1
                if visit.project.project_category:
                    datasets_services[visit.project.project_category.pk]["data"][i] +=1
        


        final_project_list_dataset = []
        for project_key in project_data_set:
            #convert array to list
            project_data_set[project_key]["data"] = project_data_set[project_key]["data"].tolist()
            final_project_list_dataset.append(project_data_set[project_key])
        
        #for key in datasets_services:

        final_services_list_dataset = []
        for key in datasets_services:
            datasets_services[key]["data"] = datasets_services[key]["data"].tolist()
            final_services_list_dataset.append(datasets_services[key])

        print(final_project_list_dataset)
        print(final_services_list_dataset)

        ## most viewed services
        mx = 0
        nm = ""
        for dataset in final_services_list_dataset:
            temp = sum(dataset["data"])
            if temp > mx:
                mx = temp
                nm = dataset["label"]
            elif temp == mx and temp !=0:
                nm += ", " +  dataset["label"]
        
        return final_project_list_dataset , final_services_list_dataset , nm



