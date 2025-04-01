from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Currencies(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
    
    def __str__(self):
        return self.name
    
    
class Project_Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name

class Clients(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name
    



class Projects(models.Model):
    prio = [
        ('Critical','Critical'),
        ('High','High'),
        ('Low','Low'),
        ('Medium','Medium'),
    ]
    
    stat = [
        ('New Project','New Project'),
        ('Inprogress','Inprogress'),
        ('Pending','Pending'),
        ('Completed','Completed'),
    ]
    
    project_no =  models.CharField(max_length=200)
    title =  models.CharField(max_length=200)
    slug =  models.CharField(max_length=200)
    client =  models.ForeignKey(Clients,blank=True, null=True, on_delete=models.CASCADE)
    category =  models.ForeignKey(Project_Categories,blank=True, null=True, on_delete=models.CASCADE)
    progress =  models.CharField(max_length=200, blank=True, null=True)
    calculate_progress =  models.CharField(max_length=200,blank=True, null=True )
    description =  models.TextField(max_length=200,blank=True, null=True)
    alert_overdeu =  models.BooleanField(default=True)
    start_date =  models.DateField()
    end_date =  models.DateField()
    project_cost =  models.FloatField()
    status =  models.CharField(max_length=200, choices=stat, default="New Project")
    priority =  models.CharField(max_length=200,blank=True, null=True, choices=prio)
    notify_client =  models.BooleanField(default=False,)
    tags =  models.CharField(max_length=200,blank=True, null=True)
    assigned_to =  models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
           
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    


class Milestones(models.Model):
    stat = [
        ('New Project','New'),
        ('Inprogress','Inprogress'),
        ('Pending','Pending'),
        ('Completed','Completed'),
    ]
     
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    project =  models.ForeignKey(Projects,blank=True, null=True, on_delete=models.SET_NULL)
    progress = models.CharField(max_length=200, default=0)
    status = models.CharField(max_length=200, choices=stat, default="New")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
            
    def __str__(self):
        return self.name
    


class Training(models.Model):
    stat = [
        ('Pending','Pending'),
        ('Started','Started'),
        ('Completed','Completed'),
        ('Terminated','Terminated'),
    ]
    perf = [
        ('not concluded','not concluded'),
        ('satisfactory','satisfactory'),
        ('average','average'),
        ('poor','poor'),
        ('excellent','excellent'),
    ]
    
    training_name = models.CharField(max_length=200)
    user =  models.ForeignKey(User,blank=True, null=True, related_name='employee', on_delete=models.SET_NULL)
    assigned_by =  models.ForeignKey(User,blank=True, null=True,related_name='assigner', on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    vendor_name = models.CharField(max_length=200)
    training_cost = models.CharField(max_length=200)
    remarks =  models.TextField()
    status = models.CharField(max_length=200, choices=stat, default="Pending")
    performance = models.CharField(max_length=200, choices=perf, default="not concluded")
    upload_file = models.FileField(blank=True, null=True,upload_to="training/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Training'
            
    def __str__(self):
        return self.training_name
    


class Tasks(models.Model):
    stat = [
        ('Pending','Pending'),
        ('Inprogess','Inprogess'),
        ('Completed','Completed'),
        ('New','New'),
    ]
    prio = [
        ('Critical','Critical'),
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low'),
    ]
    
    title = models.CharField(max_length=200)
    user =  models.ForeignKey(User,blank=True, null=True, related_name='users', on_delete=models.SET_NULL)
    assigned_by =  models.ForeignKey(User,blank=True, null=True,related_name='assigned_by', on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    remarks =  models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=stat, default="New")
    priority = models.CharField(max_length=200, choices=prio, default="Low")
    upload_file = models.FileField(blank=True, null=True,upload_to="tasks/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
            
    def __str__(self):
        return self.title
    


class Calender_event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    backgroundColor = models.CharField(max_length=7, default='#333333')
    borderColor = models.CharField(max_length=7, default='#333333')

    def __str__(self):
        return self.title