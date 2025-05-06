"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', task_views.home, name='home'),
    path('signup/', task_views.signup, name='signup'),
    path('tasks/', task_views.tasks, name='tasks'),
    path('logout/', task_views.close_session, name='logout'),
    path('signin/', task_views.signin, name='signin'),
    path('tasks/create_task/', task_views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', task_views.task_details, name='url_task_details'),
    path('tasks/<int:task_id>/complete', task_views.task_complete, name='url_task_complete'),
    path('tasks/<int:task_id>/delete', task_views.task_delete, name='url_task_delete'),
    path('tasks/finished/', task_views.finished_task, name='url_finished_task'),

]
