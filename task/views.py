from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .forms import TasksForm
from .models import Tasks, Audit
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404

# Create your views here.


@login_required
def index(request):
    context = {

    }
    return render(request, 'index.html', context=context)


@login_required
def get_data(request):
    data = Tasks.objects.count()
    return JsonResponse({'data': data})


@permission_required('task.is_lead')
def create_tasks(request):
    form = TasksForm(request.POST)
    if form.is_valid():
        form.instance.created_by = request.user
        form.instance.updated_by = request.user
        form.save()
        return HttpResponseRedirect('view_tasks')
    context = {'form': form}
    return render(request, 'create.html', context=context)


@login_required
def view_tasks(request):
    if request.user.has_perm('task.is_lead'):
        data = Tasks.objects.filter(created_by=request.user)
    else:
        data = Tasks.objects.filter(assigned_to=request.user)
    return render(request, 'view_task.html', context={'data': data})


@permission_required('task.is_lead')
def audit_detail_view(request, pk):
    try:
        audit = Audit.objects.filter(task_id=pk)
    except Audit.DoesNotExist:
        raise Http404('Audit does not exist')

    return render(request, 'task/audit_view_form.html', context={'audit': audit})


class UpdateTasks(PermissionRequiredMixin, UpdateView):
    model = Tasks
    fields = ['stage', 'updated_by']
    template_name_suffix = '_update_form'
    permission_required = 'task.is_emp'
    success_url = reverse_lazy('view_tasks')
