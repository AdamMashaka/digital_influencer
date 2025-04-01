from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from courses.models import Courses, Enroll
from dashboard.forms import EventForm
from .models import *
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods


    
# Create your views here.
@login_required(login_url='authenticate:login')
def index(request):
    context = {
        'page' : 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)

def project_category(request):
    categories = Project_Categories.objects.all()
    context = {
        'page' : 'Project Category',
        'categories' : categories,
    }
    return render(request, 'dashboard/projects/category.html', context)

def add_pro_category(request):
    if request.method == 'POST':
        try:
             with transaction.atomic():
                name = request.POST['name']
                slug = slugify(name)

                category = Project_Categories()
                category.name = name
                category.slug = slug
                category.save()
                
                messages.success(request, "Category created successfully!")
                return redirect('dashboard:project_category')
        except Exception as e:
             messages.success(request, f'Category creation failed with: {e}')
             return redirect('dashboard:project_category')
         
    context = {
        'page': 'Add - Category',
    }
    template_name = 'dashboard/projects/add-category.html'
    return render(request, template_name, context)

def edit_pro_category(request, slug):
    category = Project_Categories.objects.get(slug=slug)
    if request.method == 'POST':
        try:
             with transaction.atomic():
                name = request.POST['name']
                slug = slugify(name)
                category.name = name
                category.slug = slug
                category.save()
                
                messages.success(request, "Category Updated successfully!")
                return redirect('dashboard:project_category')
        except Exception as e:
             messages.success(request, f'Category updation failed with: {e}')
             return redirect('dashboard:project_category')
         
    context = {
        'page': 'Edit - Category',
        'category' : category,
    }
    template_name = 'dashboard/projects/edit-category.html'
    return render(request, template_name, context)


def delete_pro_category(request, pk):
    if pk != None:
        try:
            category = Project_Categories.objects.get(id=pk)
            category.delete()
            messages.success(request, "Category deleted successfully!")
            return redirect('dashboard:project_category')
        except Exception as e:
            print(e)
            messages.success(request, f'Category deletion failed with: {e}')
            return redirect('dashboard:project_category')

