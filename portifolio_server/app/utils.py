import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .analysis import DataAnalysis
import time
from django.utils.translation import gettext_lazy as _

@login_required
def dashboard_callback(request, context):
    
    analysis = DataAnalysis()
    location_labels, location_data = analysis.get_location_dataset()
    
    projects_over_time_datasets , services_over_time_datesets , max_service = analysis.get_project_visits_dataset_overtime_2()
    days_labels , visitor_data = analysis.get_visits_dataset()
    project_labels , project_data = analysis.get_projects_visits_dataset()
    
    #projects_over_time_datasets , services_over_time_datesets , max_service= analysis.get_project_visits_dataset_overtime()
    
    context.update({
        "homePageViews": [
            {
                "title": _("Home page Website Total views over time"),
                "metric": f"{sum(visitor_data)} Views",
                
                "chart": json.dumps(
                    {
                        "labels": days_labels,
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
                                "text": 'Projects Total views'
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
                        "labels": days_labels,
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
                                "text": 'Website Views location'
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
                "metric": f"Most Viewed Service  {max_service}",
                
                "chart": json.dumps(
                    {
                        "labels": days_labels,
                        "datasets": services_over_time_datesets,
                    }
                ),
                
                   "options": json.dumps({
                        "responsive": True,
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": 'Projects Corresponds to Services Views'
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
    })
    return context


    