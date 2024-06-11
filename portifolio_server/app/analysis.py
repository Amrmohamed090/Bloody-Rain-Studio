
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
        
        # this function for the first graph
        # return the home page visits per day for the time range
        
        # Aggregate and count visitors in the specified time range, grouped by day
        visitor_counts = (
            Visitor.objects
            .filter(timestamp__gte=self.start_date, timestamp__lte=self.end_date)
            .annotate(day=functions.TruncDay('timestamp'))
            .values('day')
            .annotate(day_count=Count('pk'))
            .order_by('day')
        )
        # Extract visitor counts for each day
        visitor_data = [visit['day_count'] for visit in visitor_counts]
        print(len(visitor_data))
        print(len(self.days_labels))
        return self.days_labels, visitor_data
    


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
        end_date = datetime.now().date() 
        if start_date is None:
            start_date = end_date - timedelta(days=60)  # 60 days ago
        #get all project visits in the specific range first
        project_visits_within_range = ProjectVisit.objects.filter(timestamp__range=(start_date, end_date)).order_by('timestamp')
        # Create a dictionary to hold ProjectVisits grouped by day
        project_visits_by_day = defaultdict(list)

        # Iterate over the queryset and group ProjectVisits by day
        for visit in project_visits_within_range:
            visit_day = visit.timestamp.date()
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
        for key in project_data_set:
            project_data_set[key]["data"] = project_data_set[key]["data"].tolist()
            final_project_list_dataset.append(project_data_set[key])
        
        final_services_list_dataset = []
        for key in datasets_services:
            datasets_services[key]["data"] = datasets_services[key]["data"].tolist()
            final_services_list_dataset.append(datasets_services[key])

        

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



'''

old function, high complexity
        
    def get_project_visits_dataset_overtime(self, start_date=None, end_date=None):
        end_date = datetime.now().date() 
        if start_date is None:
            start_date = end_date - timedelta(days=60)  # 60 days ago
        
        # Generate labels representing each day in the range
        days_labels = []

        current_date = start_date
        while current_date <= end_date:
            days_labels.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)  # Move to the next day

        datasets_services = {}
        for service in self.services:
            datasets_services[service.pk] = {
                "label": service.title,
                "data": [0 for _ in days_labels],
            }
        


        # Initialize the list to store project data
        datasets = []
        

        # Retrieve project views per day
        for project in self.projects:
            project_name = project.project_name
            visit_counts = []

            # Retrieve visit counts for each day
            for i in range(len(days_labels)):
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

'''

