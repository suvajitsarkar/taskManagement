from django.contrib import admin

# Register your models here.
from .models import Tasks, Audit

admin.site.register(Tasks)
admin.site.register(Audit)