def generate_project_no():
    last_no = Projects.objects.order_by('-project_no').first()
    
    if last_no:
        last_number = int(last_no.project_no.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f'PRO-{timezone.now().strftime("%Y%m%d")}-{new_number:04d}'


def validate_datetime(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValidationError("Incorrect data format, should be YYYY-MM-DD HH:MM")

def projects(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Validate existence of POST data
                title = request.POST.get('title')
                category_id = request.POST.get('category')
                project_cost = request.POST.get('project_cost')
                priority = request.POST.get('priority')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                assigned_id = request.POST.get('assigned_to')
                description = request.POST.get('description')
                project_no = generate_project_no()
                if not all([title, category_id, project_cost, priority, start_date, end_date, assigned_id, description]):
                    raise ValueError("All fields are required.")

                # Convert and validate dates
                start_date = validate_datetime(start_date)
                end_date = validate_datetime(end_date)

                slug = slugify(title)
                category = get_object_or_404(Project_Categories, id=category_id)
                assigned_to = get_object_or_404(User, id=assigned_id)

                # Create and save the project instance
                project = Projects(project_no=project_no,title=title, slug=slug, category=category, project_cost=project_cost,
                                   priority=priority, start_date=start_date, end_date=end_date,
                                   assigned_to=assigned_to, description=description)
                project.save()

                messages.success(request, "Project created successfully!")
                return redirect('dashboard:projects')
        except Exception as e:
            print(e)
            messages.error(request, f'Project creation failed with: {e}')
            return redirect('dashboard:projects')

    categories = Project_Categories.objects.all()
    users = User.objects.all()
    projects = Projects.objects.all()
    
    new = Projects.objects.filter(status="New Project")
    inprogress = Projects.objects.filter(status="Inprogress")
    pending = Projects.objects.filter(status="Pending")
    complete = Projects.objects.filter(status="Completed")

    new = new.count()
    inprogress = inprogress.count()
    pending = pending.count()
    complete = complete.count()
    
    context = {
        'page' : 'Projects',
        'categories': categories,
        'users': users,
        'new': new,
        'projects': projects,
        'inprogress': inprogress,
        'pending': pending,
        'complete': complete,
    }
    return render(request, 'dashboard/projects/projects.html', context)

def edit_project(request, project_no):
    
    project = Projects.objects.get(project_no=project_no)
    if request.method == "POST":
        try:
            with transaction.atomic():
                title = request.POST.get('title')
                category_id = request.POST.get('category')
                project_cost = request.POST.get('project_cost')
                priority = request.POST.get('priority')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                assigned_id = request.POST.get('assigned_to')
                description = request.POST.get('description')
                project_no = generate_project_no()
                if not all([title, category_id, project_cost, priority, start_date, end_date, assigned_id, description]):
                    raise ValueError("All fields are required.")

                # Convert and validate dates
                start_date = validate_datetime(start_date)
                end_date = validate_datetime(end_date)

                slug = slugify(title)
                category = get_object_or_404(Project_Categories, id=category_id)
                assigned_to = get_object_or_404(User, id=assigned_id)

                # Create and save the project instance
                project.project_no=project_no
                project.title=title 
                project.slug=slug 
                project.category=category 
                project.project_cost=project_cost
                project.priority=priority 
                project.start_date=start_date 
                end_date=end_date
                project.assigned_to=assigned_to
                project.description=description
                project.save()

                messages.success(request, "Project updated successfully!")
                return redirect('dashboard:projects')
        except Exception as e:
            print(e)
            messages.error(request, f'Project updation failed with: {e}')
            return redirect('dashboard:projects')  
        
    categories = Project_Categories.objects.all()
    users = User.objects.all()
    context = {
        'page' : f'Edit Project - {project.project_no}',
        'project': project,
        'categories': categories,
        'users': users,
    }
    return render(request, 'dashboard/projects/edit-project.html', context)

def delete_project(request, project_no):
    if project_no != None:
        try:
            project = Project_Categories.objects.get(project_no=project_no)
            project.delete()
            messages.success(request, "Project deleted successfully!")
            return redirect('dashboard:projects') 
        except Exception as e:
            print(e)
            messages.success(request, f'Project deletion failed with: {e}')
            return redirect('dashboard:projects') 


def project_details(request, project_id):
    project = Projects.objects.get(id=project_id)
    context = {
        'page' : 'Project Details',
        'project' : project,
    }
    return render(request, 'dashboard/projects/project-details.html', context)

def milestones(request, project_id):
    milestones = Milestones.objects.all()
    project = Projects.objects.get(id=project_id)
    users = User.objects.all()
    context = {
        'page' : 'Project Milestones',
        'project' : project,
        'users' : users,
    }
    return render(request, 'dashboard/projects/milestones.html', context)


def training(request):
    trainings = Training.objects.all()
    context = {
        'page' : 'Training',
        'trainings' : trainings,
    }
    return render(request, 'dashboard/training/training.html', context)

def new_training(request):
    users = User.objects.all()

    if request.method == "POST":
        try:
            with transaction.atomic():
                training_name = request.POST.get('training_name')
                user_id = request.POST.get('user')
                assigned_by_id = request.POST.get('assigned_by')
                start_dates = request.POST.get('start_date')
                finish_date = request.POST.get('finish_date')
                vendor_name = request.POST.get('vendor_name')
                training_cost = request.POST.get('training_cost')
                remarks = request.POST.get('remarks') 
                status = request.POST.get('status')
                performance = request.POST.get('performance')
                upload_file = request.FILES.get('upload_file')

                if upload_file:
                    max_upload_size = 10 * 1024 * 1024  # 10 MB
                    if upload_file.size > max_upload_size:
                        messages.error(request, "File size should not exceed 10 MB.")
                        return redirect('dashboard:new_training')

                start_date = validate_datetime(start_dates)
                end_date = validate_datetime(finish_date)

                if start_date <= timezone.now():
                    messages.error(request, "The start date must be greater than today.")
                    return redirect('dashboard:new_training')
                
                if start_date >= finish_date:
                    messages.error(request, "The start date must be before the finish date.")
                    return redirect('dashboard:new_training')
                
                if not all([training_name, user_id, assigned_by_id, start_date, end_date, status]):
                    raise ValueError("Mandatory fields are missing")

                new_training = Training()
                new_training.training_name = training_name
                new_training.user = User.objects.get(id=user_id)
                new_training.assigned_by = User.objects.get(id=assigned_by_id)
                new_training.start_date = start_date
                new_training.finish_date = end_date
                new_training.vendor_name = vendor_name
                new_training.training_cost = training_cost
                new_training.remarks = remarks
                new_training.status = status
                new_training.performance = performance
                new_training.upload_file = upload_file
                new_training.save()

                messages.success(request, "Training created successfully!")
                return redirect('dashboard:training')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('dashboard:training')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('dashboard:training')

    context = {
        'page': 'New Training',
        'users': users,
    }
    return render(request, 'dashboard/training/new-training.html', context)

def edit_training(request, train_id):
    users = User.objects.all()
    training = Training.objects.get(id=train_id)
    
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                training_name = request.POST.get('training_name')
                user_id = request.POST.get('user')
                assigned_by_id = request.POST.get('assigned_by')
                start_dates = request.POST.get('start_date')
                finish_date = request.POST.get('finish_date')
                vendor_name = request.POST.get('vendor_name')
                training_cost = request.POST.get('training_cost')
                remarks = request.POST.get('remarks') 
                status = request.POST.get('status')
                performance = request.POST.get('performance')
                upload_file = request.FILES.get('upload_file')

                if upload_file:
                    max_upload_size = 10 * 1024 * 1024  # 10 MB
                    if upload_file.size > max_upload_size:
                        messages.error(request, "File size should not exceed 10 MB.")
                        return redirect('dashboard:new_training')

                start_date = validate_datetime(start_dates)
                end_date = validate_datetime(finish_date)

                if start_date <= timezone.now():
                    messages.error(request, "The start date must be greater than today.")
                    return redirect('dashboard:new_training')
                
                if start_date >= finish_date:
                    messages.error(request, "The start date must be before the finish date.")
                    return redirect('dashboard:new_training')
                
                if not all([training_name, user_id, assigned_by_id, start_date, end_date, status]):
                    raise ValueError("Mandatory fields are missing")

                training.training_name = training_name
                training.user = User.objects.get(id=user_id)
                training.assigned_by = User.objects.get(id=assigned_by_id)
                training.start_date = start_date
                training.finish_date = end_date
                training.vendor_name = vendor_name
                training.training_cost = training_cost
                training.remarks = remarks
                training.status = status
                training.performance = performance
                training.upload_file = upload_file
                training.save()

                messages.success(request, "Training updated successfully!")
                return redirect('dashboard:training')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('dashboard:training')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('dashboard:training')
    
    context = {
        'page' : 'Edit Training',
        'users' : users,
        'training' : training,
    }
    return render(request, 'dashboard/training/edit-training.html', context)

def delete_training(request, train_id):
    if train_id != None:
        try:
            project = Training.objects.get(id=train_id)
            project.delete()
            messages.success(request, "training deleted successfully!")
            return redirect('dashboard:training') 
        except Exception as e:
            print(e)
            messages.success(request, f'training deletion failed with: {e}')
            return redirect('dashboard:training') 



def tasks(request):
    tasks = Tasks.objects.all()
    users = User.objects.all()
    context = {
        'page' : 'Tasks',
        'tasks' : tasks,
        'users' : users,
    }
    return render(request, 'dashboard/tasks/tasks.html', context)


def new_task(request):
    users = User.objects.all()
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                title = request.POST.get('title')
                user_id = request.POST.get('user')
                assigned_by_id = request.POST.get('assigned_by')
                start_dates = request.POST.get('start_date')
                finish_date = request.POST.get('finish_date')
                remarks = request.POST.get('remarks') 
                status = "New"
                priority = request.POST.get('priority')
                upload_file = request.FILES.get('upload_file')

                if upload_file:
                    max_upload_size = 10 * 1024 * 1024  # 10 MB
                    if upload_file.size > max_upload_size:
                        messages.error(request, "File size should not exceed 10 MB.")
                        return redirect('dashboard:new_task')

                start_date = validate_datetime(start_dates)
                end_date = validate_datetime(finish_date)


                if not all([title, user_id, assigned_by_id, start_date, end_date, status]):
                    raise ValueError("Mandatory fields are missing")

                new_task = Tasks()
                new_task.title = title
                new_task.user = User.objects.get(id=user_id)
                new_task.assigned_by = User.objects.get(id=assigned_by_id)
                new_task.start_date = start_date
                new_task.finish_date = end_date
                new_task.remarks = remarks
                new_task.status = status
                new_task.priority = priority
                new_task.upload_file = upload_file
                new_task.save()

                messages.success(request, "Task created successfully!")
                return redirect('dashboard:tasks')
        except ValidationError as e:
            print(e)
            messages.error(request, str(e))
            return redirect('dashboard:Task')
        except Exception as e:
            print(e)
            messages.error(request, f"An error occurred: {e}")
            return redirect('dashboard:tasks')


def edit_task(request, task_id):
    users = User.objects.all()
    task = Tasks.objects.get(id=task_id)
    url = request.META.get('HTTP_REFERER', '/')
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                title = request.POST.get('title')
                user_id = request.POST.get('user')
                assigned_by_id = request.POST.get('assigned_by')
                start_dates = request.POST.get('start_date')
                finish_date = request.POST.get('finish_date')
                remarks = request.POST.get('remarks') 
                status = request.POST.get('status', task.status)
                priority = request.POST.get('priority')
                upload_file = request.FILES.get('upload_file',task.upload_file)

                if upload_file:
                    max_upload_size = 10 * 1024 * 1024  # 10 MB
                    if upload_file.size > max_upload_size:
                        messages.error(request, "File size should not exceed 10 MB.")
                        return redirect(url)

                start_date = validate_datetime(start_dates)
                end_date = validate_datetime(finish_date)
                
                if not all([title, user_id, assigned_by_id, start_date, end_date, status]):
                    raise ValueError("Mandatory fields are missing")

                task.title = title
                task.user = User.objects.get(id=user_id)
                task.assigned_by = User.objects.get(id=assigned_by_id)
                task.start_date = start_date
                task.finish_date = end_date
                task.remarks = remarks
                task.status = status
                task.priority = priority
                task.upload_file = upload_file
                task.save()

                messages.success(request, "Task updated successfully!")
                return redirect('dashboard:tasks')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect(url)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect(url)
    
    context = {
        'page' : 'Edit Task',
        'users' : users,
        'task' : task,
    }
    return render(request, 'dashboard/tasks/edit-task.html', context)


def delete_task(request, task_id):
    if task_id != None:
        try:
            task = Tasks.objects.get(id=task_id)
            task.delete()
            messages.success(request, "Task deleted successfully!")
            return redirect('dashboard:tasks') 
        except Exception as e:
            print(e)
            messages.success(request, f'Task deletion failed with: {e}')
            return redirect('dashboard:tasks') 



def calendars(request):
    events = Calender_event.objects.all()
    context = {
        'page' : 'Our Calendar',
    }
    return render(request, 'dashboard/calendar/calendar.html', context)

@require_http_methods(["GET"])
def api_get_events(request):
    events = Calender_event.objects.all()
    return JsonResponse(list(events.values()), safe=False)

@require_http_methods(["POST"])
def api_add_event(request):
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save()
        return JsonResponse({'id': event.id}, status=201)
    return JsonResponse(form.errors, status=400)

@require_http_methods(["POST"])
def api_edit_event(request, pk):
    event = Calender_event.objects.get(pk=pk)
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        form.save()
        return JsonResponse({'id': event.id}, status=200)
    return JsonResponse(form.errors, status=400)

@require_http_methods(["DELETE"])
def api_delete_event(request, pk):
    event = Calender_event.objects.get(pk=pk)
    event.delete()
    return JsonResponse({'status': 'success'}, status=204)

def new_enrollment(request):
    users = User.objects.all()
    courses = Courses.objects.all()
    
    if request.method == 'POST':
        try:
             with transaction.atomic():
                student = request.POST['student_id']
                course = request.POST['course_id']
                
                new_enroll = Enroll()
                new_enroll.student = User.objects.get(id=student)
                new_enroll.course = Courses.objects.get(id=course)
                new_enroll.save()
                
                messages.success(request, "Enroll created successfully!")
                return redirect('dashboard:enrolled_student')
        except Exception as e:
             messages.success(request, f'Enroll creation failed with: {e}')
             return redirect('dashboard:enrolled_student')
         
    context = {
        'page': 'New Enrollment',
        'users' : users,
        'courses' : courses,
    }
    template_name = 'dashboard/students/new-enrollment.html'
    return render(request, template_name, context)

def edit_enrollment(request, enroll_id):
    users = User.objects.all()
    courses = Courses.objects.all()
    enroll = Enroll.objects.get(id=enroll_id)
    if request.method == 'POST':
        try:
             with transaction.atomic():
                student = request.POST['student_id']
                course = request.POST['course_id']
                
                enroll.student = User.objects.get(id=student)
                enroll.course = Courses.objects.get(id=course)
                enroll.save()
                
                messages.success(request, "Enroll updated successfully!")
                return redirect('dashboard:enrolled_student')
        except Exception as e:
             messages.success(request, f'Enroll updation failed with: {e}')
             return redirect('dashboard:enrolled_student')
         
    context = {
        'page': 'New Enrollment',
        'users' : users,
        'courses' : courses,
        'enroll' : enroll,
    }
    template_name = 'dashboard/students/edit-enrollment.html'
    return render(request, template_name, context)

def enrolled_student(request):
    enrolled = Enroll.objects.all()
    context = {
        'page': 'Enrolled Student',
        'enrolled' : enrolled,
    }
    template_name = 'dashboard/students/enrolled-student.html'
    return render(request, template_name, context)

def cancelled_student(request):
    context = {
        'page': 'Cancelled Student',
    }
    template_name = 'dashboard/students/cancelled-student.html'
    return render(request, template_name, context)

def delete_enrollement(request, enroll_id):
    if enroll_id != None:
        try:
            enroll = Enroll.objects.get(id=enroll_id)
            enroll.delete()
            messages.success(request, "Enrollment deleted successfully!")
            return redirect('dashboard:enrolled_student') 
        except Exception as e:
            print(e)
            messages.success(request, f'Enrollment deletion failed with: {e}')
            return redirect('dashboard:enrolled_student') 





def general_setting(request):
    context = {
        'page': 'General Setting',
    }
    template_name = 'dashboard/settings/general/general.html'
    return render(request, template_name, context)


def currencies(request):
    context = {
        'page': 'Currencies',
    }
    template_name = 'dashboard/settings/currencies/currencies.html'
    return render(request, template_name, context)

def payment_method(request):
    context = {
        'page': 'Payment Method',
    }
    template_name = 'dashboard/settings/payment/payment-method.html'
    return render(request, template_name, context)

def email_config(request):
    context = {
        'page': 'Email Configuration',
    }
    template_name = 'dashboard/settings/payment/payment-method.html'
    return render(request, template_name, context)

def email_template(request):
    context = {
        'page': 'Email Template',
    }
    template_name = 'dashboard/settings/payment/payment-method.html'
    return render(request, template_name, context)
