from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', views.index, name = "dashboard"),

    path('projects/', views.projects, name = "projects"),
    path('projects/edit/<str:project_no>/', views.edit_project, name = "edit_project"),
    path('projects/delete/<str:project_no>/', views.delete_project, name = "delete_project"),
    path('projects/details/<str:project_id>/', views.project_details, name = "project_details"),
    path('projects/details/milestones/<str:project_id>/', views.milestones, name = "milestones"),
    
    path('project-category/', views.project_category, name = "project_category"),
    path('project-category/add/', views.add_pro_category, name = "add_pro_category"),
    path('project-category/edit/<str:slug>/', views.edit_pro_category, name = "edit_pro_category"),
    path('project-category/delete/<int:pk>/', views.delete_pro_category, name = "delete_pro_category"),
    
    path('training/', views.training, name = "training"),
    path('new-training/', views.new_training, name = "new_training"),
    path('edit-training/<int:train_id>/', views.edit_training, name = "edit_training"),
    path('delete-training/<int:train_id>/', views.delete_training, name = "delete_training"),
    
    path('tasks/', views.tasks, name = "tasks"),
    path('new-task/', views.new_task, name = "new_task"),
    path('edit-task/<int:task_id>/', views.edit_task, name = "edit_task"),
    path('delete-task/<int:task_id>/', views.delete_task, name = "delete_task"),
    
    path('calendars/', views.calendars, name = "calendars"),
    path('api/events/', views.api_get_events, name='api_get_events'),
    path('api/events/add/', views.api_add_event, name='api_add_event'),
    path('api/events/edit/<int:pk>/', views.api_edit_event, name='api_edit_event'),
    path('api/events/delete/<int:pk>/', views.api_delete_event, name='api_delete_event'),
    
    path('new-enrollment/', views.new_enrollment, name="new_enrollment"),
    path('edit-enrollment/<int:enroll_id>/', views.edit_enrollment, name="edit_enrollment"),
    path('delete-enrollment/<int:enroll_id>/', views.delete_enrollement, name="delete_enrollement"),
    path('enrolled-student/', views.enrolled_student, name="enrolled_student"),
    path('cancelled-student/', views.cancelled_student, name="cancelled_student"),

    #app settings
     path('general-setting/', views.general_setting, name="general_setting"),
     path('currencies/', views.currencies, name="currencies"),
     path('email-configuration/', views.email_config, name="email_config"),
     path('email-template/', views.email_template, name="email_template"),
     path('payment-method/', views.payment_method, name="payment_method"),
     path('dashboard-setting/', views.dashboard_setting, name="dashboard_setting"),
     path('training/', views.training, name="training"),
]