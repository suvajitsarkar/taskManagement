from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/get_data', views.get_data, name='get_data'),
    path('create', views.create_tasks, name='create'),
    path('view_tasks', views.view_tasks, name='view_tasks'),
    path('<int:pk>/update', views.UpdateTasks.as_view(), name='update_tasks'),
    path('view/<int:pk>', views.audit_detail_view, name='view_update')
]
