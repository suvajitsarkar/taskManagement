from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='creator', null=True, on_delete=NULL)
    description = models.TextField(max_length=1000, help_text="Enter task summary")
    assigned_to = models.ManyToManyField(User, help_text="Select employees to assign the task")
    date_created = models.DateTimeField(auto_now=True)
    task_stages = (
        ('n', 'Not Started'),
        ('i', 'In Progress'),
        ('r', 'In Review'),
        ('d', 'Done'),
    )
    stage = models.CharField(
        max_length=1,
        choices=task_stages,
        default='n',
        help_text="Stage of the task",
    )

    class Meta:
        permissions = (('is_lead', 'lead can see all task'),)

    def __str__(self):
        """String for representing the Model object."""
        return self.task_name
