from django.db import models
from django.contrib.auth.models import User
from .constants import TASK_STAGES
from django.db.models.signals import post_save


# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='Creator', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, help_text="Enter task summary")
    assigned_to = models.ManyToManyField(User, help_text="Select employees to assign the task")
    updated_by = models.ForeignKey(User, related_name='Updater', null=True, on_delete=models.CASCADE)
    stage = models.CharField(
        max_length=1,
        choices=TASK_STAGES,
        default=TASK_STAGES[0],
        help_text="Stage of the task",
    )

    @property
    def stage_value(self):
        for i in TASK_STAGES:
            if i[0] == self.stage:
                return i[1]

    class Meta:
        permissions = (('is_lead', 'lead can add task'), ('is_emp', 'employee can change progress of task'),)

    def __str__(self):
        return self.task_name


class Audit(models.Model):
    updater = models.ForeignKey(User, on_delete=models.CASCADE)
    task_obj = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    stage = models.CharField(
        max_length=1,
        choices=TASK_STAGES,
        default=TASK_STAGES[0],
        help_text="Stage of the task",
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def stage_value(self):
        for i in TASK_STAGES:
            if i[0] == self.stage:
                return i[1]

    class Meta:
        permissions = (('is_lead', 'lead can add task'), ('is_emp', 'employee can change progress of task'),)

    def __str__(self):
        return self.task_obj


def create_audit(sender, **kwargs):
    for i in kwargs:
        print(i, kwargs[i])
    print("Sender Details:-")
    print(kwargs['instance'].updated_by)
    Audit.objects.create(updater=kwargs['instance'].updated_by,
                         task_obj=kwargs['instance'],
                         task_id=kwargs['instance'].id,
                         stage=kwargs['instance'].stage)


post_save.connect(create_audit, sender=Tasks)
